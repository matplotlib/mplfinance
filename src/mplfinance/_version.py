
def parse_last_component(last_component_str):
    """
    Parse the last component of the version string __version__
    In:
        last_component_str: str, last component of version string e.g. for '0.12.3a5' is '3a5'
    Returns:
        a: str, e.g. for '3a5' is 3
        b: str, e.g. for '3a5' is 'alpha'
        c: str, e.g. for '3a5' is 5
    """
    spec_inv = {v:k for k,v in _specifier_.items()}
    for specifier in _specifier_.values():
        splt = last_component_str.split(specifier)
        if len(splt) == 1:
            continue
        return int(splt[0]), spec_inv[specifier], int(splt[1])
    

def parse_version(v_str):
    """
    Convert __version__ -> version_info format
    
    In:
        v_str: str, version string e.g. '0.12.3a5'
        
    Out:
        tuple, len == 5; format == version_info (see below)
    """
    tmp = v_str.split('.')
    a,b,c = parse_last_component(tmp[2])
    return (
        int(tmp[0]), int(tmp[1]), a, b, c
    )


def compare_versions(v_str1, v_str2):
    """
    In:
        v_str1: str, __version__ string parsable by parse_version
        v_str2: str, __version__ string parsable by parse_version
    
    Returns:
        '>' | '==' | '<', reads v_str1 (x) v_str2
    """
    
    p_str1 = parse_version(v_str1)
    p_str2 = parse_version(v_str2)
    p_str1[3] = _specifier_order_[p_str1[3]]
    p_str2[3] = _specifier_order_[p_str2[3]]
    out = []
    for i, comp_i in enumerate(p_str1):
        comp_j = p_str2[i]
        if comp_i > comp_j:
            out.append('>')
        elif comp_i == comp_j:
            out.append('==')
        elif comp_i < comp_j:
            out.append('<')
    
    if out[0] != '==':
        return out[0]
    
    if out[1] != '==':
        return out[1]
    
    if out[2] != '==':
        return out[2]
    
    if out[3] != '==':
        return out[3]
    
    if out[4] != '==':
        return out[4]

    return '=='


version_info = (0, 12, 3, 'alpha', 5)

_specifier_ = {
    'alpha': 'a',
    'beta': 'b',
    'candidate': 'rc',
    'final': ''
}

_specifier_order_ = {
    'alpha': 1,
    'beta': 2,
    'candidate': 3, 
    'final': 4
}

__version__ = '%s.%s.%s%s'%(version_info[0], version_info[1], version_info[2],
  '' if version_info[3]=='final' else _specifier_[version_info[3]]+str(version_info[4]))