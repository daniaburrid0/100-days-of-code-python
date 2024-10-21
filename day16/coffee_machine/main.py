import logging
from typing import Dict, Any
import json
from pathlib import Path
import sys
from menu import Menu
from resource_manager import ResourceManager, ResourceType
from money_machine import MoneyMachine
from coffee_machine import CoffeeMachine

# Configurar logging para la aplicación
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='coffee_machine.log'
)
logger = logging.getLogger(__name__)

def load_config(config_file: str = 'config.json') -> Dict[str, Any]:
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        logger.info(f"Configuración cargada exitosamente desde {config_file}")
        return config
    except FileNotFoundError:
        logger.error(f"Archivo de configuración {config_file} no encontrado")
        raise
    except json.JSONDecodeError:
        logger.error(f"Error al decodificar el archivo de configuración {config_file}")
        raise

def initialize_menu(config: Dict[str, Any]) -> Menu:
    menu_file = config.get('menu_file', 'menu_data.json')
    try:
        menu = Menu.from_file(Path(menu_file))
        logger.info(f"Menú inicializado correctamente desde {menu_file}")
        return menu
    except FileNotFoundError:
        logger.error(f"Archivo de menú {menu_file} no encontrado")
        raise
    except json.JSONDecodeError:
        logger.error(f"Error al decodificar el archivo de menú {menu_file}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al inicializar el menú: {e}")
        raise

def initialize_resource_manager(config: Dict[str, Any]) -> ResourceManager:
    initial_resources = config.get('initial_resources', {})
    typed_resources = {
        ResourceType[k.upper()]: v for k, v in initial_resources.items()
    }
    try:
        resource_manager = ResourceManager(typed_resources)
        logger.info("Gestor de recursos inicializado correctamente")
        return resource_manager
    except ValueError as e:
        logger.error(f"Error al inicializar el gestor de recursos: {e}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al inicializar el gestor de recursos: {e}")
        raise

def initialize_money_machine(config: Dict[str, Any]) -> MoneyMachine:
    initial_balance = config.get('initial_balance', 0)
    try:
        money_machine = MoneyMachine(initial_balance)
        logger.info(f"Máquina de dinero inicializada con saldo inicial de ${initial_balance}")
        return money_machine
    except ValueError as e:
        logger.error(f"Error al inicializar la máquina de dinero: {e}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al inicializar la máquina de dinero: {e}")
        raise

def create_coffee_machine(menu: Menu, resource_manager: ResourceManager, money_machine: MoneyMachine) -> CoffeeMachine:
    try:
        coffee_machine = CoffeeMachine(menu, resource_manager, money_machine)
        logger.info("Máquina de café creada correctamente")
        return coffee_machine
    except Exception as e:
        logger.error(f"Error al crear la máquina de café: {e}")
        raise

def maintenance_mode(coffee_machine: CoffeeMachine):
    logger.info("Entrando en modo de mantenimiento")
    print("Modo de mantenimiento")
    print("1. Recargar recursos")
    print("2. Ver estadísticas")
    print("3. Salir del modo de mantenimiento")
    choice = input("Seleccione una opción: ")
    if choice == "1":
        # Implementar lógica para recargar recursos
        pass
    elif choice == "2":
        # Implementar lógica para mostrar estadísticas
        pass
    elif choice == "3":
        logger.info("Saliendo del modo de mantenimiento")
        return
    else:
        print("Opción no válida")

def save_state(coffee_machine: CoffeeMachine):
    try:
        coffee_machine.save_state()
        logger.info("Estado de la máquina guardado correctamente")
    except Exception as e:
        logger.error(f"Error al guardar el estado de la máquina: {e}")

def load_state(coffee_machine: CoffeeMachine):
    try:
        coffee_machine.load_state()
        logger.info("Estado de la máquina cargado correctamente")
    except FileNotFoundError:
        logger.warning("No se encontró un archivo de estado previo")
    except Exception as e:
        logger.error(f"Error al cargar el estado de la máquina: {e}")

def main():
    logger.info("Iniciando la máquina de café")

    try:
        config = load_config()
        menu = initialize_menu(config)
        resource_manager = initialize_resource_manager(config)
        money_machine = initialize_money_machine(config)
        coffee_machine = create_coffee_machine(menu, resource_manager, money_machine)
        load_state(coffee_machine)
    except Exception as e:
        logger.critical(f"Error crítico al inicializar la máquina de café: {e}")
        sys.exit(1)

    while True:
        try:
            print("\n1. Modo normal")
            print("2. Modo mantenimiento")
            print("3. Apagar")
            mode = input("Seleccione un modo: ")

            if mode == "1":
                coffee_machine.start()
            elif mode == "2":
                maintenance_mode(coffee_machine)
            elif mode == "3":
                save_state(coffee_machine)
                logger.info("Apagando la máquina de café")
                break
            else:
                print("Modo no válido")
        except KeyboardInterrupt:
            logger.info("Operación cancelada por el usuario")
            save_state(coffee_machine)
            break
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            print("Ha ocurrido un error inesperado. Por favor, intente de nuevo.")

    print("Gracias por usar la máquina de café. ¡Hasta luego!")

if __name__ == "__main__":
    main()
