"""
Provides access to the configuration.
"""

import operator
from functools import reduce
from pathlib import Path
from urllib.parse import urljoin

from ruamel.yaml import YAML

from mcmd.utils.errors import ConfigError, McmdError

_config = None
_properties_file: Path = None


def set_config(config, properties_file):
    """The config module must not have dependencies on other modules in the config package so the necessary information
    should be passed here."""
    global _config
    if _config:
        raise ValueError('config already set')
    _config = config

    global _properties_file
    if _properties_file:
        raise ValueError('properties file already set')
    _properties_file = properties_file

    _persist()


def _persist():
    """Writes the config to disk."""
    YAML().dump(_config, _properties_file)


def get(*args):
    try:
        prop = _config
        for at in list(args):
            prop = prop[at]
        return prop
    except KeyError as e:
        raise ConfigError('missing property: {}'.format(_key_error_string(e)))


def url():
    try:
        return _get_selected_host_auth()['url']
    except KeyError as e:
        raise ConfigError('missing property: {}'.format(_key_error_string(e)))


def username():
    try:
        return _get_selected_host_auth()['username']
    except KeyError as e:
        raise ConfigError('missing property: {}'.format(_key_error_string(e)))


def token():
    return _get_selected_host_auth().get('token', None)


def password():
    return _get_selected_host_auth().get('password', None)


def git_paths():
    root = get('git', 'root')
    if root is None or len(root) == 0:
        return []
    else:
        root_path = Path(root)
        paths = get('git', 'paths')
        return [root_path.joinpath(path) for path in paths]


def api(endpoint):
    """Returns the combination of the host's url and the API endpoint."""
    url_ = get('host', 'selected')
    return urljoin(url_, get('api', endpoint))


def has_option(*args):
    try:
        reduce(operator.getitem, list(args), _config)
        return True
    except KeyError:
        return False


def set_host(url_):
    if host_exists(url_):
        _config['host']['selected'] = url_
    else:
        raise McmdError("There is no host with URL {}".format(url_))

    _persist()


def delete_host(url_):
    if host_exists(url_):
        del _config['host']['auth'][_get_auth_index(url_)]
    else:
        raise McmdError("There is no host with URL {}".format(url_))
    _persist()


def add_host(url_, name, pw=None):
    auth = {'url': url_,
            'username': name}
    if pw:
        auth['password'] = pw

    _config['host']['auth'].append(auth)
    _persist()


def host_exists(url_):
    return url_ in [auth['url'] for auth in _config['host']['auth']]


def _get_auth_index(url_):
    return [i for i, auth in enumerate(_config['host']['auth']) if auth['url'] == url_][0]


def _get_selected_host_auth():
    selected = get('host', 'selected')
    hosts = get('host', 'auth')
    for host_ in hosts:
        if host_['url'] == selected:
            return host_

    raise ConfigError("The selected host doesn't exist.")


def set_token(token_):
    if token_ is None:
        _get_selected_host_auth().pop('token', None)
    else:
        _get_selected_host_auth()['token'] = token_
    _persist()


def _key_error_string(error):
    return str(error).strip("'")
