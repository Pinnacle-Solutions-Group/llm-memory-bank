"""Integration tests for single file generation demonstrating real-world usage."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from lib.single_file import transform_to_project_single_file


class TestSingleFileIntegration:
    """Integration tests demonstrating real-world single file usage patterns."""

    @patch("glob.glob")
    def test_complete_workflow_example(self, mock_glob, tmp_path):
        """Test a complete workflow showing all single_file options in action."""
        
        # Example rules representing a real project structure
        core_rule = """---
description: Core coding standards that always apply
activation: always
single_file: true
---
# Core Coding Standards

Always follow these fundamental principles:
- Write clear, readable code
- Use meaningful variable names
- Add tests for new functionality"""

        memory_bank_rule = """---
description: Memory bank usage guidelines for AI assistants
activation: always
single_file: section:memory-bank
---
# Memory Bank Usage

When working with the memory bank:
- Always check existing documentation first
- Update project status when making changes
- Follow established patterns"""

        api_docs_rule = """---
description: API documentation generation guidelines
activation: always
single_file: section:docs/api
---
# API Documentation Guidelines

For API documentation:
- Use OpenAPI specifications
- Include code examples
- Keep documentation in sync with code"""

        editor_only_rule = """---
description: Editor-specific formatting that shouldn't be in CLAUDE.md
activation: always
single_file: false
---
# Editor-Specific Formatting

This rule applies only in editors, not in single files."""

        skip_legacy_rule = """---
description: Legacy rule using old skip syntax
activation: always
single_file: skip
---
# Legacy Rule

This uses the old 'skip' syntax for backward compatibility."""

        # Create temporary files
        rules = [
            ("05-core.md", core_rule),
            ("10-memory-bank-usage.md", memory_bank_rule),
            ("20-api-docs.md", api_docs_rule),
            ("15-editor-only.md", editor_only_rule),
            ("25-legacy.md", skip_legacy_rule),
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            rule_paths = []
            for filename, content in rules:
                rule_path = os.path.join(temp_dir, filename)
                with open(rule_path, "w") as f:
                    f.write(content)
                rule_paths.append(rule_path)

            # Mock glob to return our test files
            mock_glob.return_value = rule_paths

            # Run transformation
            transform_to_project_single_file(str(tmp_path), "CLAUDE.md")

            # Verify main CLAUDE.md structure
            main_file = tmp_path / "CLAUDE.md"
            assert main_file.exists()
            main_content = main_file.read_text()
            
            # Should have proper header
            assert "# CLAUDE.md" in main_content
            assert "This file provides guidance to Claude Code" in main_content
            
            # Should have conditional instructions for sections
            assert "## Conditional Instructions" in main_content
            assert "consult `/memory-bank/CLAUDE.md`" in main_content
            assert "consult `/docs/api/CLAUDE.md`" in main_content
            
            # Should have core rules section
            assert "## Core Rules" in main_content
            assert "Core Coding Standards" in main_content
            
            # Should NOT include editor-only or skipped content
            assert "Editor-Specific Formatting" not in main_content
            assert "Legacy Rule" not in main_content
            assert "Memory Bank Usage" not in main_content
            assert "API Documentation Guidelines" not in main_content

            # Verify memory-bank/CLAUDE.md
            mb_file = tmp_path / "memory-bank" / "CLAUDE.md"
            assert mb_file.exists()
            mb_content = mb_file.read_text()
            assert "Memory-Bank Instructions for Claude Code" in mb_content
            assert "Memory Bank Usage" in mb_content
            assert "Core Coding Standards" not in mb_content

            # Verify docs/api/CLAUDE.md
            api_file = tmp_path / "docs" / "api" / "CLAUDE.md"
            assert api_file.exists()
            api_content = api_file.read_text()
            assert "Api Instructions for Claude Code" in api_content
            assert "API Documentation Guidelines" in api_content
            assert "Memory Bank Usage" not in api_content

    @patch("glob.glob")
    def test_priority_ordering_across_sections(self, mock_glob, tmp_path):
        """Test that priority ordering works correctly within each section."""
        
        # Create rules with different priorities in same section
        rule1 = """---
description: High priority memory bank rule
activation: always
single_file: section:memory-bank
---
# High Priority Rule
This should come first"""

        rule2 = """---
description: Low priority memory bank rule  
activation: always
single_file: section:memory-bank
---
# Low Priority Rule
This should come second"""

        rule3 = """---
description: Medium priority memory bank rule
activation: always
single_file: section:memory-bank
---
# Medium Priority Rule
This should come in the middle"""

        with tempfile.TemporaryDirectory() as temp_dir:
            rule_paths = []
            filenames = ["05-rule1.md", "20-rule2.md", "10-rule3.md"]
            for rule, filename in zip([rule1, rule2, rule3], filenames):
                rule_path = os.path.join(temp_dir, filename)
                with open(rule_path, "w") as f:
                    f.write(rule)
                rule_paths.append(rule_path)

            mock_glob.return_value = rule_paths

            # Run transformation
            transform_to_project_single_file(str(tmp_path), "CLAUDE.md")

            # Check priority ordering in section file
            section_file = tmp_path / "memory-bank" / "CLAUDE.md"
            content = section_file.read_text()
            
            # Verify ordering: priority 5, then 10, then 20
            high_pos = content.find("High Priority Rule")
            medium_pos = content.find("Medium Priority Rule")
            low_pos = content.find("Low Priority Rule")
            
            assert high_pos < medium_pos < low_pos

    @patch("glob.glob")
    def test_nested_section_paths(self, mock_glob, tmp_path):
        """Test that deeply nested section paths work correctly."""
        
        rule = """---
description: Deeply nested section rule
activation: always
single_file: section:docs/api/v2/auth
---
# Authentication Documentation
Deep nesting test"""

        with tempfile.TemporaryDirectory() as temp_dir:
            rule_path = os.path.join(temp_dir, "10-nested-rule.md")
            with open(rule_path, "w") as f:
                f.write(rule)

            mock_glob.return_value = [rule_path]

            # Run transformation
            transform_to_project_single_file(str(tmp_path), "CLAUDE.md")

            # Check main file references the nested path
            main_content = (tmp_path / "CLAUDE.md").read_text()
            assert "consult `/docs/api/v2/auth/CLAUDE.md`" in main_content

            # Check nested directory structure was created
            nested_file = tmp_path / "docs" / "api" / "v2" / "auth" / "CLAUDE.md"
            assert nested_file.exists()
            assert "Authentication Documentation" in nested_file.read_text()