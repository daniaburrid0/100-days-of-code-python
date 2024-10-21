from typing import Dict, List, Optional
from pathlib import Path
from drink import Drink
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Menu:
    """
    Representa el menú de bebidas disponibles en la máquina de café.
    """

    def __init__(self, menu_file: Path = Path('data/menu_data.json')):
        """
        Inicializa el menú cargando los datos desde un archivo JSON.

        Args:
            menu_file (Path): Ruta al archivo JSON que contiene los datos del menú.
        """
        self._drinks: Dict[str, Drink] = {}
        self._load_menu(menu_file)

    def _load_menu(self, menu_file: Path) -> None:
        """
        Carga los datos del menú desde un archivo JSON y crea objetos Drink.

        Args:
            menu_file (Path): Ruta al archivo JSON que contiene los datos del menú.
        """
        if not menu_file.exists():
            raise FileNotFoundError(f"El archivo de menú {menu_file} no existe.")

        with menu_file.open('r') as file:
            try:
                menu_data = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error al decodificar el archivo JSON: {e}")

        for drink_name, drink_info in menu_data.items():
            try:
                ingredients = drink_info['ingredients']
                price = drink_info['price']
                self._drinks[drink_name] = Drink(drink_name, ingredients, price)
            except KeyError as e:
                logger.warning(f"Error: Falta la clave {e} para la bebida {drink_name}. Se omitirá esta bebida.")
            except Exception as e:
                logger.error(f"Error inesperado al procesar la bebida {drink_name}: {e}")

        if not self._drinks:
            logger.info("No se pudo cargar ninguna bebida del menú. El menú está vacío.")

    def find_drink(self, drink_name: str) -> Optional[Drink]:
        return self._drinks.get(drink_name)

    @property
    def available_drinks(self) -> List[str]:
        """
        Obtiene la lista de nombres de bebidas disponibles en el menú.

        Returns:
            List[str]: Lista de nombres de bebidas disponibles.
        """
        return list(self._drinks.keys())

    def print_menu(self) -> None:
        """
        Imprime el menú de bebidas disponibles con sus precios.
        """
        print("Menú de Bebidas:")
        print("-----------------")
        for drink in self._drinks.values():
            print(f"{drink}")
        if not self._drinks:
            print("No hay bebidas disponibles en el menú.")

    @classmethod
    def from_file(cls, menu_file: Path) -> 'Menu':
        """
        Crea una instancia de Menu desde un archivo.

        Args:
            menu_file (Path): Ruta al archivo JSON que contiene los datos del menú.

        Returns:
            Menu: Una nueva instancia de Menu.
        """
        menu = cls()
        menu._load_menu(menu_file)
        return menu

    def __len__(self) -> int:
        """Retorna el número de bebidas en el menú."""
        return len(self._drinks)

    def __iter__(self):
        """Permite iterar sobre las bebidas del menú."""
        return iter(self._drinks.values())
