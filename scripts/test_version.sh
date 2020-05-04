#!/bin/bash
# Run this script test.sh from project root directory containing setup.py

set -ev

pr_branch=$1
if [ "${pr_branch}" == "false" ]
# All integrations pass if they're merged without a PR.
then
    exit 0
fi

echo "PR: branch passed in: $pr_branch"
pip3 install .
git fetch origin +refs/pull/${pr_branch}/merge
git checkout FETCH_HEAD
pr_version=$(python3 -c "import mplfinance; print(mplfinance.__version__)")
git checkout master
in_version=$(python3 -c "import mplfinance; print(mplfinance.__version__)")
echo "PR: ${pr_version}; Incumbent: ${in_version}"
result=$(python3 scripts/check_version.py --pr ${pr_version} --in ${in_version})
if [ "${result}" != "VersionCheck:pr>master" ]
then
    # version in PR doesn't pass the test
    echo "${result}"
    exit 1
fi