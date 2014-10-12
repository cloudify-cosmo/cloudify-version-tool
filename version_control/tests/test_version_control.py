########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

__author__ = 'anna'

import testtools
import os
import shutil
from version_control.version_control import execute
import filecmp

TEST_DIR = 'version_control/tests/'
TEST_RESOURCES_DIR = TEST_DIR + 'resources/'


class TestBase(testtools.TestCase):

    def test_version(self):

        test_dirs = os.listdir(TEST_RESOURCES_DIR)

        for file in test_dirs:
            if os.path.isdir(os.path.join(TEST_RESOURCES_DIR, file)) \
                    and file.startswith('cloudify-'):
                print file

                input = TEST_RESOURCES_DIR + file + '/input'
                working_dir = TEST_RESOURCES_DIR + file + '/work-copy'
                expected_output = \
                    TEST_RESOURCES_DIR + file + '/expected-output'

                if not os.path.exists(input):
                    continue

                shutil.rmtree(working_dir, ignore_errors=True)

                # Copy the input because the files will be changed in place
                shutil.copytree(input, working_dir)
                execute("1.1", "3.1",
                        TEST_RESOURCES_DIR + 'config.yaml',
                        working_dir, 'm6', verbose=True)
                res = filecmp.dircmp(working_dir, expected_output)

                try:
                    self.assertEquals(0, len(res.diff_files))

                    for sd in res.subdirs.itervalues():
                        print sd.diff_files
                        self.assertEquals(0, len(sd.diff_files))
                except AssertionError:
                    filecmp.dircmp(working_dir, expected_output)\
                        .report_full_closure()
                    raise

    def test_illegal_versions(self):
        ex = self.assertRaises(
            SystemExit, execute, '1.1', '3.11',
            TEST_RESOURCES_DIR + 'config.yaml', '', 'm6', verbose=True)
        self.assertIn('illegal version', str(ex))
        ex = self.assertRaises(
            SystemExit, execute, '1', '3.1',
            TEST_RESOURCES_DIR + 'config.yaml', '', 'm6', verbose=True)
        self.assertIn('illegal version', str(ex))
        ex = self.assertRaises(
            SystemExit, execute, '1.1', '3.1',
            TEST_RESOURCES_DIR + 'config.yaml', '', 'd6', verbose=True)
        self.assertIn('illegal version', str(ex))
        ex = self.assertRaises(
            SystemExit, execute, '1.1', '3.1',
            TEST_RESOURCES_DIR + 'config.yaml', '', '6', verbose=True)
        self.assertIn('illegal version', str(ex))
        ex = self.assertRaises(
            SystemExit, execute, '1.1', '3.1.1.1',
            TEST_RESOURCES_DIR + 'config.yaml', '', 'm6', verbose=True)
        self.assertIn('illegal version', str(ex))
