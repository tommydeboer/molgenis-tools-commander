from typing import Optional

from mcmd.core.errors import McmdError
from mcmd.molgenis.model.system import EntityType, Package, Attribute
from mcmd.molgenis.service._client import api
from mcmd.molgenis.service._client.client import get, post, delete
from mcmd.molgenis.service._client.rest_api_v2_mapper import map_to_package


def get_entity_type(id: str) -> EntityType:
    pass


def get_package(id_: str) -> Package:
    package = get_package_or_none(id_)
    if not package:
        raise McmdError('Package with id {} not found'.format(id_))
    else:
        return package


def get_package_or_none(id_: str) -> Optional[Package]:
    packages = get(api.rest2(Package.meta.id),
                   params={
                       'attrs': 'id,parent(id)',
                       'q': 'id==' + id_
                   }).json()['items']
    if len(packages) == 0:
        return None
    else:
        return map_to_package(packages[0])


def get_attribute(entity_type_id: str, attribute_name: str) -> Attribute:
    pass


def add_package(id_: str, parent: Optional[Package]):
    data = {'id': id_,
            'label': id_}

    if parent:
        data['parent'] = parent.id

    post(api.rest1(Package.meta.id), data=data)


def delete_entity_type_data(entity_type_id: str):
    delete(api.rest1(entity_type_id))
