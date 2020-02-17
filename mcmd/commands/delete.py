import mcmd.io.ask
from mcmd.commands._registry import arguments
from mcmd.core.command import command
from mcmd.io import io
from mcmd.io.io import highlight
from mcmd.molgenis.model.system import EntityType, Package, SystemEntityType, Group
from mcmd.molgenis.resources import ResourceType
from mcmd.molgenis.service import resources, security


# =========
# Arguments
# =========


@arguments('delete')
def add_arguments(subparsers):
    p_delete = subparsers.add_parser('delete',
                                     help='delete resources')
    p_delete.set_defaults(func=delete,
                          write_to_history=True)
    p_delete_resource = p_delete.add_mutually_exclusive_group()
    p_delete_resource.add_argument('--entity-type', '-e',
                                   action='store_true',
                                   help='flag to specify that the resource is an entity type')
    p_delete_resource.add_argument('--package', '-p',
                                   action='store_true',
                                   help='flag to specify that the resource is a package')
    p_delete_resource.add_argument('--group', '-g',
                                   action='store_true',
                                   help='flag to specify that the resource is a group')

    p_delete_options = p_delete.add_mutually_exclusive_group()
    p_delete_options.add_argument('--data',
                                  action='store_true',
                                  help='use in conjunction with --entity-type to only delete the rows of the entity '
                                       'type')
    p_delete_options.add_argument('--attribute',
                                  metavar='NAME',
                                  type=str,
                                  help='use in conjunction with --entity-type to only delete an attribute of the '
                                       'entity type')
    p_delete_options.add_argument('--contents',
                                  action='store_true',
                                  help='use in conjunction with --package to only delete the contents of the package')

    p_delete.add_argument('--force', '-f',
                          action='store_true',
                          help='forces the delete action without asking for confirmation')
    p_delete.add_argument('resource',
                          type=str,
                          help='the identifier of the resource to delete')


# =======
# Methods
# =======


@command
def delete(args):
    resource = _get_resource(args)
    if isinstance(resource, EntityType):
        if args.data:
            _delete_entity_type_data(entity_type=resource, force=args.force)
        elif args.attribute:
            _delete_entity_type_attribute(entity_type=resource,
                                          attribute_name=args.attribute,
                                          force=args.force)
        else:
            _delete_entity_type(entity_type=resource, force=args.force)
    elif isinstance(resource, Package):
        if args.contents:
            _delete_package_contents(package=resource, force=args.force)
        else:
            _delete_package(package=resource, force=args.force)
    elif isinstance(resource, Group):
        _delete_group(group=resource, force=args.force)


def _delete_entity_type(entity_type: EntityType, force: bool):
    if force or (not force and mcmd.io.ask.confirm(
            'Are you sure you want to delete entity type {} including its data?'.format(entity_type.id))):
        io.start('Deleting entity type {}'.format(highlight(entity_type.id)))
        resources.delete_entity_type(entity_type)


def _delete_entity_type_data(entity_type: EntityType, force: bool):
    if force or (not force and mcmd.io.ask.confirm(
            'Are you sure you want to delete all data in entity type {}?'.format(entity_type.id))):
        io.start('Deleting all data from entity {}'.format(highlight(entity_type.id)))
        resources.delete_entity_type_data(entity_type)


def _delete_entity_type_attribute(entity_type: EntityType, attribute_name: str, force: bool):
    if force or (not force and mcmd.io.ask.confirm(
            'Are you sure you want to delete attribute {} of entity type {}?'.format(attribute_name, entity_type.id))):
        io.start('Deleting attribute {} of entity {}'.format(highlight(attribute_name), highlight(entity_type.id)))
        attribute = resources.get_attribute(entity_type, attribute_name)
        resources.delete_attribute(attribute)


def _delete_package(package: Package, force: bool):
    if force or (not force and mcmd.io.ask.confirm(
            'Are you sure you want to delete package {} and all of its contents?'.format(package.id))):
        io.start('Deleting package {}'.format(highlight(package.id)))
        resources.delete_package(package)


def _delete_package_contents(package: Package, force: bool):
    if force or (not force and mcmd.io.ask.confirm(
            'Are you sure you want to delete the contents of package {}?'.format(package.id))):
        io.start('Deleting contents of package {}'.format(highlight(package.id)))
        resources.delete_package_contents(package)


def _delete_group(group: Group, force: bool):
    if force or (not force and mcmd.io.ask.confirm(
            'Are you sure you want to delete group {}?'.format(group.name))):
        io.start('Deleting group {}'.format(highlight(group.name)))
        security.delete_group(group)


def _get_resource(args) -> SystemEntityType:
    resource_id = args.resource
    if args.entity_type:
        return resources.get_entity_type(resource_id)
    elif args.package:
        return resources.get_package(resource_id)
    elif args.group:
        return security.get_group(resource_id)
    else:
        entity_type = resources.get_entity_type_or_none(resource_id)
        package = resources.get_package_or_none(resource_id)
        group = security.get_group_or_none(resource_id)

        return resources.detect_resource_type(resource_id,
                                              [ResourceType.ENTITY_TYPE, ResourceType.PACKAGE, ResourceType.GROUP])
