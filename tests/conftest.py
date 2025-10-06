# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.

"""File with fixtures and configurations required for all tests. Automatically imported to `test_` files.

Test functions generally follow this pattern:

def test_(Classname_methodname)|(functionname)_case(args in order from furthest to closest to this test, e.g. mocker, conftest_fixture, local_fixture, parameter):
    block with
    preparations for the test case

    block with
    pretest-assertions
    confirming the case setup

    block with
    the tested function being executed

    block with
    post-test assertions
    confirming the behaviour of the tested function

    block with
    cleanup
"""

import os

import pytest


def pytest_configure(config):
    """Configures the path for pytest to be the directory of this file for consistent relative paths."""
    pytest_ini_dir = os.path.dirname(os.path.abspath(config.inifile))
    os.chdir(pytest_ini_dir)


@pytest.fixture(scope="session")
def toc():
    """Initializing toc in session scope fixture to avoid load on gesetze-im-internet servers."""
    from gesetze_im_internet import toc

    return toc
