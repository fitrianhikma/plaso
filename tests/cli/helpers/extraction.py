#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the extraction CLI arguments helper."""

import argparse
import sys
import unittest

from plaso.cli import tools
from plaso.cli.helpers import extraction
from plaso.lib import errors

from tests.cli import test_lib as cli_test_lib


class ExtractionArgumentsHelperTest(cli_test_lib.CLIToolTestCase):
  """Tests for the extraction CLI arguments helper."""

  # pylint: disable=no-member,protected-access

  _PYTHON3_13_OR_LATER = sys.version_info[0:2] >= (3, 13)

  if _PYTHON3_13_OR_LATER:
    _EXPECTED_OUTPUT = """\
usage: cli_helper.py [--extract_winreg_binary] [--preferred_year YEAR]
                     [--skip_compressed_streams]

Test argument parser.

{0:s}:
  --extract_winreg_binary, --extract-winreg-binary
                        Extract binary Windows Registry values. WARNING: This
                        can make processing significantly slower.
  --preferred_year, --preferred-year YEAR
                        When a format\'s timestamp does not include a year,
                        e.g. syslog, use this as the initial year instead of
                        attempting auto-detection.
  --skip_compressed_streams, --skip-compressed-streams
                        Skip processing file content within compressed
                        streams, such as syslog.gz and syslog.bz2.
""".format(cli_test_lib.ARGPARSE_OPTIONS)

  else:
    _EXPECTED_OUTPUT = """\
usage: cli_helper.py [--extract_winreg_binary] [--preferred_year YEAR]
                     [--skip_compressed_streams]

Test argument parser.

{0:s}:
  --extract_winreg_binary, --extract-winreg-binary
                        Extract binary Windows Registry values. WARNING: This
                        can make processing significantly slower.
  --preferred_year YEAR, --preferred-year YEAR
                        When a format\'s timestamp does not include a year,
                        e.g. syslog, use this as the initial year instead of
                        attempting auto-detection.
  --skip_compressed_streams, --skip-compressed-streams
                        Skip processing file content within compressed
                        streams, such as syslog.gz and syslog.bz2.
""".format(cli_test_lib.ARGPARSE_OPTIONS)

  def testAddArguments(self):
    """Tests the AddArguments function."""
    argument_parser = argparse.ArgumentParser(
        prog='cli_helper.py', description='Test argument parser.',
        add_help=False,
        formatter_class=cli_test_lib.SortedArgumentsHelpFormatter)

    extraction.ExtractionArgumentsHelper.AddArguments(argument_parser)

    output = self._RunArgparseFormatHelp(argument_parser)
    self.assertEqual(output, self._EXPECTED_OUTPUT)

  def testParseOptions(self):
    """Tests the ParseOptions function."""
    options = cli_test_lib.TestOptions()

    test_tool = tools.CLITool()
    extraction.ExtractionArgumentsHelper.ParseOptions(options, test_tool)

    self.assertIsNone(test_tool._preferred_year)
    self.assertTrue(test_tool._process_compressed_streams)

    with self.assertRaises(errors.BadConfigObject):
      extraction.ExtractionArgumentsHelper.ParseOptions(options, None)

    # TODO: improve test coverage.


if __name__ == '__main__':
  unittest.main()
