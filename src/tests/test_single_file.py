"""Tests for single file transformation functionality."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from lib.single_file import transform_to_project_single_file


class TestSingleFileTransformation:
    """Test single file transformation functionality."""

    @patch("glob.glob")
    def test_transform_to_project(self, mock_glob, tmp_path):
        """Test transforming rules into a single file with correct priority sorting."""
        # Create test rules
        rule1 = """---
description: Rule 1
activation: always
single_file: true
---
# Content 1
This is rule 1"""

        rule2 = """---
description: Rule 2
activation: always
single_file: true
---
# Content 2
This is rule 2"""

        rule3 = """---
description: Rule 3
activation: manual
---
# Content 3
This should not appear"""

        # Create temporary files
        with tempfile.TemporaryDirectory() as temp_dir:
            rule1_path = os.path.join(temp_dir, "20-rule1.md")
            rule2_path = os.path.join(temp_dir, "10-rule2.md")
            rule3_path = os.path.join(temp_dir, "05-rule3.md")

            with open(rule1_path, "w") as f:
                f.write(rule1)
            with open(rule2_path, "w") as f:
                f.write(rule2)
            with open(rule3_path, "w") as f:
                f.write(rule3)

            # Mock glob to return our test files
            mock_glob.return_value = [rule1_path, rule2_path, rule3_path]

            # Run transformation
            output_file = "output.md"
            transform_to_project_single_file(str(tmp_path), output_file)

            # Verify output contains rules in priority order
            content = (tmp_path / output_file).read_text()
            assert "Rule: 10-rule2" in content  # priority 10 comes first
            assert "Rule: 20-rule1" in content  # priority 20 comes second
            assert content.index("Rule: 10-rule2") < content.index("Rule: 20-rule1")
            assert "Content 2" in content
            assert "Content 1" in content
            assert "Content 3" not in content  # manual activation should be skipped

    @patch("glob.glob")
    def test_transform_with_missing_priority(self, mock_glob, tmp_path):
        """Test handling of rules with missing priority field."""
        # Create test rules
        rule1 = """---
description: Rule 1
activation: always
single_file: true
---
# Content 1
This is rule 1"""

        rule2 = """---
description: Rule 2
activation: always
single_file: true
---
# Content 2
This is rule 2"""

        # Create temporary files
        with tempfile.TemporaryDirectory() as temp_dir:
            rule1_path = os.path.join(temp_dir, "10-rule1.md")
            rule2_path = os.path.join(temp_dir, "rule2.md")  # No priority prefix = 999

            with open(rule1_path, "w") as f:
                f.write(rule1)
            with open(rule2_path, "w") as f:
                f.write(rule2)

            # Mock glob to return our test files
            mock_glob.return_value = [rule1_path, rule2_path]

            # Run transformation
            output_file = "output.md"
            transform_to_project_single_file(str(tmp_path), output_file)

            # Verify output contains rules in correct order
            content = (tmp_path / output_file).read_text()
            assert "Rule: 10-rule1" in content  # priority 10
            assert "Rule: rule2" in content  # priority 999 (default)
            assert content.index("Rule: 10-rule1") < content.index("Rule: rule2")
            assert "Content 1" in content
            assert "Content 2" in content

    @patch("glob.glob")
    def test_transform_empty_directory(self, mock_glob, tmp_path):
        """Test handling of empty rules directory."""
        mock_glob.return_value = []
        output_file = "output.md"
        transform_to_project_single_file(str(tmp_path), output_file)

        output_path = tmp_path / output_file
        assert output_path.exists()
        assert output_path.read_text() == ""

    @patch("glob.glob")
    def test_transform_no_always_rules(self, mock_glob, tmp_path):
        """Test handling when no rules have activation: always."""
        # Create test rule
        rule = """---
description: Rule 1
activation: manual
priority: 10
---
# Content
This should not appear"""

        # Create temporary file
        with tempfile.TemporaryDirectory() as temp_dir:
            rule_path = os.path.join(temp_dir, "rule.md")
            with open(rule_path, "w") as f:
                f.write(rule)

            # Mock glob to return our test file
            mock_glob.return_value = [rule_path]

            output_file = "output.md"
            transform_to_project_single_file(str(tmp_path), output_file)

            output_path = tmp_path / output_file
            assert output_path.exists()
            content = output_path.read_text()
            # Should be empty or have minimal content when no rules match
            assert "Rule" not in content

    @patch("glob.glob")
    def test_transform_with_section_rules(self, mock_glob, tmp_path):
        """Test transforming rules with section-specific destinations."""
        # Create test rules
        rule1 = """---
