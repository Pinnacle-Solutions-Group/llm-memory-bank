"""Tests for transformation between template and editor formats using activation-based system."""

import os
import tempfile
from pathlib import Path

import pytest

from lib.cursor import transform_from_project as cursor_from_project
from lib.cursor import transform_to_project as cursor_to_project
from lib.windsurf import transform_from_project as windsurf_from_project
from lib.windsurf import transform_to_project as windsurf_to_project


class TestCursorTransformations:
    """Test Cursor-specific transformations."""

    def test_cursor_link_transformation(self):
        """Test Cursor link transformation: rules/ → mdc:.cursor/rules/"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as src:
            content = """---
description: Test rule with links
activation: agent-requested
---

# Test Rule

See [other rule](rules/core/other-rule.md) for details.
Also check [memory bank](memory-bank/project/tech_context.md).

Multiple links: [rule1](rules/rule1.md) and [rule2](rules/workflow/rule2.md).
"""
            src.write(content)
            src.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".mdc", delete=False
            ) as dst:
                cursor_to_project(src.name, dst.name)

                with open(dst.name, "r") as f:
                    result = f.read()

                # Check link transformations
                assert "mdc:.cursor/rules/core/other-rule.mdc" in result
                assert "mdc:.cursor/rules/rule1.mdc" in result
                assert "mdc:.cursor/rules/workflow/rule2.mdc" in result
                assert "mdc:memory-bank/project/tech_context.md" in result

                # Ensure original links are replaced
                assert "(rules/core/other-rule.md)" not in result
                assert "(rules/rule1.md)" not in result

                # Check that it has expected Cursor frontmatter
                assert "alwaysApply: false" in result
                assert "globs: " in result

    def test_cursor_frontmatter_transformation(self):
        """Test Cursor frontmatter transformation with globs."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as src:
            content = """---
description: TypeScript coding standards
activation: glob
globs: "**/*.ts,**/*.tsx"
---

# TypeScript Rules

Use strict typing.
"""
            src.write(content)
            src.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".mdc", delete=False
            ) as dst:
                cursor_to_project(src.name, dst.name)

                with open(dst.name, "r") as f:
                    result = f.read()

                # Check Cursor-specific frontmatter format
                assert "description: TypeScript coding standards" in result
                assert "globs: **/*.ts,**/*.tsx" in result
                # Auto-Attached rules should omit alwaysApply
                assert "alwaysApply" not in result

    def test_cursor_reverse_transformation(self):
        """Test Cursor reverse transformation: mdc:.cursor/rules/ → rules/"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".mdc", delete=False) as src:
            content = """---
description: "Test rule with mdc links"
globs: "**/*.ts,**/*.tsx"
---

# Test Rule

See [other rule](mdc:.cursor/rules/core/other-rule.mdc) for details.
Also check [rule2](mdc:.cursor/rules/workflow/rule2.mdc).
"""
            src.write(content)
            src.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", delete=False
            ) as dst:
                cursor_from_project(src.name, dst.name)

                with open(dst.name, "r") as f:
                    result = f.read()

                # Check link transformations back to template format
                assert "rules/core/other-rule.md" in result
                assert "rules/workflow/rule2.md" in result

                # Ensure mdc links are replaced
                assert "mdc:.cursor/rules" not in result
                assert ".mdc" not in result

                # Check frontmatter is in activation-based format
                assert 'globs: "**/*.ts,**/*.tsx"' in result
                assert "activation: glob" in result


class TestWindsurfTransformations:
    """Test Windsurf-specific transformations."""

    def test_windsurf_link_transformation(self):
        """Test Windsurf link transformation: rules/ → .windsurf/rules/"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as src:
            content = """---
description: "Test rule with links"
activation: glob
globs: "**/*.ts,**/*.tsx"
---

# Test Rule

See [other rule](rules/core/other-rule.md) for details.
Also check [memory bank](memory-bank/project/tech_context.md).

Multiple links: [rule1](rules/rule1.md) and [rule2](rules/workflow/rule2.md).
"""
            src.write(content)
            src.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", delete=False
            ) as dst:
                windsurf_to_project(src.name, dst.name)

                with open(dst.name, "r") as f:
                    result = f.read()

                # Check link transformations
                assert ".windsurf/rules/core/other-rule.md" in result
                assert ".windsurf/rules/rule1.md" in result
                assert ".windsurf/rules/workflow/rule2.md" in result
                assert ".windsurf/memory-bank/project/tech_context.md" in result

                # Ensure original links are replaced
                assert "(rules/core/other-rule.md)" not in result
                assert "(rules/rule1.md)" not in result

                # Check that it has expected Windsurf frontmatter
                assert "trigger: glob" in result
                assert "globs: **/*.ts,**/*.tsx" in result

    def test_windsurf_trigger_derivation(self):
        """Test Windsurf trigger derivation in transformation."""
        test_cases = [
            # (activation, globs, expected_trigger)
            ("always", None, "always"),
            ("glob", "**/*.ts", "glob"),
            ("agent-requested", None, "model"),
            ("manual", None, "manual"),
        ]

        for activation, globs, expected_trigger in test_cases:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", delete=False
            ) as src:
                # Build frontmatter content
                fm_lines = ["---"]
                fm_lines.append(f'description: "Test {activation} rule"')
                fm_lines.append(f"activation: {activation}")
                if globs:
                    fm_lines.append(f'globs: "{globs}"')
                fm_lines.extend(["---", "", "# Rule Content"])

                content = "\n".join(fm_lines)
                src.write(content)
                src.flush()

                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".md", delete=False
                ) as dst:
                    windsurf_to_project(src.name, dst.name)

                    with open(dst.name, "r") as f:
                        result = f.read()

                    assert f"trigger: {expected_trigger}" in result

    def test_windsurf_reverse_transformation(self):
        """Test Windsurf reverse transformation: .windsurf/rules/ → rules/"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as src:
            content = """---
