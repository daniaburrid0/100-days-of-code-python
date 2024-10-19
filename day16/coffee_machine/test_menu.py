import pytest
from pathlib import Path
from menu import Menu
from drink import Drink

@pytest.fixture
def test_menu_file():
    return Path('data/test_menu_data.json')

@pytest.fixture
def menu(test_menu_file):
    return Menu(test_menu_file)

def test_menu_initialization(menu):
    assert len(menu) == 3
    assert "espresso" in menu.available_drinks
    assert "latte" in menu.available_drinks
    assert "cappuccino" in menu.available_drinks

def test_menu_iteration(menu):
    drinks = list(menu)
    assert len(drinks) == 3
    assert all(isinstance(drink, Drink) for drink in drinks)

def test_available_drinks(menu):
    available = menu.available_drinks
    assert "espresso" in available
    assert "latte" in available
    assert "cappuccino" in available
    assert len(available) == 3

def test_print_menu(menu, capsys):
    menu.print_menu()
    captured = capsys.readouterr()
    assert "Menú de Bebidas:" in captured.out
    assert "Espresso: $1.50" in captured.out
    assert "Latte: $2.50" in captured.out
    assert "Cappuccino: $3.00" in captured.out

def test_menu_from_file(test_menu_file):
    menu = Menu.from_file(test_menu_file)
    assert len(menu) == 3
    assert "espresso" in menu.available_drinks

def test_menu_with_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        Menu(Path('nonexistent_file.json'))

def test_menu_with_invalid_json(tmp_path):
    invalid_json = tmp_path / "invalid.json"
    invalid_json.write_text("{invalid json")
    with pytest.raises(ValueError):
        Menu(invalid_json)

def test_menu_with_empty_json(tmp_path):
    empty_json = tmp_path / "empty.json"
    empty_json.write_text("{}")
    menu = Menu(empty_json)
    assert len(menu) == 0  # Verifica que el menú está vacío
    assert menu.available_drinks == []

def test_menu_with_missing_keys(tmp_path):
    incomplete_json = tmp_path / "incomplete.json"
    incomplete_json.write_text('{"incomplete_drink": {"price": 1.0}}')
    menu = Menu(incomplete_json)
    assert len(menu) == 0  # No se debería cargar la bebida incompleta
