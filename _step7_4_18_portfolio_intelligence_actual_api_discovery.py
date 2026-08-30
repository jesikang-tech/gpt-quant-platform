from pathlib import Path
import ast

path = Path("core/portfolio_decision_intelligence.py")
text = path.read_text(encoding="utf-8")
tree = ast.parse(text)

print("===== PHASE 7-4-18 DISCOVERY 2 RETRY =====")
print("===== PORTFOLIO DECISION INTELLIGENCE ACTUAL API =====")
print()

print("===== DEFINITIONS =====")

for node in tree.body:
    if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
        print(
            f"{type(node).__name__}: "
            f"{node.name} "
            f"line={node.lineno}"
        )

print()
print("===== ADAPTIVE STRATEGY REFERENCES =====")

lines = text.splitlines()

for i, line in enumerate(lines, 1):
    if "adaptive_strategy" in line or "adaptive_action" in line:
        print(f"{i}: {line.strip()}")

print()
print("===== POSSIBLE ENTRYPOINTS =====")

for node in tree.body:
    if isinstance(node, ast.ClassDef):
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                print(f"{node.name}.{child.name} line={child.lineno}")

print()
print("===== PHASE 7-4-18 DISCOVERY 2 RETRY COMPLETE =====")