trigger: glob
description: "Test rule with windsurf links"
globs: "**/*.ts,**/*.tsx"
---

# Test Rule

See [other rule](.windsurf/rules/core/other-rule.md) for details.
Also check [rule2](.windsurf/rules/workflow/rule2.md).
"""
            src.write(content)
            src.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", delete=False
            ) as dst:
                windsurf_from_project(src.name, dst.name)

                with open(dst.name, "r") as f:
                    result = f.read()

                # Check link transformations back to template format
                assert "rules/core/other-rule.md" in result
                assert "rules/workflow/rule2.md" in result

                # Ensure windsurf links are replaced
                assert ".windsurf/rules" not in result

                # Check frontmatter conversion back to activation-based format
                assert 'globs: "**/*.ts,**/*.tsx"' in result
                assert "activation: glob" in result


class TestRoundtripConsistency:
    """Test template ↔ editor roundtrip consistency."""

    def test_cursor_roundtrip_consistency(self):
        """Test template → cursor → template maintains consistency."""
        original_content = """---
description: "Comprehensive test rule with multiple features"
activation: glob
globs: "**/*.ts,**/*.tsx,**/*.js,**/*.jsx"
---

# Comprehensive Test Rule

This rule tests multiple features:

- Link to [core rule](rules/core/general-coding-conventions.md)
- Link to [workflow rule](rules/workflow/planning/planning-rules.md)
- Reference to [memory bank](memory-bank/project/tech_context.md)

## Implementation Details

Follow the patterns described in [best practices](rules/best-practices/error-documentation-guidelines.md).
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as template:
            template.write(original_content)
            template.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".mdc", delete=False
            ) as cursor_file:
                # Template → Cursor
                cursor_to_project(template.name, cursor_file.name)

                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".md", delete=False
                ) as back_to_template:
                    # Cursor → Template
                    cursor_from_project(cursor_file.name, back_to_template.name)

                    with open(back_to_template.name, "r") as f:
                        result = f.read()

                    # Check activation integrity maintained
                    assert "activation: glob" in result
                    assert 'globs: "**/*.ts,**/*.tsx,**/*.js,**/*.jsx"' in result
                    assert "description:" in result

    def test_windsurf_roundtrip_consistency(self):
        """Test template → windsurf → template maintains consistency."""
        original_content = """---
description: "Advanced debugging rule with explicit manual activation"
activation: manual
---

# Manual Debugging Rule

This rule is manually invoked for complex debugging scenarios.

See [debugging guidelines](rules/workflow/debugging/debugging-rules.md) and
[error documentation](rules/best-practices/error-documentation-guidelines.md).
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as template:
            template.write(original_content)
            template.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", delete=False
            ) as windsurf_file:
                # Template → Windsurf
                windsurf_to_project(template.name, windsurf_file.name)

                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".md", delete=False
                ) as back_to_template:
                    # Windsurf → Template
                    windsurf_from_project(windsurf_file.name, back_to_template.name)

                    with open(back_to_template.name, "r") as f:
                        result = f.read()

                    # Check activation integrity maintained
                    assert "activation: manual" in result
                    assert "description:" in result


class TestEditorDifferences:
    """Test differences between editor-specific formats."""

    def test_frontmatter_differences(self):
        """Test that each editor generates its expected frontmatter format."""
        template_content = """---
description: "Multi-purpose test rule"
activation: glob
globs: "**/*.ts,**/*.tsx"
---

# Test Rule

Content here.
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as template:
            template.write(template_content)
            template.flush()

            # Test Cursor transformation
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".mdc", delete=False
            ) as cursor_file:
                cursor_to_project(template.name, cursor_file.name)

                with open(cursor_file.name, "r") as f:
                    cursor_result = f.read()

                # Cursor should omit alwaysApply for Auto-Attached mode
                assert "globs: " in cursor_result
                assert "alwaysApply" not in cursor_result

            # Test Windsurf transformation
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", delete=False
            ) as windsurf_file:
                windsurf_to_project(template.name, windsurf_file.name)

                with open(windsurf_file.name, "r") as f:
                    windsurf_result = f.read()

                # Windsurf should include trigger
                assert "trigger: glob" in windsurf_result
                assert "globs: " in windsurf_result

    def test_link_transformation_differences(self):
        """Test different link transformation patterns for each editor."""
        template_content = """---
description: "Link transformation test"
activation: always
---

# Link Test

See [rule](rules/test-rule.md) for details.
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as template:
            template.write(template_content)
            template.flush()

            # Test Cursor link transformation
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".mdc", delete=False
            ) as cursor_file:
                cursor_to_project(template.name, cursor_file.name)

                with open(cursor_file.name, "r") as f:
                    cursor_result = f.read()

                assert "mdc:.cursor/rules/test-rule.mdc" in cursor_result
                assert "alwaysApply: true" in cursor_result

            # Test Windsurf link transformation
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", delete=False
            ) as windsurf_file:
                windsurf_to_project(template.name, windsurf_file.name)

                with open(windsurf_file.name, "r") as f:
                    windsurf_result = f.read()

                assert ".windsurf/rules/test-rule.md" in windsurf_result
                assert "trigger: always" in windsurf_result
