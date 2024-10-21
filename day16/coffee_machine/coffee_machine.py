from typing import Dict, Optional
from enum import Enum
from menu import Menu
from resource_manager import ResourceManager, ResourceType
from money_machine import MoneyMachine
from contextlib import contextmanager
from decimal import Decimal, ROUND_HALF_UP
import json
import time
from datetime import datetime

class Command(Enum):
    OFF = "off"
    REPORT = "report"
    MAINTENANCE = "maintenance"

class InsufficientResourcesError(Exception):
    def __init__(self, resource: str, required: int, available: int):
        self.resource = resource
        self.required = required
        self.available = available
        super().__init__(f"Recurso insuficiente: {resource}. Requerido: {required}, Disponible: {available}")

class InvalidDrinkError(Exception):
    def __init__(self, drink_name: str):
        self.drink_name = drink_name
        super().__init__(f"Bebida inválida: {drink_name}")

class CoffeeMachine:
    """Representa una máquina de café que integra menú, recursos y transacciones."""

    def __init__(self, menu: Menu, resource_manager: ResourceManager, money_machine: MoneyMachine) -> None:
        """
        Inicializa la máquina de café con sus componentes.

        Args:
            menu: Instancia de Menu.
            resource_manager: Instancia de ResourceManager.
            money_machine: Instancia de MoneyMachine.
        """
        self.menu = menu
        self.resource_manager = resource_manager
        self.money_machine = money_machine
        self.COMMANDS = {
            Command.OFF.value: lambda: self.shutdown(),
            Command.REPORT.value: lambda: self.print_report(),
            Command.MAINTENANCE.value: lambda: self.maintenance_mode(),
        }

    @contextmanager
    def error_logging(self):
        try:
            yield
        except Exception as e:
            self._log_error(type(e).__name__, str(e))
            raise

    def start(self) -> None:
        """Inicia el funcionamiento de la máquina de café."""
        while True:
            try:
                user_input = input("¿Qué le gustaría? (espresso/latte/cappuccino): ").lower().strip()

                if user_input in self.COMMANDS:
                    self.COMMANDS[user_input]()
                    if user_input == Command.OFF.value:
                        break
                elif self.menu.find_drink(user_input):
                    self.process_selection(user_input)
                else:
                    print("Lo siento, esa opción no es válida. Por favor, intente de nuevo.")
            except KeyboardInterrupt:
                print("\nOperación cancelada por el usuario.")
                self.shutdown()
                break
            except Exception as e:
                self.handle_error(e)

    def process_selection(self, selection: str) -> None:
        """
        Procesa la selección del usuario.

        Args:
            selection: La selección del usuario (bebida o comando).
        """
        with self.error_logging():
            drink = self.menu.find_drink(selection)
            if not drink:
                raise InvalidDrinkError(f"Bebida '{selection}' no encontrada en el menú.")

            missing_resource = self.check_resources(selection)
            if missing_resource:
                raise InsufficientResourcesError(f"No hay suficiente {missing_resource.value}.")

            if not self.process_payment(selection):
                print("Pago insuficiente. Operación cancelada.")
                return

            self.make_coffee(selection)
            print(f"¡Aquí tiene su {selection}! Disfrútelo.")
            self.check_low_resources()

    def check_resources(self, drink_name: str) -> Optional[ResourceType]:
        """
        Verifica la disponibilidad de recursos para una bebida.

        Args:
            drink_name: Nombre de la bebida seleccionada.

        Returns:
            ResourceType faltante si no hay suficientes recursos, None si hay suficientes.
        """
        drink = self.menu.find_drink(drink_name)
        if not drink:
            raise InvalidDrinkError(f"Bebida '{drink_name}' no encontrada en el menú.")

        for ingredient, amount in drink.ingredients.items():
            resource_type = ResourceType(ingredient)
            available = self.resource_manager.get_resource(resource_type)
            if available < amount:
                return resource_type

        return None

    def process_payment(self, drink_name: str) -> bool:
        drink = self.menu.find_drink(drink_name)
        if not drink:
            raise InvalidDrinkError(f"Bebida '{drink_name}' no encontrada en el menú.")

        cost = Decimal(str(drink.cost)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        print(f"El costo de {drink_name} es ${cost:.2f}.")
        print("Por favor, inserte monedas.")

        try:
            payment = self.money_machine.process_coins()
            if payment < cost:
                print(f"Lo siento, eso no es suficiente dinero. ${payment:.2f} devuelto.")
                return False

            change = self._calculate_change(payment, cost)
            self._handle_change(change)

            self.money_machine.add_money(float(cost))
            return True
        except Exception as e:
            print(f"Error al procesar el pago: {str(e)}")
            return False

    def _calculate_change(self, payment: Decimal, cost: Decimal) -> Decimal:
        return (payment - cost).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def _handle_change(self, change: float) -> None:
        if change > 0:
            print(f"Aquí está ${change:.2f} en cambio.")

    def make_coffee(self, drink_name: str) -> None:
        drink = self.menu.find_drink(drink_name)
        if not drink:
            raise InvalidDrinkError(f"Bebida '{drink_name}' no encontrada en el menú.")

        try:
            for ingredient, amount in drink.ingredients.items():
                resource_type = ResourceType(ingredient)
                self.resource_manager.use_resource(resource_type, amount)
        except ValueError as e:
            raise RuntimeError(f"Error al preparar {drink_name}: {str(e)}")

        print(f"Preparando {drink_name}...")
        time.sleep(2)
        print(f"{drink_name} está listo.")

    def print_report(self) -> None:
        """Imprime un informe del estado actual de la máquina."""
        print("--- Informe de la Máquina de Café ---")
        self._print_resource_report()
        self._print_financial_report()

    def _print_resource_report(self) -> None:
        """Imprime el informe de recursos disponibles."""
        try:
            for resource_type in ResourceType:
                amount = self.resource_manager.get_resource(resource_type)
                unit = "ml" if resource_type in [ResourceType.WATER, ResourceType.MILK] else "g"
                print(f"{resource_type.value.capitalize()}: {amount}{unit}")
        except Exception as e:
            print(f"Error al obtener informe de recursos: {str(e)}")

    def _print_financial_report(self) -> None:
        """Imprime el informe financiero."""
        try:
            earnings = self.money_machine.get_earnings()
            print(f"Ganancias: ${earnings:.2f}")
        except Exception as e:
            print(f"Error al obtener informe financiero: {str(e)}")

    def refill_resources(self, resources: Dict[ResourceType, int]) -> None:
        """
        Reabastece los recursos de la máquina.

        Args:
            resources: Diccionario de recursos a añadir.
        """
        for resource_type, amount in resources.items():
            try:
                if not isinstance(resource_type, ResourceType):
                    raise ValueError(f"Tipo de recurso inválido: {resource_type}")
                if amount <= 0:
                    raise ValueError(f"Cantidad inválida para {resource_type.value}: {amount}")

                current_amount = self.resource_manager.get_resource(resource_type)
                new_amount = current_amount + amount
                self.resource_manager.set_resource(resource_type, new_amount)
                print(f"{resource_type.value.capitalize()} reabastecido: +{amount}")
            except ValueError as e:
                print(f"Error al reabastecer {resource_type.value}: {str(e)}")
            except Exception as e:
                print(f"Error inesperado al reabastecer {resource_type.value}: {str(e)}")

        print("Reabastecimiento completado.")

    def get_status(self) -> Dict[str, any]:
        """
        Obtiene el estado actual de la máquina.

        Returns:
            Diccionario con el estado actual de recursos y ganancias.
        """
        status = {
            "resources": {},
            "earnings": 0.0
        }

        try:
            for resource_type in ResourceType:
                amount = self.resource_manager.get_resource(resource_type)
                status["resources"][resource_type.value] = amount

            status["earnings"] = self.money_machine.get_earnings()
        except Exception as e:
            raise RuntimeError(f"Error al obtener el estado de la máquina: {str(e)}")

        return status

    def handle_error(self, error: Exception) -> None:
        """
        Maneja errores ocurridos durante la operación.

        Args:
            error: La excepción ocurrida.
        """
        error_type = type(error).__name__
        error_message = str(error)
        print(f"Error en la máquina de café: {error_type} - {error_message}")

        if isinstance(error, InvalidDrinkError):
            print("Se ha seleccionado una bebida inválida.")
        elif isinstance(error, InsufficientResourcesError):
            print("No hay suficientes recursos para preparar la bebida.")
        elif isinstance(error, ValueError):
            print("Se ha producido un error de valor. Por favor, revise los datos ingresados.")
        elif isinstance(error, RuntimeError):
            print("Error de ejecución. La operación no pudo completarse.")
        else:
            print("Se ha producido un error inesperado. Por favor, contacte al servicio técnico.")

        self._log_error(error_type, error_message)

    def _log_error(self, error_type: str, error_message: str) -> None:
        """
        Registra el error en un archivo de log.

        Args:
            error_type: Tipo de error ocurrido.
            error_message: Mensaje detallado del error.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {error_type}: {error_message}\n"

        try:
            with open("coffee_machine_errors.log", "a") as log_file:
                log_file.write(log_entry)
        except IOError as e:
            print(f"No se pudo registrar el error: {e}")

    def shutdown(self) -> None:
        """Realiza el proceso de apagado de la máquina."""
        print("Apagando la máquina de café.")
        self.save_state()

    def maintenance_mode(self) -> None:
        """Activa el modo de mantenimiento de la máquina."""
        print("Entrando en modo de mantenimiento...")
        # Implementa aquí la lógica del modo de mantenimiento
        print("Modo de mantenimiento completado.")

    def check_low_resources(self, threshold: float = 0.2) -> None:
        """
        Verifica si algún recurso está por debajo del umbral especificado.

        Args:
            threshold: Umbral para considerar un recurso como bajo (por defecto 20%).
        """
        for resource_type in ResourceType:
            amount = self.resource_manager.get_resource(resource_type)
            capacity = self.resource_manager.get_capacity(resource_type)
            if amount / capacity < threshold:
                print(f"Advertencia: {resource_type.value} está bajo.")

    def calculate_possible_drinks(self) -> Dict[str, int]:
        """
        Calcula cuántas bebidas de cada tipo se pueden hacer con los recursos actuales.

        Returns:
            Diccionario con el nombre de la bebida y la cantidad posible.
        """
        possible_drinks = {}
        for drink in self.menu.get_drinks():
            max_servings = float('inf')
            for ingredient, amount in drink.ingredients.items():
                resource_type = ResourceType(ingredient)
                available = self.resource_manager.get_resource(resource_type)
                servings = available // amount
                max_servings = min(max_servings, servings)
            possible_drinks[drink.name] = int(max_servings)
        return possible_drinks

    def save_state(self, filename: str = "coffee_machine_state.json") -> None:
        """
        Guarda el estado actual de la máquina en un archivo JSON.

        Args:
            filename: Nombre del archivo para guardar el estado.
        """
        state = self.get_status()
        with open(filename, 'w') as f:
            json.dump(state, f)
        print(f"Estado de la máquina guardado en {filename}")

    def load_state(self, filename: str = "coffee_machine_state.json") -> None:
        """
        Carga el estado de la máquina desde un archivo JSON.

        Args:
            filename: Nombre del archivo para cargar el estado.
        """
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
            # Implementar la lógica para restaurar el estado
            for resource_type, amount in state['resources'].items():
                self.resource_manager.set_resource(ResourceType(resource_type), amount)
            self.money_machine.set_earnings(state['earnings'])
            print(f"Estado de la máquina cargado desde {filename}")
        except FileNotFoundError:
            print(f"No se encontró el archivo de estado {filename}")
        except json.JSONDecodeError:
            print(f"Error al decodificar el archivo de estado {filename}")
        except Exception as e:
            print(f"Error al cargar el estado: {str(e)}")
