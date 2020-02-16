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


class Group(NamedTuple):
    id: str
    name: str

    meta = Meta(id='sys_sec_Group',
                name='Group')


class User(NamedTuple, Principal):
    id: str
    username: str

    meta = Meta(id='sys_sec_User',
                name='User')


class Role(NamedTuple, Principal):
    id: str
    name: str
    label: str
    group: Optional[Group]

    meta = Meta(id='sys_sec_Role',
                name='Role')


class RoleMembership(NamedTuple):
    id: str
    user: User
    role: Role

    meta = Meta(id='sys_sec_RoleMembership',
                name='RoleMembership')


class EntityType(NamedTuple, PermissableResource):
    id: str

    meta = Meta(id='sys_md_EntityType',
                name='EntityType')


class Package(NamedTuple, PermissableResource):
    id: str

    meta = Meta(id='sys_md_Package',
                name='Package')


class Plugin(NamedTuple, PermissableResource):
    id: str

    meta = Meta(id='sys_Plugin',
                name='Plugin')


class Entity(NamedTuple, PermissableResource):
    id: str
    entity_type: EntityType