from mplfinance import _version
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check versions.')
    parser.add_argument('--pr', type=str, help='mplfinance.__version__ for the PR')
    parser.add_argument('--in', type=str, help='mplfinance.__version__ for the `master` branch')
    
    args = parser.parse_args()
    test_tag = 'VersionCheck:{}'
    outcome = _version.compare_versions(v_str1=args.pr, v_str2=args.in)
    print(test_tag.format('pr{}master'.format(outcome)))