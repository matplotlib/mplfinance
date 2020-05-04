from mplfinance import _version
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check versions.')
    parser.add_argument('--pr_v', type=str, help='mplfinance.__version__ for the PR')
    parser.add_argument('--in_v', type=str, help='mplfinance.__version__ for the `master` branch')
    
    args = parser.parse_args()
    test_tag = 'VersionCheck:{}'
    outcome = _version.compare_versions(
        v_str1=args.pr_v, 
        v_str2=args.in_v
    )
    print(test_tag.format('pr{}master'.format(outcome)))