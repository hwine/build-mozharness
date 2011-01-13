import os
import shutil
import subprocess
import sys
import unittest

try:
    import json
except:
    import simplejson as json

import mozharness.base.errors as errors
import mozharness.base.script as script

class TestScript(unittest.TestCase):
    def cleanup(self):
        if os.path.exists('test_logs'):
            shutil.rmtree('test_logs')
        for filename in ('localconfig.json', 'localconfig.json.bak'):
            if os.path.exists(filename):
                os.remove(filename)

    def test_helper_functions(self):
        self.cleanup()
        s = script.BaseScript(initial_config_file='test/test.json')
        if os.path.exists('test_dir'):
            if os.path.isdir('test_dir'):
                shutil.rmtree('test_dir')
            else:
                os.remove('test_dir')
        self.assertFalse(os.path.exists('test_dir'),
                         msg="test_helper_functions() cleanup failed")
        s.mkdir_p('test_dir/foo/bar/baz')
        self.assertTrue(os.path.isdir('test_dir/foo/bar/baz'),
                        msg="mkdir_p error")
        s.mkdir_p('test_dir/foo/bar/baz')
        self.assertTrue(os.path.isdir('test_dir/foo/bar/baz'),
                        msg="mkdir_p error when dir exists")
        s.download_file("http://www.google.com", file_name="test_dir/google",
                        error_level="ignore")
        self.assertTrue(os.path.exists('test_dir/google'),
                        msg="error downloading google.com")
        contents1 = s.get_output_from_command("cat test_dir/google")
        fh = open("test_dir/google")
        contents2 = fh.read()
        fh.close()
        self.assertEqual(contents1, contents2,
                         msg="get_output_from_command('cat file') differs from fh.read")
        self.assertEqual(s.run_command("cat google", cwd="test_dir"), 0,
                         msg="run_command('cat file') did not exit 0")
        s.move('test_dir/google', 'test_dir/google2')
        self.assertFalse(os.path.exists('test_dir/google'),
                         msg="test_dir/google still exists after move()")
        self.assertTrue(os.path.exists('test_dir/google2'),
                        msg="test_dir/google2 doesn't exist after move()")
        s.copyfile('test_dir/google2', 'test_dir/google')
        self.assertTrue(os.path.exists('test_dir/google'),
                         msg="test_dir/google doesn't exist after copyfile()")
        s.run_command("rm test_dir/google test_dir/google2")
        self.assertFalse(os.path.exists('test_dir/google'),
                         msg="run_command('rm file') did not remove file")
        s.rmtree('test_dir')
        self.assertFalse(os.path.exists('test_dir'),
                         msg="rmtree unsuccessful")
        s.rmtree('test_dir')
        self.assertFalse(os.path.exists('test_dir'),
                         msg="2nd rmtree unsuccessful")
        self.cleanup()

    def test_summary(self):
        """I need a log watcher helper function, here and in test_log."""
        self.cleanup()
        s = script.BaseScript(config={'log_type': 'multi'},
                              initial_config_file='test/test.json')
        info_logsize = os.path.getsize("test_logs/test_info.log")
        self.assertTrue(info_logsize > 0,
                        msg="initial info logfile missing/size 0")
        s.add_summary('one')
        info_logsize2 = os.path.getsize("test_logs/test_info.log")
        self.assertTrue(info_logsize < info_logsize2,
                        msg="add_summary() not logged")
        warning_logsize = os.path.getsize("test_logs/test_warning.log")
        s.add_summary('two', level="warning")
        warning_logsize2 = os.path.getsize("test_logs/test_warning.log")
        self.assertTrue(warning_logsize < warning_logsize2,
                        msg="add_summary(level='warning') not logged in warning log")
        info_logsize = os.path.getsize("test_logs/test_info.log")
        warning_logsize = os.path.getsize("test_logs/test_warning.log")
        s.summary()
        info_logsize2 = os.path.getsize("test_logs/test_info.log")
        warning_logsize2 = os.path.getsize("test_logs/test_warning.log")
        self.assertTrue(info_logsize < info_logsize2,
                        msg="summary() didn't log to info")
        self.assertTrue(warning_logsize < warning_logsize2,
                        msg="summary() with warning didn't log to warning")
        self.cleanup()

    def testMercurial(self):
        self.cleanup()
        s = script.MercurialScript(initial_config_file='test/test.json')
        s.mkdir_p('test_dir')
        s.run_command("touch test_dir/tools")
        s.scm_checkout("http://hg.mozilla.org/build/tools",
                      parent_dir="test_dir", clobber=True)
        self.assertTrue(os.path.isdir("test_dir/tools"))
        s.scm_checkout("http://hg.mozilla.org/build/tools",
                      dir_name="test_dir/tools", halt_on_failure=False)
        s.rmtree('test_dir')
        self.cleanup()

    def testNoop(self):
        self.cleanup()
        s = script.MercurialScript(config={'noop': True},
                                   initial_config_file='test/test.json')
        if os.path.exists('test_dir'):
            if os.path.isdir('test_dir'):
                shutil.rmtree('test_dir')
            else:
                os.remove('test_dir')
        self.assertFalse(os.path.exists('test_dir'),
                         msg="testNoop() cleanup failed")
        s.mkdir_p('test_dir/foo/bar/baz')
        self.assertFalse(os.path.exists('test_dir'),
                         msg="mkdir_p noop error")
        s.download_file("http://www.google.com", file_name="test_logs/google",
                        error_level="ignore")
        self.assertFalse(os.path.exists('test_logs/google'),
                         msg="download_file noop error")
        contents1 = s.run_command("cat test/test.json", cwd="configs",
                                  return_type="output")
        self.assertEqual(contents1, None,
                         msg="get_output_from_command noop error")
        s.run_command("touch test_logs/foo")
        self.assertFalse(os.path.exists('test_logs/foo'),
                         msg="run_command noop error")
        cwd = os.getcwd()
        s.chdir('test_logs', ignore_if_noop=True)
        self.assertEqual(cwd, os.getcwd(),
                         msg="chdir noop error")
        os.chdir(cwd)
        s.chdir('test_logs')
        self.assertEqual('%s/test_logs' % cwd, os.getcwd(),
                         msg="chdir noop noignore error")
        s.chdir(cwd)
        self.cleanup()

    def testLog(self):
        self.cleanup()
        s = script.BaseScript(config={'log_type': 'multi',
                                       'log_level': 'debug'},
                              initial_config_file='test/test.json')
        s.log_obj=None
        s2 = script.BaseScript(config={'log_type': 'multi'},
                               initial_config_file='test/test.json')
        for obj in (s, s2):
            obj.debug("Testing DEBUG")
            obj.warning("Testing WARNING")
            obj.warn("Testing WARNING 2")
            obj.error("Testing ERROR")
            obj.critical("Testing CRITICAL")
            try:
                obj.fatal("Testing FATAL")
            except:
                pass
            else:
                self.assertTrue(False, msg="fatal() didn't!")
        self.cleanup()

    def testRunCommand(self):
        self.cleanup()
        s = script.BaseScript(config={'log_type': 'multi',
                                       'log_level': 'debug'},
                              initial_config_file='test/test.json')
        error_logsize = os.path.getsize("test_logs/test_error.log")
        s.run_command(command="this_cmd_should_not_exist --help",
                      env={'GARBLE': 'FARG'},
                      error_list=errors.PythonErrorList)
        error_logsize2 = os.path.getsize("test_logs/test_error.log")
        error_logsize = error_logsize2
        s.run_command(command="ls",
                      cwd='/this_dir_should_not_exist',
                      error_list=errors.PythonErrorList)
        error_logsize2 = os.path.getsize("test_logs/test_error.log")
        self.assertTrue(error_logsize2 > error_logsize,
                        msg="command not found error not hit")
        error_logsize = error_logsize2
        output = s.get_output_from_command(command="ls",
                     cwd='/this_dir_should_not_exist')
        error_logsize2 = os.path.getsize("test_logs/test_error.log")
        self.assertTrue(error_logsize2 > error_logsize,
                        msg="command not found error not hit")
        error_logsize = error_logsize2
        output = s.get_output_from_command(command="ls /this_file_should_not_exist")
        error_logsize2 = os.path.getsize("test_logs/test_error.log")
        self.assertTrue(error_logsize2 > error_logsize,
                        msg="command not found error not hit")
        error_logsize = error_logsize2
        s.run_command(command="cat mozharness/base/errors.py",
                      error_list=[{
                       'substr': "error", 'level': "error"
                      },{
                       'regex': ',$', 'level': "ignore",
                      },{
                       'substr': ']$', 'level': "warning",
                      }])
        error_logsize2 = os.path.getsize("test_logs/test_error.log")
        self.assertTrue(error_logsize2 > error_logsize,
                        msg="command not found error not hit")
        self.cleanup()
