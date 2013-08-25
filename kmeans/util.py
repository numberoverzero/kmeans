import os
import sysconfig

_soabi = sysconfig.get_config_var('SOABI')
_so = sysconfig.get_config_var('SO')
if _soabi:
    _so_suffix = '.' + _soabi + _so
else:
    _so_suffix = _so

def so_path(dir, filename):
    '''http://www.python.org/dev/peps/pep-3149/'''
    return os.path.join(dir, filename + _so_suffix)

def here(__file__):
    '''Absolute directory of a script given its __file__ value'''
    return os.path.dirname(os.path.realpath(__file__))
