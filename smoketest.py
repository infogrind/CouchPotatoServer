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
CP_IP = "127.0.0.1"
CP_PORT = 5050

import os
import shutil
import signal
import socket
import sys
import subprocess
import tempfile
import time


class TestContext:
    def __enter__(self):
        self.tmpdirname = tempfile.mkdtemp()
        print "Temporary directory is {}".format(self.tmpdirname)
        shutil.copyfile(TEST_SETTINGS, self.tmpdirname + "/settings.conf")

        # Use temporary directory as data directory; it will be deleted again
        # below.
        args = DEFAULT_ARGS + "--data_dir {}".format(self.tmpdirname).split()
        print "Running application in subprocess"
        self.child = subprocess.Popen([PROGRAM] + args)
        print "Subrocess is running. Waiting {} seconds to warm up.".format(
                WARMUP_TIME_SEC)
        time.sleep(WARMUP_TIME_SEC)


    def __exit__(self, exc_type, exc_value, traceback):
        # Note: we don't check if there were any exceptions; we want to
        # terminate in any case.
        try:
            self.child.terminate()

            # TODO(marius): Find out how to use a timeout here and force the
            # process to terminate in case it doesn't react.
            print ("Sent SIGTERM, waiting for child process {} to "
            "terminate.").format(self.child.pid)
            self.child.wait()
            self.child = None

        finally:
            # Clean up temporary directory
            try:
                shutil.rmtree(self.tmpdirname)
            except:
                print "Error removing temporary directory {}".format(
                        self.tmpdirname)


def isPortOpen(ip, port):
    """
    Verifies if there is an open TCP socket at the given IP address and port.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, port))
        print "Socket connected at {}:{}".format(ip, port)
        return True
    except:
        print "Error connecting to {}:{}: {}".format(ip, port,
            sys.exc_info()[0])
        time.sleep(1)
        return False
    finally:
        try:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except:
            # Nothing to do, if we couldn't shut down, so be it. (This happens
            # normally if we couldn't connect to the socket in the first place.)
            pass


def main():
    """
    Main function
    """
    with TestContext():
        print "Testing if TCP connection can be made at {}:{}".format(CP_IP,
            CP_PORT)
        assert(isPortOpen(CP_IP, CP_PORT))


if __name__ == "__main__":
    main()
