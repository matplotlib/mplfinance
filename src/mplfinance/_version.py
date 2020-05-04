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

version_info = (0, 12, 3, 'alpha', 5)

_specifier_ = {'alpha': 'a','beta': 'b','candidate': 'rc','final': ''}

__version__ = '%s.%s.%s%s'%(version_info[0], version_info[1], version_info[2],
  '' if version_info[3]=='final' else _specifier_[version_info[3]]+str(version_info[4]))