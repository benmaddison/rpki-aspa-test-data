# Copyright (c) 2022 Ben Maddison. All rights reserved.
#
# The contents of this file are licensed under the MIT License
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""rpki_aspa_test_data cli module."""

from __future__ import annotations

import argparse
import logging
import pathlib

from . import resources

log = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    help_fmt = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=help_fmt)
    parser.add_argument("--test-cases", "-c", type=pathlib.Path,
                        default=resources().joinpath("test-cases.yml"),
                        help="Test cases definition spec file\n"
                             "(default: %(default)s)")
    parser.add_argument("--extra-cases", "-e", nargs="*", type=pathlib.Path,
                        default=[],
                        help="Extra test case definitions\n"
                             "(default: %(default)s)")
    parser.add_argument("--output-path", "-o", type=pathlib.Path,
                        default=pathlib.Path("target"),
                        help="Output directory path\n"
                             "(default: %(default)s)")
    return parser.parse_args()
