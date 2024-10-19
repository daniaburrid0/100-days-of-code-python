import pytest
from resource_manager import ResourceManager, ResourceType

@pytest.fixture
def resource_manager():
    initial_resources = {
        ResourceType.WATER: 300,
        ResourceType.MILK: 200,
        ResourceType.COFFEE: 100
    }
    return ResourceManager(initial_resources)

def test_initialization(resource_manager):
    resources = resource_manager.get_resources()
    assert resources[ResourceType.WATER] == 300
    assert resources[ResourceType.MILK] == 200
    assert resources[ResourceType.COFFEE] == 100

def test_check_resources_sufficient(resource_manager):
    required_resources = {
        ResourceType.WATER: 50,
        ResourceType.MILK: 30,
        ResourceType.COFFEE: 15
    }
    assert resource_manager.check_resources(required_resources) is None

def test_check_resources_insufficient(resource_manager):
    required_resources = {
        ResourceType.WATER: 350,
        ResourceType.MILK: 30,
        ResourceType.COFFEE: 15
    }
    assert resource_manager.check_resources(required_resources) == ResourceType.WATER

def test_deduct_resources(resource_manager):
    used_resources = {
        ResourceType.WATER: 50,
        ResourceType.MILK: 30,
        ResourceType.COFFEE: 15
    }
    resource_manager.deduct_resources(used_resources)
    resources = resource_manager.get_resources()
    assert resources[ResourceType.WATER] == 250
    assert resources[ResourceType.MILK] == 170
    assert resources[ResourceType.COFFEE] == 85

def test_deduct_resources_insufficient(resource_manager):
    used_resources = {
        ResourceType.WATER: 350,
        ResourceType.MILK: 30,
        ResourceType.COFFEE: 15
    }
    with pytest.raises(ValueError):
        resource_manager.deduct_resources(used_resources)

def test_add_resources(resource_manager):
    added_resources = {
        ResourceType.WATER: 100,
        ResourceType.MILK: 50,
        ResourceType.COFFEE: 25
    }
    resource_manager.add_resources(added_resources)
    resources = resource_manager.get_resources()
    assert resources[ResourceType.WATER] == 400
    assert resources[ResourceType.MILK] == 250
    assert resources[ResourceType.COFFEE] == 125

def test_add_resources_negative(resource_manager):
    added_resources = {
        ResourceType.WATER: -50
    }
    with pytest.raises(ValueError):
        resource_manager.add_resources(added_resources)

def test_has_resource(resource_manager):
    assert resource_manager.has_resource(ResourceType.WATER) is True
    assert resource_manager.has_resource(ResourceType.MILK) is True
    assert resource_manager.has_resource(ResourceType.COFFEE) is True

def test_print_report(resource_manager, capsys):
    resource_manager.print_report()
    captured = capsys.readouterr()
    assert "Water: 300ml" in captured.out
    assert "Milk: 200ml" in captured.out
    assert "Coffee: 100g" in captured.out

def test_str_representation(resource_manager):
    str_repr = str(resource_manager)
    assert "Water: 300ml" in str_repr
    assert "Milk: 200ml" in str_repr
    assert "Coffee: 100g" in str_repr

def test_repr_representation(resource_manager):
    repr_str = repr(resource_manager)
    assert "ResourceManager" in repr_str
    assert "'WATER': 300" in repr_str
    assert "'MILK': 200" in repr_str
    assert "'COFFEE': 100" in repr_str
