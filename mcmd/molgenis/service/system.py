"""
Contains bare-bones definitions of System Entity Types of MOLGENIS.
"""
from typing import NamedTuple, Optional


class Meta(NamedTuple):
    name: str


class Group(NamedTuple):
    id: str
    name: str
    meta = Meta(name='Group')


class Principal:
    # TODO move id and (user)name vars to this class
    pass


class User(Principal, NamedTuple):
    id: str
    username: str
    meta = Meta(name='User')


class Role(Principal, NamedTuple):
    id: str
    name: str
    label: str
    group: Optional[Group]
    meta = Meta(name='Role')


class RoleMembership(NamedTuple):
    id: str
    user: User
    role: Role
    meta = Meta(name='RoleMembership')
