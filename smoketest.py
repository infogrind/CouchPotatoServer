#!/usr/bin/env python2
"""
Smoke test for the CouchPotato application

This script launches the CouchPotato server and runs a number of tests, to make
sure the most critical features are working and that there is not some
fundamental problem.
"""

PROGRAM = "./CouchPotato.py"
DEFAULT_ARGS = "--debug --quiet".split()
WARMUP_TIME_SEC = 5
TEST_SETTINGS = "testdata/settings.conf"

import os
import shutil
import signal
import sys
import subprocess
import tempfile
import time


def main():
    """
    Main function
    """
    try:
        tmpdirname = tempfile.mkdtemp()
        print "Temporary directory is {}".format(tmpdirname)
        shutil.copyfile(TEST_SETTINGS, tmpdirname + "/settings.conf")

        # Use temporary directory as data directory; it will be deleted again
        # below.
        args = DEFAULT_ARGS + "--data_dir {}".format(tmpdirname).split()
        print "Running application in subprocess"
        child = subprocess.Popen([PROGRAM] + args)
        print "Subrocess is running. Waiting {} seconds to warm up.".format(
                WARMUP_TIME_SEC)
        time.sleep(WARMUP_TIME_SEC)
        child.terminate()

        # TODO(marius): Should use a timeout
        print "Sent SIGTERM, waiting for child process {} to terminate.".format(
                child.pid)
        child.wait()

    finally:
        try:
            shutil.rmtree(tmpdirname)
        except:
            print "Error removing temporary directory {}".format(tmpdirname)


if __name__ == "__main__":
    main()
