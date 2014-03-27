# This is a template config file for b2g emulator unittest production.
import os

config = {
    # mozharness options
    "application": "b2g",
    "busybox_url": "http://runtime-binaries.pvt.build.mozilla.org/tooltool/sha512/0748e900821820f1a42e2f1f3fa4d9002ef257c351b9e6b78e7de0ddd0202eace351f440372fbb1ae0b7e69e8361b036f6bd3362df99e67fc585082a311fc0df",
    "xre_url": "http://runtime-binaries.pvt.build.mozilla.org/tooltool/sha512/ff548dd1267fb2b1e0bf26db7101a9b19625a1db02fb5d78731f2dd5fb624345e325d9952a005546017f72ca3de1f7d0a56c8b5cbded55dc84b7a2775227c037",
    "tooltool_servers": ["http://runtime-binaries.pvt.build.mozilla.org/tooltool/"],

    "exes": {
        'python': '/tools/buildbot/bin/python',
        'virtualenv': ['/tools/buildbot/bin/python', '/tools/misc-python/virtualenv.py'],
        'tooltool.py': "/tools/tooltool.py",
    },

    "find_links": [
        "http://pypi.pvt.build.mozilla.org/pub",
        "http://pypi.pub.build.mozilla.org/pub",
    ],
    "pip_index": False,

    "buildbot_json_path": "buildprops.json",

    "default_actions": [
        'clobber',
        'read-buildbot-config',
        'download-and-extract',
        'create-virtualenv',
        'install',
        'run-tests',
    ],
    "download_symbols": "ondemand",
    "download_minidump_stackwalk": True,
    "default_blob_upload_servers": [
        "https://blobupload.elasticbeanstalk.com",
    ],
    "blob_uploader_auth_file": os.path.join(os.getcwd(), "oauth.txt"),

    "run_file_names": {
        "jsreftest": "runreftestb2g.py",
        "mochitest": "runtestsb2g.py",
        "reftest": "runreftestb2g.py",
        "crashtest": "runreftestb2g.py",
        "xpcshell": "runtestsb2g.py"
    },
    # test harness options are located in the gecko tree
    "in_tree_config": "config/mozharness/b2g_emulator_config.py",
    "vcs_output_timeout": 1760,
}
