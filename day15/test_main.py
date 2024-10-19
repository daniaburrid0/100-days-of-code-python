import unittest
from unittest.mock import patch
from io import StringIO
import sys

# Importa las funciones y constantes necesarias de tu script principal
from my_main import (
    MENU, RESOURCES, prompt_user, process_command, check_resources,
    process_coins, check_transaction, make_coffee, print_report
)

class TestCoffeeMachine(unittest.TestCase):

    def setUp(self):
        global RESOURCES
        RESOURCES = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
        }

    @patch('builtins.input', return_value='espresso')
    def test_prompt_user(self, mock_input):
        self.assertEqual(prompt_user(), 'espresso')

    @patch('builtins.input', return_value='invalid')
    def test_prompt_user_invalid(self, mock_input):
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', side_effect=['invalid', 'latte']):
                self.assertEqual(prompt_user(), 'latte')
                mock_print.assert_called_with("Opción no válida. Por favor, intente de nuevo.")

    def test_check_resources_sufficient(self):
        self.assertTrue(check_resources('espresso'))

    def test_check_resources_insufficient(self):
        global RESOURCES
        RESOURCES['water'] = 30
        self.assertFalse(check_resources('espresso'))

    @patch('builtins.input', side_effect=['2', '1', '1', '1'])
    def test_process_coins(self, mock_input):
        self.assertAlmostEqual(process_coins(), 0.66, places=2)

    def test_check_transaction_sufficient(self):
        self.assertTrue(check_transaction('espresso', 2.0))

    def test_check_transaction_insufficient(self):
        self.assertFalse(check_transaction('espresso', 1.0))

    def test_make_coffee(self):
        initial_water = RESOURCES['water']
        initial_coffee = RESOURCES['coffee']
        make_coffee('espresso')
        self.assertEqual(RESOURCES['water'], initial_water - MENU['espresso']['ingredients']['water'])
        self.assertEqual(RESOURCES['coffee'], initial_coffee - MENU['espresso']['ingredients']['coffee'])

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_report(self):
        global RESOURCES
        RESOURCES = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
        }
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            print_report(5.5)
            output = mock_stdout.getvalue()
            self.assertIn("Agua  :  300 ml", output)
            self.assertIn("Leche :  200 ml", output)
            self.assertIn("Café  :  100 g", output)
            self.assertIn("Dinero: $5.50", output)

    @patch('builtins.input', return_value='espresso')
    @patch('my_main.process_coins', return_value=2.0)
    def test_process_command_espresso(self, mock_coins, mock_input):
        continue_running, money = process_command('espresso', 0)
        self.assertTrue(continue_running)
        self.assertEqual(money, 1.5)

    def test_process_command_off(self):
        continue_running, money = process_command('off', 0)
        self.assertFalse(continue_running)

if __name__ == '__main__':
    unittest.main()
