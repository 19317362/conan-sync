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

# python3 mysync.py --source conan-center --dest my --ignore_failures
# Check if conan is installed
# run_conan([], reraise_error=True)
# only download to local, without upload & remove
# get list of recipes on source
# only conan-community can search *
# bincrafters search failed

# member = ['conan-center','jfrog']
member = ['jfrog']

for source_remote in member:
    for letter in 'mnopqrstuvwxyz-_': #'abcdefghijklmnopqrstuvwxyz-_':     # 第一个实例
        raw_exsits_pkg = run_conan(['search', "*"])
            
        try:
            exists_recipes = raw_exsits_pkg.decode('utf8').splitlines()[2:]
        except:
            continue
        retry = 0
        raw_source_recipes = ''
        while retry < 8 :
            pat = '*' +letter +'*'
            print('search ...', pat)
            starttime = datetime.datetime.now()
            raw_source_recipes = run_conan(['search', '-r', source_remote, pat])
            endtime = datetime.datetime.now()
            print('time used :', (endtime - starttime).seconds)
            if raw_source_recipes is None:
                retry = retry + 1
                continue
            else:
                break

        if retry >=8 :
            print('GIVE UP ...', pat)
            continue

        try:
            source_recipes = raw_source_recipes.decode('utf8').splitlines()[2:]  # Skip the header lines
        except:
            continue

        package_json = tempfile.NamedTemporaryFile(mode='r', encoding='utf8')

        for source_recipe in source_recipes:
            print(source_recipe)
            if source_recipe.count('/')<2: # skip old patern like aaa/vvv
                continue

            if source_recipe in exists_recipes:  # Already present on dest
                # print(": Already present on dest, skipping")
                continue        
            # Sync recipe over
            print('downloading ...',source_recipe)
            starttime = datetime.datetime.now()
            run_conan(['download', '-r', source_remote, '--recipe', source_recipe])
            endtime = datetime.datetime.now()
            print('time used :', (endtime - starttime).seconds)
            



 
