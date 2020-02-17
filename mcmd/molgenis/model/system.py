"""
Contains bare-bones definitions of System Entity Types of MOLGENIS.
"""
from typing import NamedTuple, Optional


class Principal:
    pass


class PermissableResource:
    pass


class Meta(NamedTuple):
    id: str
    name: str


class SystemEntityType(NamedTuple):
    meta: Meta


class Group(SystemEntityType):
    id: str
    name: str

    meta = Meta(id='sys_sec_Group',
                name='Group')


class User(SystemEntityType, Principal):
    id: str
    username: str

    meta = Meta(id='sys_sec_User',
                name='User')


class Role(SystemEntityType, Principal):
    id: str
    name: str
    label: str
    group: Optional[Group]

    meta = Meta(id='sys_sec_Role',
                name='Role')


class RoleMembership(SystemEntityType):
    id: str
    user: User
    role: Role

    meta = Meta(id='sys_sec_RoleMembership',
                name='RoleMembership')


class EntityType(SystemEntityType, PermissableResource):
    id: str

    meta = Meta(id='sys_md_EntityType',
                name='EntityType')


class Attribute(SystemEntityType):
    id: str
    name: str

    meta = Meta(id='sys_md_Attribute',
                name='Attribute')


class Package:
    # forward declaration so Package can reference itself
    pass


# noinspection PyRedeclaration
class Package(SystemEntityType, PermissableResource):
    id: str
    parent: Optional[Package]

    meta = Meta(id='sys_md_Package',
                name='Package')


class Plugin(SystemEntityType, PermissableResource):
    id: str

    meta = Meta(id='sys_Plugin',
                name='Plugin')


class Entity(NamedTuple, PermissableResource):
    id: str
    entity_type: EntityType
