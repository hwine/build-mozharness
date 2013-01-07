#!/usr/bin/env python
import os
config = {
    "default_actions": [
        'clobber',
        'checkout-gecko',
        'download-gonk',
        'unpack-gonk',
        'checkout-gaia',
        'checkout-gaia-l10n',
        'checkout-gecko-l10n',
        'checkout-compare-locales',
        'update-source-manifest',
        'build',
        'build-symbols',
        'make-updates',
        'make-update-xml',
        'upload-updates',
        'prep-upload',
        'upload',
        'upload-source-manifest',
    ],
    "ssh_key": os.path.expanduser("~/.ssh/b2gbld_dsa"),
    "ssh_user": "b2gbld",
    "upload_remote_host": "pvtbuilds2.dmz.scl3.mozilla.com",
    "upload_remote_basepath": "/pub/mozilla.org/b2g/tinderbox-builds",
    "upload_dep_target_exclusions": ["unagi"],
    "tooltool_servers": ["http://runtime-binaries.pvt.build.mozilla.org/tooltool/"],
    "upload_remote_nightly_basepath": "/pub/mozilla.org/b2g/nightly",
    "gittool_share_base": "/builds/git-shared/git",
    "gittool_base_mirror_urls": [],
    "hgtool_share_base": "/builds/hg-shared",
    "hgtool_base_mirror_urls": ["http://hg-internal.dmz.scl3.mozilla.com"],
    "hgtool_base_bundle_urls": ["http://ftp.mozilla.org/pub/mozilla.org/firefox/bundles"],
    "target_suffix": "_betatest",
    "exes": {
        "tooltool.py": "/tools/tooltool.py",
    },
    "update": {
        "upload_remote_host": "update.boot2gecko.org",
        "upload_remote_basepath": "/data/update-channels/betatest",
        "base_url": "http://update.boot2gecko.org/betatest/",
        "ssh_key": os.path.expanduser("~/.ssh/b2gbld_dsa"),
        "ssh_user": "ec2-user",
        "autopublish": True,
    },
    "manifest": {
        "upload_remote_host": "stage.mozilla.org",
        "upload_remote_basepath": "/pub/mozilla.org/b2g/manifests",
        "ssh_key": os.path.expanduser("~/.ssh/b2gbld_dsa"),
        "ssh_user": "b2gbld",
        "target_suffix": "-stable",
        "branches": ['mozilla-b2g18'],
        "translate_hg_to_git": True,
        "translate_base_url": "http://cruncher.build.mozilla.org/mapper",
    },
    "env": {
        "CCACHE_DIR": "/builds/ccache",
        "CCACHE_COMPRESS": "1",
        "CCACHE_UMASK": "002",
        "SYMBOL_SERVER_HOST": "symbols1.dmz.phx1.mozilla.com",
        "SYMBOL_SERVER_USER": "b2gbld",
        "SYMBOL_SERVER_SSH_KEY": "/home/mock_mozilla/.ssh/b2gbld_dsa",
        "SYMBOL_SERVER_PATH": "/mnt/netapp/breakpad/symbols_b2g/",
        "POST_SYMBOL_UPLOAD_CMD": "/usr/local/bin/post-symbol-upload.py",
        "B2G_UPDATE_CHANNEL": "beta",
    },
    "purge_minsize": 15,
    "clobberer_url": "http://clobberer.pvt.build.mozilla.org/index.php",
    "is_automation": True,
}