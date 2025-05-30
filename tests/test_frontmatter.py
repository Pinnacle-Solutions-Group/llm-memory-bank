"""Tests for frontmatter parsing and transformation using activation-based system."""

import pytest

from lib.common import (
    create_cursor_frontmatter,
    create_windsurf_frontmatter,
    derive_editor_fields,
    extract_frontmatter,
    validate_frontmatter,
)


class TestFrontmatterExtraction:
    """Test frontmatter extraction from markdown content."""

    def test_extract_activation_frontmatter(self):
        """Test extracting activation-based frontmatter."""
        content = """---
description: "Simple rule description"
activation: glob
globs: "**/*.ts,**/*.tsx"
---

# Rule Content

This is the rule body.
"""
        frontmatter, body = extract_frontmatter(content)

        assert frontmatter["description"] == "Simple rule description"
        assert frontmatter["activation"] == "glob"
        assert frontmatter["globs"] == "**/*.ts,**/*.tsx"
        assert body.strip().startswith("# Rule Content")

    def test_extract_multiline_description(self):
        """Test extracting multi-line description with pipe syntax."""
        content = """---
description: |
  Defines the core logic for the AI to determine its operational FOCUS
  (Planning, Implementation, Debugging) and how to apply other rule sets.
activation: always
---

# Rule Content
"""
        frontmatter, body = extract_frontmatter(content)

        expected_desc = (
            "Defines the core logic for the AI to determine its operational FOCUS\n"
            "(Planning, Implementation, Debugging) and how to apply other rule sets."
        )
        assert frontmatter["description"] == expected_desc
        assert frontmatter["activation"] == "always"

    def test_extract_no_frontmatter(self):
        """Test content without frontmatter."""
        content = """# Rule Content

This is just markdown without frontmatter.
"""
        frontmatter, body = extract_frontmatter(content)

        assert frontmatter == {}
        assert body == content


class TestActivationValidation:
    """Test validation of activation-based frontmatter."""

    def test_missing_activation_field(self):
        """Test that missing activation field raises error."""
        frontmatter = {"description": "Test rule"}

        with pytest.raises(ValueError, match="Missing required 'activation' field"):
            validate_frontmatter(frontmatter)

    def test_invalid_activation_value(self):
        """Test that invalid activation value raises error."""
        frontmatter = {"description": "Test rule", "activation": "invalid"}

        with pytest.raises(ValueError, match="Invalid activation type: invalid"):
            derive_editor_fields("invalid")

    def test_glob_activation_requires_globs(self):
        """Test that glob activation requires globs field."""
        frontmatter = {"description": "Test rule", "activation": "glob"}

        with pytest.raises(
            ValueError, match="activation: glob requires non-empty globs"
        ):
            validate_frontmatter(frontmatter)

    def test_always_activation_with_globs_invalid(self):
        """Test that always activation with globs is invalid."""
        frontmatter = {
            "description": "Test rule",
            "activation": "always",
            "globs": "**/*.ts",
        }

        with pytest.raises(
            ValueError, match="activation: always should not have globs field"
        ):
            validate_frontmatter(frontmatter)


class TestCursorFrontmatter:
    """Test Cursor-specific frontmatter generation."""

    def test_cursor_always_rule(self):
        """Test Cursor always activation rule."""
        frontmatter = {
            "description": "Core meta rules for AI behavior",
            "activation": "always",
        }

        result = create_cursor_frontmatter(frontmatter)
        expected = """---
description: Core meta rules for AI behavior
globs: 
alwaysApply: true
---

"""
        assert result == expected

    def test_cursor_glob_rule(self):
        """Test Cursor glob activation rule (Auto-Attached)."""
        frontmatter = {
            "description": "TypeScript coding standards",
            "activation": "glob",
            "globs": "**/*.ts,**/*.tsx",
        }

        result = create_cursor_frontmatter(frontmatter)
        expected = """---
description: TypeScript coding standards
globs: **/*.ts,**/*.tsx
---

"""
        assert result == expected
        # Should omit alwaysApply for Auto-Attached behavior
        assert "alwaysApply" not in result

    def test_cursor_agent_requested_rule(self):
        """Test Cursor agent-requested activation rule."""
        frontmatter = {
            "description": "Advanced debugging techniques",
            "activation": "agent-requested",
        }

        result = create_cursor_frontmatter(frontmatter)
        expected = """---
description: Advanced debugging techniques
globs: 
alwaysApply: false
---

"""
        assert result == expected

    def test_cursor_manual_rule(self):
        """Test Cursor manual activation rule."""
        frontmatter = {
            "description": "Manual documentation generator",
            "activation": "manual",
        }

        result = create_cursor_frontmatter(frontmatter)
        expected = """---
description: Manual documentation generator
globs: 
alwaysApply: false
---

"""
        assert result == expected

    def test_cursor_multiline_description(self):
        """Test Cursor frontmatter with multi-line description."""
        frontmatter = {
            "description": "Defines the core logic for the AI to determine its operational FOCUS\n(Planning, Implementation, Debugging) and how to apply other rule sets.",
            "activation": "always",
        }

        result = create_cursor_frontmatter(frontmatter)
        expected = """---
description: Defines the core logic for the AI to determine its operational FOCUS
(Planning, Implementation, Debugging) and how to apply other rule sets.
globs: 
alwaysApply: true
---

"""
        assert result == expected

    def test_cursor_empty_description(self):
        """Test Cursor frontmatter with empty description."""
        frontmatter = {"description": "", "activation": "manual"}

        result = create_cursor_frontmatter(frontmatter)
        expected = """---
description: 
globs: 
alwaysApply: false
---

"""
        assert result == expected


