import argparse
import json
import subprocess
import sys
import time
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

# get list of recipes on source

raw_exsits_pkg = run_conan(['search', "*"])
exists_recipes = raw_exsits_pkg.decode('utf8').splitlines()[2:]

for letter in 'abcdefghijklmnopqrstuvwxyz-_':     # 第一个实例
    pat = '*' +letter +'*'
    print('search ...', pat)
    t = time.process_time()
    raw_source_recipes = run_conan(['search', '-r', source_remote, pat])
    print('time used :', time.process_time() - t)
    source_recipes = raw_source_recipes.decode('utf8').splitlines()[2:]  # Skip the header lines

    package_json = tempfile.NamedTemporaryFile(mode='r', encoding='utf8')

    for source_recipe in source_recipes:
        print(source_recipe)
        # Sync recipe over
        t = time.process_time()
        run_conan(['download', '-r', source_remote, '--recipe', source_recipe])
        print('time used :', time.process_time() - t)


 
