from urllib.parse import urljoin

from mcmd.molgenis.service._client import api
from mcmd.molgenis.service._client.client import post_form
from mcmd.molgenis.service.permissions import Permission
from mcmd.molgenis.model.system import User, Role, EntityType, Package, Plugin


def grant_user_entity_type_permission(user: User, permission: Permission, entity_type: EntityType):
    data = {'radio-' + entity_type.id: permission.value(),
            'username': user.username}
    _grant(data, 'entityclass', 'user')


def grant_user_package_permission(user: User, permission: Permission, package: Package):
    data = {'radio-' + package.id: permission.value(),
            'username': user.username}
    _grant(data, 'package', 'user')


def grant_user_plugin_permission(user: User, permission: Permission, plugin: Plugin):
    data = {'radio-' + plugin.id: permission.value(),
            'username': user.username}
    _grant(data, 'plugin', 'user')


def grant_role_entity_type_permission(role: Role, permission: Permission, entity_type: EntityType):
    data = {'radio-' + entity_type.id: permission.value(),
            'rolename': role.name}
    _grant(data, 'entityclass', 'user')


def grant_role_package_permission(role: Role, permission: Permission, package: Package):
    data = {'radio-' + package.id: permission.value(),
            'rolename': role.name}
    _grant(data, 'package', 'user')


def grant_role_plugin_permission(role: Role, permission: Permission, plugin: Plugin):
    data = {'radio-' + plugin.id: permission.value(),
            'rolename': role.name}
    _grant(data, 'plugin', 'user')


def _grant(data: dict, resource_name: str, principal_name: str):
    url = urljoin(api.permissions(), '{}/{}'.format(resource_name, principal_name))
    post_form(url, data)
