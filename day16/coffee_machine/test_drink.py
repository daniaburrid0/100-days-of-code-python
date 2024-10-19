# test_drink.py

import pytest
from drink import Drink

@pytest.fixture
def sample_drink():
    return Drink("latte", {"water": 200, "milk": 150, "coffee": 24}, 2.5)

def test_drink_initialization(sample_drink):
    assert sample_drink.name == "latte"
    assert sample_drink.ingredients == {"water": 200, "milk": 150, "coffee": 24}
    assert sample_drink.price == 2.5

def test_drink_str_representation(sample_drink):
    assert str(sample_drink) == "Latte: $2.50"

def test_drink_repr_representation(sample_drink):
    expected_repr = "Drink(name='latte', ingredients={'water': 200, 'milk': 150, 'coffee': 24}, price=2.5)"
    assert repr(sample_drink) == expected_repr

def test_drink_properties_are_read_only(sample_drink):
    with pytest.raises(AttributeError):
        sample_drink.name = "espresso"
    with pytest.raises(AttributeError):
        sample_drink.price = 3.0

def test_ingredients_property_returns_copy(sample_drink):
    ingredients = sample_drink.ingredients
    ingredients["water"] = 300
    assert sample_drink.ingredients["water"] == 200

def test_drink_with_different_values():
    espresso = Drink("espresso", {"water": 50, "coffee": 18}, 1.5)
    assert espresso.name == "espresso"
    assert espresso.ingredients == {"water": 50, "coffee": 18}
    assert espresso.price == 1.5
    assert str(espresso) == "Espresso: $1.50"

def test_drink_with_empty_ingredients():
    with pytest.raises(ValueError):
        Drink("water", {}, 1.0)

def test_drink_with_negative_price():
    with pytest.raises(ValueError):
        Drink("tea", {"water": 200}, -1.0)