description: Main rule
activation: always
priority: 10
single_file: true
---
# Main Content
This goes in main CLAUDE.md"""

        rule2 = """---
description: Memory bank rule
activation: always
priority: 5
single_file: section:memory-bank
---
# Memory Bank Content
This goes in memory-bank/CLAUDE.md"""

        rule3 = """---
description: Skipped rule
activation: always
priority: 1
single_file: false
---
# Skipped Content
This should not appear"""

        # Create temporary files
        with tempfile.TemporaryDirectory() as temp_dir:
            rule1_path = os.path.join(temp_dir, "rule1.md")
            rule2_path = os.path.join(temp_dir, "rule2.md")
            rule3_path = os.path.join(temp_dir, "rule3.md")

            with open(rule1_path, "w") as f:
                f.write(rule1)
            with open(rule2_path, "w") as f:
                f.write(rule2)
            with open(rule3_path, "w") as f:
                f.write(rule3)

            # Mock glob to return our test files
            mock_glob.return_value = [rule1_path, rule2_path, rule3_path]

            # Run transformation
            output_file = "CLAUDE.md"
            transform_to_project_single_file(str(tmp_path), output_file)

            # Verify main CLAUDE.md
            main_output = tmp_path / output_file
            assert main_output.exists()
            main_content = main_output.read_text()
            assert "# CLAUDE.md" in main_content
            assert "Main Content" in main_content
            assert "Memory Bank Content" not in main_content
            assert "Skipped Content" not in main_content
            assert "consult `/memory-bank/CLAUDE.md`" in main_content

            # Verify memory-bank/CLAUDE.md
            section_output = tmp_path / "memory-bank" / "CLAUDE.md"
            assert section_output.exists()
            section_content = section_output.read_text()
            assert "Memory-Bank Instructions" in section_content
            assert "Memory Bank Content" in section_content
            assert "Main Content" not in section_content

    @patch("glob.glob")
    def test_transform_with_multiple_sections(self, mock_glob, tmp_path):
        """Test transforming rules with multiple section destinations."""
        # Create test rules
        rule1 = """---
description: Main rule
activation: always
priority: 10
single_file: true
---
# Main Content
This goes in main CLAUDE.md"""

        rule2 = """---
description: Memory bank rule 1
activation: always
priority: 5
single_file: section:memory-bank
---
# Memory Bank Content 1
First memory bank rule"""

        rule3 = """---
description: Memory bank rule 2
activation: always
priority: 15
single_file: section:memory-bank
---
# Memory Bank Content 2
Second memory bank rule"""

        rule4 = """---
description: API docs rule
activation: always
priority: 1
single_file: section:api/docs
---
# API Documentation
API specific instructions"""

        # Create temporary files
        with tempfile.TemporaryDirectory() as temp_dir:
            rule_paths = []
            for i, rule in enumerate([rule1, rule2, rule3, rule4], 1):
                rule_path = os.path.join(temp_dir, f"rule{i}.md")
                with open(rule_path, "w") as f:
                    f.write(rule)
                rule_paths.append(rule_path)

            # Mock glob to return our test files
            mock_glob.return_value = rule_paths

            # Run transformation
            output_file = "CLAUDE.md"
            transform_to_project_single_file(str(tmp_path), output_file)

            # Verify main CLAUDE.md
            main_output = tmp_path / output_file
            assert main_output.exists()
            main_content = main_output.read_text()
            assert "# CLAUDE.md" in main_content
            assert "Main Content" in main_content
            assert "consult `/memory-bank/CLAUDE.md`" in main_content
            assert "consult `/api/docs/CLAUDE.md`" in main_content

            # Verify memory-bank/CLAUDE.md has both rules in priority order
            mb_output = tmp_path / "memory-bank" / "CLAUDE.md"
            assert mb_output.exists()
            mb_content = mb_output.read_text()
            assert "Memory Bank Content 1" in mb_content
            assert "Memory Bank Content 2" in mb_content
            # Check priority order (5 comes before 15)
            assert mb_content.index("Memory Bank Content 1") < mb_content.index("Memory Bank Content 2")

            # Verify api/docs/CLAUDE.md
            api_output = tmp_path / "api" / "docs" / "CLAUDE.md"
            assert api_output.exists()
            api_content = api_output.read_text()
            assert "Docs Instructions" in api_content
            assert "API Documentation" in api_content

    @patch("glob.glob")
    def test_backward_compatibility_skip(self, mock_glob, tmp_path):
        """Test that single_file: skip still works for backward compatibility."""
        # Create test rules
        rule1 = """---
