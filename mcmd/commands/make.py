from mcmd import io
from mcmd.molgenis import api
from mcmd.molgenis.client import post, get
from mcmd.command import command
from mcmd.commands._registry import arguments
from mcmd.io import highlight
from mcmd.utils.errors import McmdError
from mcmd.utils.utils import lower_kebab, upper_snake


# =========
# Arguments
# =========

@arguments('make')
def add_arguments(subparsers):
    p_make = subparsers.add_parser('make',
                                   help='Make a user member of a role')
    p_make.set_defaults(func=make,
                        write_to_history=True)
    p_make.add_argument('user',
                        type=str,
                        help='The user to make a member')
    p_make.add_argument('role',
                        type=str,
                        help='The role to make the user a member of')


# =======
# Methods
# =======

@command
def make(args):
    io.start('Making user %s a member of role %s' % (highlight(args.user), highlight(args.role.upper())))

    group_name = _find_group(args.role)

    url = api.member(group_name)
    post(url, data={'username': args.user, 'roleName': args.role.upper()})


def _find_group(role):
    io.debug('Fetching groups')
    groups = get(api.rest2('sys_sec_Group'),
                 params={
                     'attrs': 'name'
                 })
    role = lower_kebab(role)

    matches = {len(group['name']): group['name'] for group in groups.json()['items'] if role.startswith(group['name'])}

    if not matches:
        raise McmdError('No group found for role %s' % upper_snake(role))

    return matches[max(matches, key=int)]
