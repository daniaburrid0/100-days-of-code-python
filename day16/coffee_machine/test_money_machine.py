import pytest
from decimal import Decimal
from unittest.mock import patch
from money_machine import MoneyMachine

@pytest.fixture
def money_machine():
    return MoneyMachine()

def test_initialization():
    mm = MoneyMachine()
    assert mm.profit == Decimal('0.00')

    mm = MoneyMachine(10.5)
    assert mm.profit == Decimal('10.50')

def test_initialization_with_negative_value():
    with pytest.raises(ValueError):
        MoneyMachine(-5)

def test_report(capsys, money_machine):
    money_machine.report()
    captured = capsys.readouterr()
    assert "Dinero recaudado: $0.00" in captured.out
    assert "Número de transacciones: 0" in captured.out
    assert "No se han realizado transacciones aún." in captured.out

@patch('builtins.input', side_effect=['2', '1', '1', '5'])
def test_process_coins(mock_input, money_machine):
    total = money_machine.process_coins()
    assert total == Decimal('0.70')

@patch('builtins.input', side_effect=['-1', '2', '1', '1', '5'])
def test_process_coins_with_negative_input(mock_input, capsys, money_machine):
    total = money_machine.process_coins()
    captured = capsys.readouterr()
    assert "Error: El número de monedas no puede ser negativo." in captured.out
    assert total == Decimal('0.70')

def test_make_payment_sufficient(money_machine):
    with patch.object(money_machine, 'process_coins', return_value=Decimal('3.00')):
        assert money_machine.make_payment(2.5) == True
        assert money_machine.profit == Decimal('2.50')

def test_make_payment_insufficient(money_machine, capsys):
    with patch.object(money_machine, 'process_coins', return_value=Decimal('1.00')):
        assert money_machine.make_payment(2.5) == False
        captured = capsys.readouterr()
        assert "Lo siento, eso no es suficiente dinero." in captured.out
        assert money_machine.profit == Decimal('0.00')

def test_make_payment_exact(money_machine):
    with patch.object(money_machine, 'process_coins', return_value=Decimal('2.50')):
        assert money_machine.make_payment(2.5) == True
        assert money_machine.profit == Decimal('2.50')

def test_make_payment_with_change(money_machine, capsys):
    with patch.object(money_machine, 'process_coins', return_value=Decimal('3.00')):
        assert money_machine.make_payment(2.5) == True
        captured = capsys.readouterr()
        assert "Aquí está su cambio: $0.50" in captured.out
        assert money_machine.profit == Decimal('2.50')

def test_make_payment_negative_cost():
    mm = MoneyMachine()
    with pytest.raises(ValueError):
        mm.make_payment(-1)

def test_str_representation(money_machine):
    assert str(money_machine) == "MoneyMachine(profit=$0.00, transactions=0)"

def test_repr_representation(money_machine):
    assert repr(money_machine).startswith("MoneyMachine(profit=0.00, transactions=0, coin_values=")
