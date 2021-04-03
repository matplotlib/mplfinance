import argparse
from packaging import version


def compare_versions(v_str1, v_str2):
    """
    Compares two version strings.
    
    In:
        v_str1: str, __version__ string
        v_str2: str, __version__ string
    
    Returns:
        '>' | '==' | '<', reads v_str1 (x) v_str2
    """
    
    p_str1 = version.parse(v_str1)
    p_str2 = version.parse(v_str2)
    if p_str1 > p_str2:
        return '>'
    
    if p_str1 == p_str2:
        return '=='
    
    return '<'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check versions.')
    parser.add_argument('--pr_v', type=str, help='mplfinance.__version__ for the PR')
    parser.add_argument('--in_v', type=str, help='mplfinance.__version__ for the `master` branch')
    
    args = parser.parse_args()
    test_tag = 'VersionCheck:{}'
    outcome = compare_versions(
        v_str1=args.pr_v, 
        v_str2=args.in_v
    )
    print(test_tag.format('pr{}master'.format(outcome)))