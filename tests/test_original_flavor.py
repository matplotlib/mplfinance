import glob
import os
import subprocess

def test_original_flavor_e2e_examples():
    """Run e2e tests for  folder"""

    os.chdir("examples/original_flavor")
    exs = glob.glob('*.py')
    try:
        for ex in exs:
            subprocess.check_call(["python", ex])
    finally:
        os.chdir("../../")
