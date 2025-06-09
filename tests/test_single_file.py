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
priority: 20
---
# Content 1
This is rule 1"""

        rule2 = """---
description: Rule 2
activation: always
priority: 10
---
# Content 2
This is rule 2"""

        rule3 = """---
description: Rule 3
activation: manual
priority: 5
---
# Content 3
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
            output_file = "output.md"
            transform_to_project_single_file(str(tmp_path), output_file)

            # Verify output
            expected = """# Rule 2

# Content 2
This is rule 2

---

# Rule 1

# Content 1
This is rule 1"""

            assert (tmp_path / output_file).read_text().strip() == expected.strip()

    @patch("glob.glob")
    def test_transform_with_missing_priority(self, mock_glob, tmp_path):
        """Test handling of rules with missing priority field."""
        # Create test rules
        rule1 = """---
description: Rule 1
activation: always
priority: 10
---
# Content 1
This is rule 1"""

        rule2 = """---
description: Rule 2
activation: always
---
# Content 2
This is rule 2"""

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
            output_file = "output.md"
            transform_to_project_single_file(str(tmp_path), output_file)

            expected = """# Rule 1

# Content 1
This is rule 1

---

# Rule 2

# Content 2
This is rule 2"""

            assert (tmp_path / output_file).read_text().strip() == expected.strip()

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
            assert output_path.read_text() == ""
