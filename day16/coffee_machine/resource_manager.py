from enum import Enum, auto
from typing import Dict, Optional

class ResourceType(Enum):
    WATER = auto()
    MILK = auto()
    COFFEE = auto()

class ResourceManager:
    """
    Gestiona los recursos de la máquina de café.
    """

    def __init__(self, initial_resources: Dict[ResourceType, int]):
        """
        Inicializa el gestor de recursos con los recursos iniciales.

        Args:
            initial_resources (Dict[ResourceType, int]): Diccionario con los recursos iniciales.
        """
        self._resources: Dict[ResourceType, int] = initial_resources.copy()

    def get_resources(self) -> Dict[ResourceType, int]:
        """
        Obtiene una copia de los recursos actuales.

        Returns:
            Dict[ResourceType, int]: Diccionario con los recursos actuales.
        """
        return self._resources.copy()

    def check_resources(self, required_resources: Dict[ResourceType, int]) -> Optional[ResourceType]:
        """
        Verifica si hay suficientes recursos para preparar una bebida.

        Args:
            required_resources (Dict[ResourceType, int]): Recursos necesarios para la bebida.

        Returns:
            Optional[ResourceType]: Tipo de recurso faltante, o None si hay suficientes recursos.
        """
        for resource, required_amount in required_resources.items():
            if resource not in self._resources:
                return resource  # Recurso no disponible en la máquina
            if self._resources[resource] < required_amount:
                return resource  # Recurso insuficiente

        return None  # Todos los recursos son suficientes

    def deduct_resources(self, used_resources: Dict[ResourceType, int]) -> None:
        """
        Deduce los recursos utilizados para preparar una bebida.

        Args:
            used_resources (Dict[ResourceType, int]): Recursos utilizados en la preparación.

        Raises:
            KeyError: Si un recurso no existe en la máquina.
            ValueError: Si no hay suficientes recursos para deducir.
        """
        for resource, amount in used_resources.items():
            if resource not in self._resources:
                raise KeyError(f"El recurso '{resource.name}' no existe en la máquina.")
            if self._resources[resource] < amount:
                raise ValueError(f"No hay suficiente {resource.name} para deducir.")
            self._resources[resource] -= amount

    def add_resources(self, added_resources: Dict[ResourceType, int]) -> None:
        """
        Añade recursos a la máquina.

        Args:
            added_resources (Dict[ResourceType, int]): Recursos a añadir.

        Raises:
            ValueError: Si la cantidad a añadir no es un entero positivo.
        """
        for resource, amount in added_resources.items():
            if not isinstance(amount, int) or amount < 0:
                raise ValueError(f"La cantidad para '{resource.name}' debe ser un entero no negativo.")
            if resource in self._resources:
                self._resources[resource] += amount
            else:
                self._resources[resource] = amount

    def print_report(self) -> None:
        """
        Imprime un informe del estado actual de los recursos.
        """
        print("Informe de Recursos:")
        print("-------------------")
        for resource, amount in self._resources.items():
            unit = self._get_unit(resource)
            print(f"{resource.name.capitalize()}: {amount}{unit}")
        if not self._resources:
            print("No hay recursos disponibles.")

    def has_resource(self, resource: ResourceType) -> bool:
        """
        Verifica si un recurso específico existe en la máquina.

        Args:
            resource (ResourceType): El recurso a verificar.

        Returns:
            bool: True si el recurso existe, False en caso contrario.
        """
        return resource in self._resources

    @staticmethod
    def _get_unit(resource_type: ResourceType) -> str:
        """
        Obtiene la unidad de medida para un tipo de recurso.

        Args:
            resource_type (ResourceType): El tipo de recurso.

        Returns:
            str: La unidad de medida ("g" para café, "ml" para otros).
        """
        if resource_type == ResourceType.COFFEE:
            return "g"
        return "ml"

    def __str__(self) -> str:
        """
        Retorna una representación en cadena de los recursos actuales.

        Returns:
            str: Representación en cadena de los recursos.
        """
        return '\n'.join([f"{resource.name.capitalize()}: {amount}{self._get_unit(resource)}"
                          for resource, amount in self._resources.items()])

    def __repr__(self) -> str:
        """
        Retorna una representación detallada del objeto ResourceManager.

        Returns:
            str: Representación detallada del objeto.
        """
        resources_repr = {resource.name: amount for resource, amount in self._resources.items()}
        return f"ResourceManager({resources_repr})"
