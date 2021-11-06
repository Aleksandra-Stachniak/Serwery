#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from re import match
from typing import Optional, List, Dict


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str)
    #  i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu
    #  float)

    def __init__(self, name: str, price: float) -> None:
        self.name: str = name
        self.price: float = price

    def __eq__(self, other):
        return isinstance(other, Product) and self.name == other.name and self.price == other.price
        # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać: (1) metodę inicjalizacyjną przyjmującą listę obiektów
#  typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#  (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną
#  dopuszczalną liczbę wyników wyszukiwania, (3) możliwość odwołania się do metody `get_entries(self, n_letters)`
#  zwracającą listę produktów spełniających kryterium wyszukiwania


class Server(ABC):
    n_max_returned_entries: int = 3

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    @abstractmethod
    def get_list_products(self, n_letters: int = 1):
        raise NotImplementedError

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        pattern = '^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters)
        entries = []

        for i in self.get_list_products(n_letters):
            if match(pattern, i.name):
                entries.append(i)

        if len(entries) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError
        else:
            return sorted(entries, key=lambda x: x.price)


class ListServer(Server):
    def __init__(self, products: List[Product], *arg, **kwargs) -> None:
        super().__init__(*arg, **kwargs)
        self.products: List[Product] = products

    def get_list_products(self, n_letters: int = 1) -> List[Product]:
        return self.products


class MapServer(Server):
    def __init__(self, products: List[Product], *arg, **kwargs) -> None:
        super().__init__(*arg, **kwargs)
        self.products: Dict[str, Product] = {el.name: el for el in products}

    def get_list_products(self, n_letters: int = 1) -> List[Product]:
        return list(self.products.values())


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, serwer: Server) -> None:
        self.serwer: Server = serwer

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            total_price = 0
            entries = self.serwer.get_entries(n_letters)
            if not entries:
                return None
            else:
                for i in entries:
                    total_price += i.price
                return total_price
        except TooManyProductsFoundError:
            return None


if __name__ == '__main__':
    pass
