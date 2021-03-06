#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
# ***** END LICENSE BLOCK *****

import os
import sys

# load modules from parent dir
sys.path.insert(1, os.path.dirname(sys.path[0]))

from mozharness.base.gaia_test import GaiaTest
from mozharness.mozilla.testing.unittest import TestSummaryOutputParserHelper


class GaiaUnitTest(GaiaTest):
    def __init__(self, require_config_file=False):
        GaiaTest.__init__(self, require_config_file)

    def run_tests(self):
        """
        Run the unit test suite.
        """
        dirs = self.query_abs_dirs()

        # make the gaia profile
        self.make_gaia(dirs['abs_gaia_dir'],
                       self.config.get('xre_path'),
                       debug=True)

        # build the testrunner command arguments
        python = self.query_python_path('python')
        cmd = [python, '-u', os.path.join(dirs['abs_runner_dir'],
                                          'gaia_unit_test',
                                          'main.py')]
        binary = os.path.join(os.path.dirname(self.binary_path), 'b2g-bin')
        cmd.extend(self._build_arg('--binary', binary))
        cmd.extend(self._build_arg('--profile', os.path.join(dirs['abs_gaia_dir'],
                                                             'profile-debug')))
        cmd.extend(self._build_arg('--symbols-path', self.symbols_path))

        output_parser = TestSummaryOutputParserHelper(config=self.config,
                                                      log_obj=self.log_obj,
                                                      error_list=self.error_list)
        # I don't like this output_timeout hardcode, but bug 920153
        code = self.run_command(cmd,
                                output_parser=output_parser,
                                output_timeout=1760)

        output_parser.print_summary('gaia-unit-tests')
        self.publish(code)

if __name__ == '__main__':
    gaia_unit_test = GaiaUnitTest()
    gaia_unit_test.run_and_exit()
