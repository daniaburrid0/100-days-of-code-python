from typing import Dict

class Drink:
    def __init__(self, name: str, ingredients: Dict[str, int], price: float):
        if not ingredients:
            raise ValueError("Ingredients cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        self._name: str = name
        self._ingredients: Dict[str, int] = ingredients
        self._price: float = price

    def __str__(self) -> str:
        return f"{self._name.capitalize()}: ${self._price:.2f}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def ingredients(self) -> Dict[str, int]:
        return self._ingredients.copy()

    @property
    def price(self) -> float:
        return self._price

    def __repr__(self) -> str:
        return f"Drink(name='{self._name}', ingredients={self._ingredients}, price={self._price})"
