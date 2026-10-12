"""Check the init_db entrypoint contract without importing platform modules."""

import ast
from pathlib import Path


def _source_tree():
    source = Path(__file__).with_name("init_db.py").read_text(encoding="utf-8")
    return ast.parse(source, filename="init_db.py")


def _calls(node, name):
    return [
        child
        for child in ast.walk(node)
        if isinstance(child, ast.Call)
        and isinstance(child.func, ast.Name)
        and child.func.id == name
    ]


def _is_main_guard(node):
    if not isinstance(node, ast.If):
        return False
    test = node.test
    return (
        isinstance(test, ast.Compare)
        and isinstance(test.left, ast.Name)
        and test.left.id == "__name__"
        and len(test.ops) == 1
        and isinstance(test.ops[0], ast.Eq)
        and len(test.comparators) == 1
        and isinstance(test.comparators[0], ast.Constant)
        and test.comparators[0].value == "__main__"
    )


def test_no_module_level_database_initialization():
    tree = _source_tree()
    # Function bodies are deferred; other module statements execute on import.
    for statement in tree.body:
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for expression in statement.decorator_list + statement.args.defaults:
                assert not _calls(expression, "init_database")
            for expression in statement.args.kw_defaults:
                if expression is not None:
                    assert not _calls(expression, "init_database")
            continue
        assert not _calls(statement, "init_database")


def test_main_directly_calls_database_initialization():
    tree = _source_tree()
    mains = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "main"
    ]
    assert len(mains) == 1
    assert any(
        isinstance(statement, ast.Expr)
        and isinstance(statement.value, ast.Call)
        and isinstance(statement.value.func, ast.Name)
        and statement.value.func.id == "init_database"
        for statement in mains[0].body
    )


def test_main_is_called_only_in_entrypoint_guard():
    tree = _source_tree()
    guards = [node for node in tree.body if _is_main_guard(node)]
    assert len(guards) == 1
    guarded_calls = [
        call for statement in guards[0].body for call in _calls(statement, "main")
    ]
    assert guarded_calls
    assert set(_calls(tree, "main")) == set(guarded_calls)
