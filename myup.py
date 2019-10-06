import argparse
import json
import subprocess
import sys
import time
import datetime
# Parse args
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=str, required=True,
                    help="Name of conan remote from which recipes and packages are being copied to --dest")
parser.add_argument('--dest', type=str, required=True,
                    help="Name of conan remote receiving all of the contents of --source")
parser.add_argument('--exec', type=str, required=False, default='conan', help="Location of 'conan' command")
parser.add_argument('--ignore_failures', action='store_true', required=False, help="Ignore failures")

args = parser.parse_args(sys.argv[1:])

source_remote = args.source
dest_remote = args.dest
conan_cmd = args.exec
ignore_failures = args.ignore_failures

CONAN_CMD_TIMEOUT_SECS = 300


def run_conan(args, reraise_error=False):
    try:
        return subprocess.check_output(args=[conan_cmd] + args, timeout=CONAN_CMD_TIMEOUT_SECS)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print("Command failed")
        print(repr(e))
        if hasattr(e, 'returncode'):
            rc = "rc=" + str(e.returncode)
        else:
            rc = "Command timed out"
        print("{} output={}".format(rc, e.output))
        if reraise_error and not ignore_failures:
            raise e

def do_dld_and_up(source_recipe):
        print('downloading ...',source_recipe)
        starttime = datetime.datetime.now()
        run_conan(['download', '-r', source_remote, '--recipe', source_recipe])
        endtime = datetime.datetime.now()
        print('time used :', (endtime - starttime).seconds)
        try:
            print('upload ...', source_recipe)
            starttime = datetime.datetime.now()
            run_conan(['upload', '-r', dest_remote,'-c', source_recipe], reraise_error=True)
            endtime = datetime.datetime.now()
            print('time used :', (endtime - starttime).seconds)    
            return 0        
        except:
            return 1

# python3 mysync.py --source conan-center --dest my --ignore_failures
# Check if conan is installed
# run_conan([], reraise_error=True)
# only download to local, without upload & remove
# get list of recipes on source
# only conan-community can search *
# bincrafters search failed

# member = ['conan-center','jfrog']
raw_exsits_pkg = run_conan(['search', "*"])
exists_recipes = raw_exsits_pkg.decode('utf8').splitlines()[2:]

for source_recipe in exists_recipes:

    try:
        # print('upload ...', source_recipe)
        # starttime = datetime.datetime.now()
        upack = run_conan(['upload', '-r', dest_remote,'-c', source_recipe], reraise_error=True)
        if upack is None:
            do_dld_and_up(source_recipe)

        # endtime = datetime.datetime.now()
        # print('time used :', (endtime - starttime).seconds)        
    except:
        # Sync recipe over
        do_dld_and_up(source_recipe)

