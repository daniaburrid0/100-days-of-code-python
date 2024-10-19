import logging
from typing import Dict, Any, Literal, Tuple

# Configuración de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

MENU: Dict[str, Dict[str, Any]] = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

RESOURCES: Dict[str, int] = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

DrinkType = Literal["espresso", "latte", "cappuccino"]
Command = Literal["off", "report"]

def prompt_user() -> DrinkType | Command:
    valid_inputs = list(MENU.keys()) + ["off", "report"]
    while True:
        user_input = input("¿Qué le gustaría? (espresso/latte/cappuccino): ").lower()
        if user_input in valid_inputs:
            return user_input
        print("Opción no válida. Por favor, intente de nuevo.")

def process_command(command: DrinkType | Command, money: float) -> Tuple[bool, float]:
    logging.info(f"Procesando comando: {command}")
    if command == "off":
        logging.info("Apagando la máquina")
        return False, money
    elif command == "report":
        logging.info("Generando informe")
        print_report(money)
    elif command in MENU:
        if check_resources(command):
            payment = process_coins()
            if check_transaction(command, payment):
                make_coffee(command)
                money += MENU[command]["cost"]
                logging.info(f"Bebida {command} preparada. Dinero actual: ${money:.2f}")
    else:
        logging.warning(f"Comando desconocido: {command}")
    return True, money

def print_report(money: float) -> None:
    logging.info("Imprimiendo informe")
    print("\n===== INFORME DE RECURSOS =====")
    print(f"Agua  : {RESOURCES['water']:4d} ml")
    print(f"Leche : {RESOURCES['milk']:4d} ml")
    print(f"Café  : {RESOURCES['coffee']:4d} g")
    print(f"Dinero: ${money:.2f}")
    print("==============================\n")

def check_resources(drink: DrinkType) -> bool:
    logging.info(f"Verificando recursos para {drink}")
    for item, amount in MENU[drink]['ingredients'].items():
        if RESOURCES[item] < amount:
            logging.warning(f"Recursos insuficientes: {item}")
            print(f"Lo siento, no hay suficiente {item}.")
            return False
    logging.info("Recursos suficientes")
    return True

def process_coins() -> float:
    logging.info("Procesando monedas")
    print("Por favor, inserte monedas.")
    total = 0.0
    coin_values = {"quarters": 0.25, "dimes": 0.10, "nickles": 0.05, "pennies": 0.01}
    for coin, value in coin_values.items():
        while True:
            try:
                count = int(input(f"¿Cuántos {coin}?: "))
                if count >= 0:
                    total += count * value
                    break
                print("Por favor, ingrese un número no negativo.")
            except ValueError:
                print("Por favor, ingrese un número entero válido.")
    logging.info(f"Total insertado: ${total:.2f}")
    return round(total, 2)

def check_transaction(drink: DrinkType, money_inserted: float) -> bool:
    drink_cost = MENU[drink]['cost']
    logging.info(f"Verificando transacción para {drink}. Costo: ${drink_cost:.2f}, Insertado: ${money_inserted:.2f}")
    if money_inserted < drink_cost:
        logging.warning("Dinero insuficiente")
        print(f"Lo siento, no es suficiente dinero. Se necesitan ${drink_cost:.2f}. Dinero devuelto.")
        return False
    change = round(money_inserted - drink_cost, 2)
    if change > 0:
        logging.info(f"Devolviendo cambio: ${change:.2f}")
        print(f"Aquí tiene ${change:.2f} de cambio.")
    return True

def make_coffee(drink: DrinkType) -> None:
    logging.info(f"Preparando {drink}")
    for item, amount in MENU[drink]['ingredients'].items():
        RESOURCES[item] -= amount
        logging.debug(f"Reduciendo {item} en {amount}")
    print(f"Aquí está su {drink}. ¡Disfrútelo!")

def run_coffee_machine() -> None:
    money = 0.0
    logging.info("Iniciando la máquina de café")
    while True:
        command = prompt_user()
        continue_running, money = process_command(command, money)
        if not continue_running:
            logging.info("Apagando la máquina de café")
            break

if __name__ == "__main__":
    run_coffee_machine()
