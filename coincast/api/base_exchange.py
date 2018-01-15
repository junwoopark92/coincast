from abc import ABC, abstractmethod

class Excahnge(ABC):
    @abstractmethod
    def get_filled_orders(self, coin_type=None, per="minute"):
        pass

    @abstractmethod
    def get_ticker(self, coin_type=None):
        pass

    @abstractmethod
    def get_wallet_status(self):
        pass

    @abstractmethod
    def get_token(self):
        pass

    @abstractmethod
    def set_token(self):
        pass

    @abstractmethod
    def get_username(self):
        pass
