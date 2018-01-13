import glob

from six import exec_


def test_e2e_examples():
    """Run e2e tests over examples folder"""

    exs = glob.glob('examples/*.py')
    for ex in exs:
        # if exec runs without problems returns None
        exec_(open(ex).read())