description: Rule with skip
activation: always
priority: 10
single_file: skip
---
# Skipped Content
This should not appear"""

        rule2 = """---
description: Rule with true
activation: always
priority: 20
single_file: true
---
# Included Content
This should appear"""

        # Create temporary files
        with tempfile.TemporaryDirectory() as temp_dir:
            rule1_path = os.path.join(temp_dir, "rule1.md")
            rule2_path = os.path.join(temp_dir, "rule2.md")

            with open(rule1_path, "w") as f:
                f.write(rule1)
            with open(rule2_path, "w") as f:
                f.write(rule2)

            # Mock glob to return our test files
            mock_glob.return_value = [rule1_path, rule2_path]

            # Run transformation
            output_file = "CLAUDE.md"
            transform_to_project_single_file(str(tmp_path), output_file)

            # Verify output
            main_output = tmp_path / output_file
            assert main_output.exists()
            main_content = main_output.read_text()
            assert "Skipped Content" not in main_content
            assert "Included Content" in main_content

    @patch("glob.glob")
    def test_transform_claude_md_header(self, mock_glob, tmp_path):
        """Test that CLAUDE.md gets proper header and CONVENTIONS.md doesn't."""
        # Create test rule
        rule = """---
description: Test rule
activation: always
priority: 10
single_file: true
---
# Test Content
Some content"""

        with tempfile.TemporaryDirectory() as temp_dir:
            rule_path = os.path.join(temp_dir, "rule.md")
            with open(rule_path, "w") as f:
                f.write(rule)

            mock_glob.return_value = [rule_path]

            # Test CLAUDE.md
            transform_to_project_single_file(str(tmp_path), "CLAUDE.md")
            claude_content = (tmp_path / "CLAUDE.md").read_text()
            assert "# CLAUDE.md" in claude_content
            assert "This file provides guidance to Claude Code" in claude_content
            assert "## Core Rules" in claude_content

            # Test CONVENTIONS.md
            transform_to_project_single_file(str(tmp_path), "CONVENTIONS.md")
            conventions_content = (tmp_path / "CONVENTIONS.md").read_text()
            assert "# CLAUDE.md" not in conventions_content
            assert "This file provides guidance to Claude Code" not in conventions_content

    @patch("glob.glob")
    def test_no_main_rules_with_sections(self, mock_glob, tmp_path):
        """Test behavior when there are only section rules, no main rules."""
        # Create test rules
        rule1 = """---
description: Memory bank rule
activation: always
priority: 5
single_file: section:memory-bank
---
# Memory Bank Content
Section-specific content"""

        rule2 = """---
description: Skipped rule
activation: always
priority: 1
single_file: false
---
# Skipped Content
This should not appear"""

        with tempfile.TemporaryDirectory() as temp_dir:
            rule1_path = os.path.join(temp_dir, "rule1.md")
            rule2_path = os.path.join(temp_dir, "rule2.md")

            with open(rule1_path, "w") as f:
                f.write(rule1)
            with open(rule2_path, "w") as f:
                f.write(rule2)

            mock_glob.return_value = [rule1_path, rule2_path]

            # Run transformation
            output_file = "CLAUDE.md"
            transform_to_project_single_file(str(tmp_path), output_file)

            # Verify main CLAUDE.md still exists with header and conditional instructions
            main_output = tmp_path / output_file
            assert main_output.exists()
            main_content = main_output.read_text()
            assert "# CLAUDE.md" in main_content
            assert "## Conditional Instructions" in main_content
            assert "consult `/memory-bank/CLAUDE.md`" in main_content
            assert "## Core Rules" not in main_content  # No core rules section

            # Verify section file exists
            section_output = tmp_path / "memory-bank" / "CLAUDE.md"
            assert section_output.exists()
            assert "Memory Bank Content" in section_output.read_text()
