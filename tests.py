import glob
import os
import subprocess


def test_e2e_examples():
    """Run e2e tests over examples folder"""
    print('>>> tests.py')
    os.chdir("examples/original_flavor")
    exs = glob.glob('*.py')
    for ex in exs:
        subprocess.check_call(["python", ex])
