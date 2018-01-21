import glob
import os
import subprocess


def test_e2e_examples():
    """Run e2e tests over examples folder"""
    os.chdir("examples")
    exs = glob.glob('*.py')
    for ex in exs:
        subprocess.check_call(["python", ex])
