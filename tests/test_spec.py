"""Tests for spec module."""

from specink.core.spec import extract_identifiers, parse_spec_sections, parse_then_lines


def test_parse_spec_sections() -> None:
    """parse_spec_sections extracts Markdown headings."""
    content = """# Feature A

Some intro text.

## Scenario 1

Details here.

### Sub-section

More content.
"""
    sections = parse_spec_sections(content)
    assert len(sections) == 3
    assert sections[0].heading == "Feature A"
    assert sections[0].level == 1
    assert sections[1].heading == "Scenario 1"
    assert sections[2].heading == "Sub-section"


def test_parse_then_lines() -> None:
    """parse_then_lines extracts BDD THEN assertions."""
    content = """**GIVEN** a user
**WHEN** they click
**THEN** `handleClick` is called
**AND** the UserModal opens
"""
    assertions = parse_then_lines(content)
    assert len(assertions) == 1
    assert "handleClick" in assertions[0].identifiers


def test_extract_identifiers() -> None:
    """extract_identifiers finds quoted and camelCase names."""
    text = "The `my_function` and ThemeProvider must work"
    ids = extract_identifiers(text)
    assert "my_function" in ids
    assert "ThemeProvider" in ids


def test_extract_identifiers_ignores_plain_words() -> None:
    """extract_identifiers ignores plain English words."""
    text = "The ID is set and UserAccount is created"
    ids = extract_identifiers(text)
    assert "ID" not in ids
    assert "is" not in ids
    assert "set" not in ids
    assert "UserAccount" in ids
