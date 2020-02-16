from enum import Enum

from mcmd.molgenis.service._client import permission_manager
from mcmd.molgenis.model.system import User, Role, Principal, PermissableResource, EntityType, Package, Plugin, Entity


class Permission(Enum):
    COUNT = 'count',
    READ_META = 'readmeta'
    READ = 'read',
    WRITE = 'write'
    WRITEMETA = 'writemeta'


def give_permission(principal: Principal, permission: Permission, resource: PermissableResource):
    if isinstance(principal, User):
        if isinstance(resource, EntityType):
            give_user_entity_type_permission(principal, permission, resource)
        elif isinstance(resource, Package):
            give_user_package_permission(principal, permission, resource)
        elif isinstance(resource, Plugin):
            give_user_plugin_permission(principal, permission, resource)
        elif isinstance(resource, Entity):
            give_user_entity_permission(principal, permission, resource)
        else:
            raise ValueError('unknown PermissableResource type')
    elif isinstance(principal, Role):
        if isinstance(resource, EntityType):
            give_role_entity_type_permission(principal, permission, resource)
        elif isinstance(resource, Package):
            give_role_package_permission(principal, permission, resource)
        elif isinstance(resource, Plugin):
            give_role_plugin_permission(principal, permission, resource)
        elif isinstance(resource, Entity):
            give_role_entity_permission(principal, permission, resource)
        else:
            raise ValueError('unknown PermissableResource type')
    else:
        raise ValueError('unknown Principal type')


def give_user_entity_type_permission(user: User, permission: Permission, entity_type: EntityType):
    permission_manager.grant_user_entity_type_permission(user, permission, entity_type)


def give_user_package_permission(user: User, permission: Permission, package: Package):
    permission_manager.grant_user_package_permission(user, permission, package)


def give_user_plugin_permission(user: User, permission: Permission, plugin: Plugin):
    permission_manager.grant_user_plugin_permission(user, permission, plugin)


# noinspection PyUnusedLocal
def give_user_entity_permission(user: User, permission: Permission, entity: Entity):
    raise NotImplementedError('row level permissions not yet implemented')


def give_role_entity_type_permission(role: Role, permission: Permission, entity_type: EntityType):
    permission_manager.grant_role_entity_type_permission(role, permission, entity_type)


def give_role_package_permission(role: Role, permission: Permission, package: Package):
    permission_manager.grant_role_package_permission(role, permission, package)


def give_role_plugin_permission(role: Role, permission: Permission, plugin: Plugin):
    permission_manager.grant_role_plugin_permission(role, permission, plugin)


# noinspection PyUnusedLocal
def give_role_entity_permission(role: Role, permission: Permission, entity: Entity):
    raise NotImplementedError('row level permissions not yet implemented')
