import glob
import os
import os.path
import subprocess

def test_original_flavor_e2e_examples():
    """Run e2e tests for  folder"""

    # os.path.join makes this work on windows as well as linux
    new_dir  = os.path.join('examples','original_flavor')
    orig_dir = os.path.join('..','..')

    os.chdir(new_dir)

    exs = glob.glob('*.py') 
    try:
        for ex in exs:
            subprocess.check_call(["python", ex])
    finally:
        os.chdir(orig_dir)