class TestWindsurfFrontmatter:
    """Test Windsurf-specific frontmatter generation."""

    def test_windsurf_always_rule(self):
        """Test Windsurf always activation rule."""
        frontmatter = {
            "description": "Core meta rules for AI behavior",
            "activation": "always",
        }

        result = create_windsurf_frontmatter(frontmatter)
        expected = """---
trigger: always
description: Core meta rules for AI behavior
globs: 
---"""
        assert result == expected

    def test_windsurf_glob_rule(self):
        """Test Windsurf glob activation rule."""
        frontmatter = {
            "description": "TypeScript coding standards",
            "activation": "glob",
            "globs": "**/*.ts,**/*.tsx",
        }

        result = create_windsurf_frontmatter(frontmatter)
        expected = """---
trigger: glob
description: TypeScript coding standards
globs: **/*.ts,**/*.tsx
---"""
        assert result == expected

    def test_windsurf_agent_requested_rule(self):
        """Test Windsurf agent-requested activation rule."""
        frontmatter = {
            "description": "Advanced debugging techniques",
            "activation": "agent-requested",
        }

        result = create_windsurf_frontmatter(frontmatter)
        expected = """---
trigger: model
description: Advanced debugging techniques
globs: 
---"""
        assert result == expected

    def test_windsurf_manual_rule(self):
        """Test Windsurf manual activation rule."""
        frontmatter = {
            "description": "Manual documentation generator",
            "activation": "manual",
        }

        result = create_windsurf_frontmatter(frontmatter)
        expected = """---
trigger: manual
description: Manual documentation generator
globs: 
---"""
        assert result == expected

    def test_windsurf_multiline_description(self):
        """Test Windsurf frontmatter with multi-line description."""
        frontmatter = {
            "description": "Defines the systematic process for diagnosing, fixing, and documenting\nissues when FOCUS = DEBUGGING.",
            "activation": "agent-requested",
        }

        result = create_windsurf_frontmatter(frontmatter)
        expected = """---
trigger: model
description: Defines the systematic process for diagnosing, fixing, and documenting
issues when FOCUS = DEBUGGING.
globs: 
---"""
        assert result == expected


class TestEditorFieldDerivation:
    """Test derivation of editor-specific fields from activation."""

    def test_always_activation_derivation(self):
        """Test always activation derives correct fields."""
        fields = derive_editor_fields("always")

        assert fields["alwaysApply"] is True
        assert fields["globs"] == ""
        assert fields["trigger"] == "always"

    def test_glob_activation_derivation(self):
        """Test glob activation derives correct fields."""
        fields = derive_editor_fields("glob", globs="**/*.ts")

        assert fields["alwaysApply"] is False
        assert fields["globs"] == "**/*.ts"
        assert fields["trigger"] == "glob"

    def test_agent_requested_activation_derivation(self):
        """Test agent-requested activation derives correct fields."""
        fields = derive_editor_fields("agent-requested")

        assert fields["alwaysApply"] is False
        assert fields["globs"] == ""
        assert fields["trigger"] == "model"

    def test_manual_activation_derivation(self):
        """Test manual activation derives correct fields."""
        fields = derive_editor_fields("manual")

        assert fields["alwaysApply"] is False
        assert fields["globs"] == ""
        assert fields["trigger"] == "manual"

    def test_glob_without_globs_raises_error(self):
        """Test that glob activation without globs raises error."""
        with pytest.raises(
            ValueError, match="activation: glob requires non-empty globs"
        ):
            derive_editor_fields("glob")


class TestRoundtripConsistency:
    """Test that transformations maintain activation integrity."""

    def test_activation_roundtrip_consistency(self):
        """Test parsing activation frontmatter and regenerating it."""
        original = """---
description: "TypeScript rules"
activation: glob
globs: "**/*.ts,**/*.tsx"
---

# Rule body
"""
        frontmatter, body = extract_frontmatter(original)

        # Test Cursor generation
        cursor_result = create_cursor_frontmatter(frontmatter)
        cursor_fm, cursor_body = extract_frontmatter(cursor_result + body)

        # Test Windsurf generation
        windsurf_result = create_windsurf_frontmatter(frontmatter)
        windsurf_fm, windsurf_body = extract_frontmatter(windsurf_result + "\n" + body)

        # Verify original activation is preserved in concept
        assert frontmatter["activation"] == "glob"
        assert frontmatter["globs"] == "**/*.ts,**/*.tsx"

        # Verify Cursor output has correct fields for Auto-Attached
        assert "alwaysApply" not in cursor_fm  # Omitted for auto-attach
        assert cursor_fm["globs"] == "**/*.ts,**/*.tsx"

        # Verify Windsurf output has correct trigger
        assert windsurf_fm["trigger"] == "glob"
        assert windsurf_fm["globs"] == "**/*.ts,**/*.tsx"


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_missing_globs_for_glob_activation(self):
        """Test that glob activation without globs field fails validation."""
        frontmatter = {"description": "Test rule", "activation": "glob"}

        with pytest.raises(ValueError):
            create_cursor_frontmatter(frontmatter)

    def test_empty_globs_for_glob_activation(self):
        """Test that glob activation with empty globs fails validation."""
        frontmatter = {"description": "Test rule", "activation": "glob", "globs": ""}

        with pytest.raises(ValueError):
            create_cursor_frontmatter(frontmatter)

    def test_non_glob_activation_with_globs(self):
        """Test that non-glob activation with globs fails validation."""
        frontmatter = {
            "description": "Test rule",
            "activation": "always",
            "globs": "**/*.ts",
        }

        with pytest.raises(ValueError):
            create_cursor_frontmatter(frontmatter)
