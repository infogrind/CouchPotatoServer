#!/usr/bin/env python2
"""
Smoke test for the CouchPotato application

This script launches the CouchPotato server and runs a number of tests, to make
sure the most critical features are working and that there is not some
fundamental problem.
"""

PROGRAM = "./CouchPotato.py"
ARGS = "--debug --console_log --data_dir ./data".split()
WARMUP_TIME = 10

import os
import shutil
import signal
import sys
import subprocess
import tempfile
import time


def main(cwd):
    """
    Main function
    """
    try:
        tmpdirname = tempfile.mkdtemp()
        print "Temporary directory is {}".format(tmpdirname)

        print "Starting CouchPotato as a child process."
        child = subprocess.Popen([PROGRAM] + ARGS)
        print "Child process PID is {}.".format(child.pid)

        print "Giving the application some time to set itself up."
        time.sleep(WARMUP_TIME)

        print "Sending SIGTERM to process {}.".format(child.pid)
        child.terminate()

        print "Waiting for it to shut down"
        child.wait()

        print "All done"

    finally:
        try:
            shutil.rmtree(tmpdirname)
        except:
            print "Error removing temporary directory {}".format(tmpdirname)


if __name__ == "__main__":
    print __file__
    print sys.argv[0]
    main(os.path.dirname(__file__))
