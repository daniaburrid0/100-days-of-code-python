
import pytest
from coffee_machine import CoffeeMachine, Command, InsufficientResourcesError, InvalidDrinkError
from menu import Menu
from resource_manager import ResourceManager, ResourceType
from money_machine import MoneyMachine
from unittest.mock import Mock, patch
import json

@pytest.fixture
def mock_resource_manager():
    resource_manager = Mock(spec=ResourceManager)
    resource_manager.get_resource = Mock(return_value=300)
    resource_manager.set_resource = Mock()
    resource_manager.get_capacity = Mock(return_value=500)
    resource_manager.use_resource = Mock()  # Añade esta línea
    return resource_manager

@pytest.fixture
def mock_money_machine():
    money_machine = Mock(spec=MoneyMachine)
    money_machine.make_payment = Mock(return_value=True)
    money_machine.get_earnings = Mock(return_value=10.0)
    money_machine.process_coins = Mock(return_value=3.0)
    money_machine.set_earnings = Mock()  # Añade esta línea
    return money_machine

@pytest.fixture
def mock_menu():
    menu = Mock(spec=Menu)
    menu.find_drink = Mock(return_value=Mock(name="latte", ingredients={"water": 200, "milk": 150, "coffee": 24}, cost=2.5))
    menu.get_drinks = Mock(return_value=[
        Mock(name="espresso", ingredients={"water": 50, "coffee": 18}),
        Mock(name="latte", ingredients={"water": 200, "milk": 150, "coffee": 24})
    ])
    return menu

@pytest.fixture
def coffee_machine(mock_menu, mock_resource_manager, mock_money_machine):
    return CoffeeMachine(mock_menu, mock_resource_manager, mock_money_machine)

def test_coffee_machine_initialization(coffee_machine):
    assert isinstance(coffee_machine.menu, Menu)
    assert isinstance(coffee_machine.resource_manager, ResourceManager)
    assert isinstance(coffee_machine.money_machine, MoneyMachine)

def test_process_selection_valid_drink(coffee_machine):
    with patch.object(coffee_machine, 'process_payment', return_value=True):
        with patch.object(coffee_machine, 'make_coffee') as mock_make_coffee:
            coffee_machine.process_selection("latte")
            mock_make_coffee.assert_called_once_with("latte")

def test_process_selection_invalid_drink(coffee_machine):
    coffee_machine.menu.find_drink.return_value = None
    with pytest.raises(InvalidDrinkError):
        coffee_machine.process_selection("invalid_drink")

def test_check_resources_sufficient(coffee_machine):
    assert coffee_machine.check_resources("latte") is None

def test_check_resources_insufficient(coffee_machine):
    coffee_machine.resource_manager.get_resource.return_value = 50
    assert coffee_machine.check_resources("latte") == ResourceType.WATER

def test_process_payment_successful(coffee_machine):
    assert coffee_machine.process_payment("latte") is True

def test_process_payment_insufficient(coffee_machine):
    coffee_machine.money_machine.make_payment.return_value = False
    assert coffee_machine.process_payment("latte") is False

def test_make_coffee(coffee_machine):
    with patch('time.sleep'):  # Mock time.sleep to speed up test
        coffee_machine.make_coffee("latte")
        coffee_machine.resource_manager.use_resource.assert_called()

def test_print_report(coffee_machine, capsys):
    coffee_machine.print_report()
    captured = capsys.readouterr()
    assert "Informe de la Máquina de Café" in captured.out

def test_refill_resources(coffee_machine):
    resources_to_add = {ResourceType.WATER: 500, ResourceType.COFFEE: 100}
    coffee_machine.refill_resources(resources_to_add)
    coffee_machine.resource_manager.set_resource.assert_called()

def test_get_status(coffee_machine):
    status = coffee_machine.get_status()
    assert "resources" in status
    assert "earnings" in status

@patch('builtins.open')
def test_save_state(mock_open, coffee_machine):
    coffee_machine.save_state()
    mock_open.assert_called_once_with("coffee_machine_state.json", 'w')

@patch('builtins.open')
@patch('json.load')
def test_load_state(mock_json_load, mock_open, coffee_machine):
    mock_json_load.return_value = {"resources": {"water": 300}, "earnings": 10.0}
    coffee_machine.load_state()
    mock_open.assert_called_once_with("coffee_machine_state.json", 'r')
    coffee_machine.resource_manager.set_resource.assert_called()
    coffee_machine.money_machine.set_earnings.assert_called_with(10.0)

def test_error_logging(coffee_machine):
    with patch('coffee_machine.CoffeeMachine._log_error') as mock_log_error:
        with pytest.raises(Exception):
            with coffee_machine.error_logging():
                raise Exception("Test error")
        mock_log_error.assert_called_once()

def test_handle_error(coffee_machine, capsys):
    error = InvalidDrinkError("Test error")
    coffee_machine.handle_error(error)
    captured = capsys.readouterr()
    assert "Se ha seleccionado una bebida inválida" in captured.out

def test_maintenance_mode(coffee_machine, capsys):
    coffee_machine.maintenance_mode()
    captured = capsys.readouterr()
    assert "Entrando en modo de mantenimiento" in captured.out

def test_check_low_resources(coffee_machine):
    with patch.object(coffee_machine.resource_manager, 'get_resource', return_value=50):
        with patch.object(coffee_machine.resource_manager, 'get_capacity', return_value=300):
            coffee_machine.check_low_resources()
            # Aquí podrías agregar una aserción para verificar si se imprimió una advertencia

def test_calculate_possible_drinks(coffee_machine):
    espresso = Mock(name="espresso")
    espresso.name = "espresso"
    espresso.ingredients = {"water": 50, "coffee": 18}
    latte = Mock(name="latte")
    latte.name = "latte"
    latte.ingredients = {"water": 200, "milk": 150, "coffee": 24}
    coffee_machine.menu.get_drinks.return_value = [espresso, latte]
    possible_drinks = coffee_machine.calculate_possible_drinks()
    assert "espresso" in possible_drinks
    assert "latte" in possible_drinks
