from typing import Optional

from mcmd.core.errors import McmdError
from mcmd.molgenis.model.system import EntityType, Package, Attribute
from mcmd.molgenis.service._client import api
from mcmd.molgenis.service._client.client import get, post, delete, delete_data
from mcmd.molgenis.service._client.rest_api_v2_mapper import map_to_package


def get_entity_type(id_: str) -> EntityType:
    entity_type = get_entity_type_or_none(id_)
    if not entity_type:
        raise McmdError("EntityType with id {} not found")
    else:
        return entity_type


def get_entity_type_or_none(id_: str) -> Optional[EntityType]:
    entity_types = get(api.rest2(EntityType.meta.id),
                       params={
                           'attrs': 'id',
                           'q': 'id==' + id_
                       }).json()['items']
    if len(entity_types) == 0:
        return None
    else:
        return entity_types[0]


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


def get_attribute(entity_type: EntityType, attribute_name: str) -> Attribute:
    raise NotImplementedError()


def add_package(id_: str, parent: Optional[Package]):
    data = {'id': id_,
            'label': id_}

    if parent:
        data['parent'] = parent.id

    post(api.rest1(Package.meta.id), data=data)


def delete_entity_type(entity_type: EntityType):
    delete_data(api.rest2(EntityType.meta.id), entity_type.id)


def delete_entity_type_data(entity_type: EntityType):
    delete(api.rest1(entity_type.id))


def delete_attribute(attribute: Attribute):
    delete(api.rest2('{}/{}'.format(Attribute.meta.id, attribute)))


def delete_package(package: Package):
    delete_data(api.rest2(Package.meta.id), package.id)


def delete_package_contents(package: Package):
    _delete_entity_types_in_package(package)
    _delete_packages_in_package(package)


def _delete_entity_types_in_package(package: Package):
    entity_types = get(api.rest2(EntityType.meta.id),
                       params={
                           'attrs': 'id',
                           'q': 'package==' + package.id
                       }).json()['items']
    entity_ids = [entity_type['id'] for entity_type in entity_types]
    if len(entity_ids) > 0:
        delete_data(api.rest2(EntityType.meta.id), entity_ids)


def _delete_packages_in_package(package_id):
    packages = get(api.rest2(Package.meta.id),
                   params={
                       'attrs': 'id',
                       'q': 'parent==' + package_id
                   }).json()['items']
    package_ids = [entity_type['id'] for entity_type in packages]
    if len(package_ids) > 0:
        delete_data(Package.meta.id, package_ids)
