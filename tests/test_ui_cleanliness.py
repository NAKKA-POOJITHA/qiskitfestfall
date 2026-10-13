"""
QuantumCure AI - Unit Tests for UI Cleanliness & Master Prompt Compliance
Tests for strict no-emoji rule, mandatory research disclaimers, and color tokens.
"""

import re
from pathlib import Path
import pytest

root_dir = Path(__file__).resolve().parent.parent
EMOJI_PATTERN = re.compile(r"[\U0001F300-\U0001F9FF\u2600-\u26FF\u2700-\u27BF]")


def test_zero_emojis_in_frontend():
    """Verify that no emojis exist in frontend python files."""
    frontend_dir = root_dir / "frontend"
    for py_file in frontend_dir.rglob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        matches = EMOJI_PATTERN.findall(content)
        assert len(matches) == 0, f"Found emojis in {py_file.name}: {matches}"


def test_zero_emojis_in_app_py():
    """Verify that no emojis exist in root app.py."""
    app_file = root_dir / "app.py"
    content = app_file.read_text(encoding="utf-8")
    matches = EMOJI_PATTERN.findall(content)
    assert len(matches) == 0, f"Found emojis in app.py: {matches}"


def test_mandatory_disclaimer_present():
    """Verify that the mandatory disclaimer string is present."""
    disclaimer_text = "Research prototype, not clinical advice. Not validated for clinical use."
    
    styles_file = root_dir / "frontend" / "styles.py"
    assert disclaimer_text in styles_file.read_text(encoding="utf-8"), "Disclaimer missing in frontend/styles.py"

    app_file = root_dir / "app.py"
    assert disclaimer_text in app_file.read_text(encoding="utf-8"), "Disclaimer missing in app.py"


def test_specified_color_tokens():
    """Verify that the exact research color tokens are specified."""
    tokens = ["#7965E8", "#18A999", "#F08A78", "#F8FAFC", "#25324A", "#64748B", "#E5E7EB"]
    styles_content = (root_dir / "frontend" / "styles.py").read_text(encoding="utf-8")
    for t in tokens:
        assert t in styles_content, f"Token {t} missing in frontend/styles.py"
