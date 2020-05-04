#!/bin/bash

# Run this script test.sh from project root directory containing setup.py
pr_branch=$1
if ["${pr_branch}" == "false"]:
then
    exit 0
fi

pip3 install .
git checkout ${pr_branch}
pr_version=$(python3 -c "import mplfinance; print(mplfinance.__version__)")
git checkout master
in_version=$(python3 -c "import mplfinance; print(mplfinance.__version__)")
echo "PR: ${pr_version}; Incumbent: ${in_version}"
result=$(python3 -m mplfinance.check_version --pr ${pr_version} --in ${in_version})
tox
if ["${result}" != "VersionCheck:pr>master"]
then
    # version in PR doesn't pass the test
    echo "${result}"
    exit 1
fi