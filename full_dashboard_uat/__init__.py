"""Isolated full-dashboard browser UAT.

This package must not import the operating API server,
initialize or access the operating database, access broker
credentials, or perform external financial-data requests.

Only synthetic, explicitly registered UAT responses are allowed.
"""

UAT_MODE = "SYNTHETIC_ONLY"
OPERATING_DATABASE_ALLOWED = False
BROKER_CALLS_ALLOWED = False
LIVE_ORDERS_ALLOWED = False
