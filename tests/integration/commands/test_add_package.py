import pytest

from mcmd.molgenis.model.system import Package
from tests.integration.utils import run_commander, random_name


@pytest.mark.integration
def test_add_package(session):
    name = random_name()
    run_commander('add package {}'.format(name))

    package = session.get_by_id(Package.meta.id, name)
    assert 'parent' not in package


@pytest.mark.integration
def test_add_package_in_package(session):
    name1 = random_name()
    name2 = random_name()
    run_commander('add package {}'.format(name1))
    run_commander('add package {} --in {}'.format(name2, name1))

    package = session.get_by_id(Package.meta.id, name2, expand=['parent'])
    assert package['parent']['id'] == name1
