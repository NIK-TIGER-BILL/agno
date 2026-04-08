"""Tests to verify that decision_log.py uses timezone-aware UTC datetimes.

`datetime.utcnow()` was deprecated in Python 3.12 (see
https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow).
This test ensures the module uses `datetime.now(tz=timezone.utc)` instead.
"""

import ast
import textwrap
from pathlib import Path


DECISION_LOG_PATH = Path(__file__).resolve().parents[2] / "agno" / "learn" / "stores" / "decision_log.py"


class TestNoDeprecatedUtcnow:
    """Ensure decision_log.py does not call datetime.utcnow()."""

    def test_no_utcnow_calls(self) -> None:
        """Parse the source and assert there are zero `datetime.utcnow()` calls."""
        source = DECISION_LOG_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(DECISION_LOG_PATH))

        utcnow_calls: list[int] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "utcnow"
            ):
                utcnow_calls.append(node.lineno)

        assert utcnow_calls == [], (
            f"Found deprecated datetime.utcnow() calls at lines: {utcnow_calls}. "
            "Use datetime.now(tz=timezone.utc) instead."
        )

    def test_timezone_imported(self) -> None:
        """Verify that `timezone` is imported from the datetime module."""
        source = DECISION_LOG_PATH.read_text(encoding="utf-8")
        assert "from datetime import" in source
        # Check that timezone is in the import line
        for line in source.splitlines():
            if line.startswith("from datetime import"):
                assert "timezone" in line, (
                    "timezone must be imported from datetime to use datetime.now(tz=timezone.utc)"
                )
                break
