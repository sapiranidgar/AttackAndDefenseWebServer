from abc import ABC, abstractmethod

from web_attacks.attack_parameters import AttackParameters


class Attack(ABC):
    @abstractmethod
    def perform_attack(self, attack_params: AttackParameters):
        pass

    @abstractmethod
    def get_attack_description(self) -> str:
        pass

    @abstractmethod
    def get_attack_name(self) -> str:
        pass

    def get_attack_details(self) -> str:
        name = self.get_attack_name()
        desc = self.get_attack_description()
        return f"##### {name} ####\nDescription: {desc}\n"