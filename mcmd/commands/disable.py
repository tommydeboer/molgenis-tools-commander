from mcmd import io
from mcmd.molgenis import api
from mcmd.molgenis.client import post, put
from mcmd.command import command
from mcmd.commands._registry import arguments
from mcmd.io import highlight
from mcmd.molgenis.resources import ensure_resource_exists, ResourceType


# =========
# Arguments
# =========

@arguments('disable')
def add_arguments(subparsers):
    p_disable = subparsers.add_parser('disable',
                                      help='Disable resources/functionality',
                                      description="Run 'mcmd disable rls -h' to view the help for those sub-commands")
    p_disable_subparsers = p_disable.add_subparsers(dest="type")

    p_disable_rls = p_disable_subparsers.add_parser('rls',
                                                    help='Disables row level security on an entity type')
    p_disable_rls.set_defaults(func=disable_rls,
                               write_to_history=True)
    p_disable_rls.add_argument('entity',
                               type=str,
                               help="The entity type to remove the row level security from")

    p_disable_language = p_disable_subparsers.add_parser('language',
                                                         help='Enables a language')
    p_disable_language.set_defaults(func=disable_language,
                                    write_to_history=True)
    p_disable_language.add_argument('language',
                                    type=str,
                                    help="the language you want to disable, specified by the two letter code (e.g. "
                                         "'en')")


# =======
# Methods
# =======

@command
def disable_rls(args):
    if not io.confirm('Are you sure you want to disable row level security on %s?' % args.entity):
        return

    io.start('Disabling row level security on entity type %s' % highlight(args.entity))

    ensure_resource_exists(args.entity, ResourceType.ENTITY_TYPE)
    post(api.rls(), data={'id': args.entity,
                          'rlsEnabled': False})


@command
def disable_language(args):
    io.start('Disabling language {}'.format(highlight(args.language)))
    url = api.rest1('sys_Language/{}/active'.format(args.language))
    put(url, 'false')
