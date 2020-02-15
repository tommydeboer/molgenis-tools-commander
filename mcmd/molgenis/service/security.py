import json
from typing import List, Optional
from urllib.parse import urljoin

from mcmd.core.compatibility import version
from mcmd.core.errors import McmdError
from mcmd.molgenis.service._client import api
from mcmd.molgenis.service._client.client import get, post, put
from mcmd.molgenis.service.rest_api_v2_mapper import map_to_role, map_to_user, map_to_role_membership, map_to_group
from mcmd.molgenis.service.system import Group, Role, User, RoleMembership
from mcmd.utils.time import timestamp


def get_group_roles(group: Group) -> List[Role]:
    roles = get(api.rest2('sys_sec_Role'),
                params={
                    'attrs': 'id,name,label,group(id,name)',
                    'q': 'group=={}'.format(group.id)
                }).json()['items']

    if len(roles) == 0:
        raise McmdError('No roles found for group {}'.format(group.name))

    return [map_to_role(role) for role in roles]


def is_member(user: User, role: Role) -> bool:
    memberships = get(api.rest2('sys_sec_RoleMembership'),
                      params={
                          'attrs': 'id',
                          'q': "user=={};role=={};(to=='',to=ge={})".format(user.id, role.id, timestamp())
                      }).json()['items']

    return len(memberships) > 0


def get_user(user_name: str) -> User:
    users = get(api.rest2('sys_sec_User'),
                params={
                    'attrs': 'id,username,changePassword,Email,active,superuser,password_',
                    'q': 'username=={}'.format(user_name)
                }).json()['items']

    if len(users) == 0:
        raise McmdError('Unknown user {}'.format(user_name))
    else:
        return map_to_user(users[0])


def get_role(role_name: str) -> Role:
    roles = get(api.rest2('sys_sec_Role'),
                params={
                    'attrs': 'id,name,label,group(id,name)',
                    'q': 'name=={}'.format(role_name)
                }).json()['items']

    if len(roles) == 0:
        raise McmdError('No role found with name {}'.format(role_name))
    else:
        return map_to_role(roles[0])


def get_roles(role_names: List[str]) -> List[Role]:
    role_names = [transform_role_name(name) for name in role_names]
    roles = get(api.rest2('sys_sec_Role'),
                params={
                    'attrs': 'id,name,label',
                    'q': 'name=in=({})'.format(','.join(role_names))
                }).json()['items']

    name_to_role = {role['name']: map_to_role(role) for role in roles}
    not_found = list()
    for role_name in role_names:
        if role_name not in name_to_role:
            not_found.append(role_name)

    if len(not_found) > 0:
        raise McmdError("Couldn't find role(s) {}".format(' and '.join(not_found)))
    else:
        return list(name_to_role.values())


def get_group(group_name: str) -> Group:
    group_name = transform_group_name(group_name)
    groups = get(api.rest2('sys_sec_Group'),
                 params={
                     'attrs': 'id,name',
                     'q': 'name=={}'.format(group_name)
                 }).json()['items']
    if len(groups) == 0:
        raise McmdError('No group found with name {}'.format(groups))
    else:
        return map_to_group(groups[0])


def get_group_membership(user: User, group: Group) -> Optional[RoleMembership]:
    group_roles = get_group_roles(group)
    group_role_ids = [role.id for role in group_roles]

    memberships = get(api.rest2('sys_sec_RoleMembership'),
                      params={
                          'attrs': 'id,user(id,username),role(id,name,label,group(id,name))',
                          'q': "user=={};role=in=({});(to=='',to=ge={})".format(user.id, ','.join(group_role_ids),
                                                                                timestamp())
                      }).json()['items']

    if len(memberships) == 0:
        return None
    else:
        return map_to_role_membership(memberships[0])


def add_user(username: str, email: str, password: str, change_password: bool, active: bool, superuser: bool):
    post(api.rest1('sys_sec_User'),
         data={'username': username,
               'Email': email,
               'password_': password,
               'changePassword': change_password,
               'active': active,
               'superuser': superuser
               })


def add_role(name: str, group: Optional[Group], includes: List[Role]):
    role_name = transform_role_name(name)
    new_role = {'name': role_name,
                'label': role_name}
    if group:
        new_role['group'] = group.id

    new_role['includes'] = [role.id for role in includes]

    data = {'entities': [new_role]}
    post(api.rest2('sys_sec_Role'), data=data)


def add_group(group_name: str):
    group_name = transform_group_name(group_name)
    post(api.group(), data={'name': group_name, 'label': group_name})


def add_group_membership(user: User, group: Group, role: Role):
    url = api.member(group.name)
    post(url, data={'username': user.username, 'roleName': role.name})


def update_group_membership(user: User, group: Group, role: Role):
    url = urljoin(api.member(group.name), user.username)
    put(url, data=json.dumps({'roleName': role.name}))


def add_role_membership(user: User, role: Role):
    """
    Adds a membership manually because the identities API can't add memberships to non-group roles.
    """
    membership = {'user': user.id,
                  'role': role.id,
                  'from': timestamp()}
    data = {'entities': [membership]}
    post(api.rest2('sys_sec_RoleMembership'), data=data)


def add_token(token: str, user: User):
    data = {'User': user.id,
            'token': token}

    post(api.rest1('sys_sec_Token'), data=data)


@version('8.1.0')
def include_group_role(role: Role, group_role: Role):
    if not group_role.group:
        raise McmdError('Role {} is not a group role'.format(group_role.name))
    if role.name == group_role.name:
        raise McmdError("A role can't include itself")

    include = {'role': group_role.name}
    put(api.role(group_role.group.name, role.name), data=json.dumps(include))


@version('7.0.0')
def transform_group_name(group_input: str):
    """Before 8.3.0 all group names are lower case."""
    return group_input.lower()


@version('8.3.0')
def transform_group_name(group_input: str):
    """Since 8.3.0 group names are case sensitive."""
    return group_input


@version('7.0.0')
def transform_role_name(role_input: str):
    """Before 8.3.0 all role names are upper case."""
    return role_input.upper()


@version('8.3.0')
def transform_role_name(role_input: str):
    """Since 8.3.0 role names are case sensitive."""
    return role_input
