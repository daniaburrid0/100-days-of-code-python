from typing import Dict
from decimal import Decimal, ROUND_HALF_UP

class MoneyMachine:
    """
    Maneja las transacciones monetarias de la máquina de café.
    """

    COIN_VALUES: Dict[str, Decimal] = {
        "quarters": Decimal('0.25'),
        "dimes": Decimal('0.10'),
        "nickles": Decimal('0.05'),
        "pennies": Decimal('0.01')
    }
    DECIMAL_PLACES = 2

    def __init__(self, initial_profit: float = 0):
        """
        Inicializa la máquina de dinero con un saldo inicial.

        Args:
            initial_profit (float): Saldo inicial de la máquina. Por defecto es 0.

        Raises:
            ValueError: Si el saldo inicial es negativo.
        """
        if initial_profit < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")
        self._profit: Decimal = Decimal(initial_profit).quantize(Decimal(f'0.{self.DECIMAL_PLACES * "0"}'), rounding=ROUND_HALF_UP)
        self._num_transactions: int = 0

    def report(self) -> None:
        """
        Imprime un informe del dinero recaudado y las transacciones realizadas.
        """
        print(f"Dinero recaudado: ${self._profit:.2f}")
        print(f"Número de transacciones: {self._num_transactions}")
        if self._num_transactions > 0:
            average_transaction = self._profit / self._num_transactions
            print(f"Promedio por transacción: ${average_transaction:.2f}")
        else:
            print("No se han realizado transacciones aún.")

    def process_coins(self) -> Decimal:
        """
        Procesa las monedas insertadas por el usuario.

        Returns:
            Decimal: El valor total de las monedas insertadas.

        Raises:
            ValueError: Si se ingresa un número negativo de monedas.
        """
        total = Decimal('0.00')
        for coin, value in self.COIN_VALUES.items():
            while True:
                try:
                    count = int(input(f"Ingrese el número de {coin}: "))
                    if count < 0:
                        raise ValueError("El número de monedas no puede ser negativo.")
                    total += Decimal(count) * value
                    break
                except ValueError as e:
                    print(f"Error: {e}. Por favor, ingrese un número válido.")
        return total.quantize(Decimal(f'0.{self.DECIMAL_PLACES * "0"}'), rounding=ROUND_HALF_UP)

    def make_payment(self, cost: float) -> bool:
        """
        Procesa el pago de una bebida.

        Args:
            cost (float): El costo de la bebida.

        Returns:
            bool: True si el pago fue exitoso, False si fue insuficiente.

        Raises:
            ValueError: Si el costo es negativo o cero.
        """
        if cost <= 0:
            raise ValueError("El costo debe ser un valor positivo.")

        cost_decimal = Decimal(str(cost)).quantize(Decimal(f'0.{self.DECIMAL_PLACES * "0"}'), rounding=ROUND_HALF_UP)
        print(f"El costo de la bebida es: ${cost_decimal:.2f}")
        payment = self.process_coins()

        if payment < cost_decimal:
            print(f"Lo siento, eso no es suficiente dinero. Se reembolsan ${payment:.2f}.")
            return False

        change = (payment - cost_decimal).quantize(Decimal(f'0.{self.DECIMAL_PLACES * "0"}'), rounding=ROUND_HALF_UP)
        if change > 0:
            print(f"Aquí está su cambio: ${change:.2f}")

        self._profit += cost_decimal
        self._num_transactions += 1
        print(f"¡Pago exitoso! Disfrute su bebida.")
        return True

    def add_money(self, amount: float) -> None:
        self._profit += Decimal(str(amount)).quantize(Decimal(f'0.{self.DECIMAL_PLACES * "0"}'), rounding=ROUND_HALF_UP)
        self._num_transactions += 1

    def get_earnings(self) -> float:
        return float(self._profit)

    def set_earnings(self, amount: float) -> None:
        self._profit = Decimal(str(amount)).quantize(Decimal(f'0.{self.DECIMAL_PLACES * "0"}'), rounding=ROUND_HALF_UP)

    @property
    def profit(self) -> Decimal:
        """
        Obtiene el profit actual.

        Returns:
            Decimal: El profit actual de la máquina.
        """
        return self._profit

    def __str__(self) -> str:
        """
        Retorna una representación en cadena del estado actual de la máquina de dinero.

        Returns:
            str: Representación en cadena del estado de la máquina de dinero.
        """
        return f"MoneyMachine(profit=${self._profit:.2f}, transactions={self._num_transactions})"

    def __repr__(self) -> str:
        """
        Retorna una representación detallada del objeto MoneyMachine.

        Returns:
            str: Representación detallada del objeto.
        """
        return f"MoneyMachine(profit={self._profit}, transactions={self._num_transactions}, coin_values={self.COIN_VALUES})"
