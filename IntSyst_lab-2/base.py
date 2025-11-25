from abc import ABC, abstractmethod
from typing import List, Set, Dict, Optional
from enum import Enum


class RelationType(Enum):
    """Типи відношень в онтології"""
    IS_A = "is_a"           # -- Наслідування
    HAS_A = "has_a"         # -- Композиція 
    USES = "uses"           # -- Асоціація 


class Entity(ABC):
    """
    РІВЕНЬ 1: Базовий клас для всіх сутностей
    Абстрактний клас - основа онтології
    """
    _instances: Dict[str, 'Entity'] = {}  # Реєстр всіх створених об'єктів
    
    def __init__(self, name: str):
        self.name = name
        self.has_parts: List['Entity'] = []      # HAS-A відношення
        self.uses_entities: List['Entity'] = []   # USES відношення
        Entity._instances[name] = self
    
    @abstractmethod
    def describe(self) -> str:
        """Опис сутності - має бути реалізований у кожному класі"""
        pass
    
    def add_part(self, part: 'Entity') -> None:
        """ (HAS-A відношення)"""
        if part not in self.has_parts:
            self.has_parts.append(part)
    
    def add_usage(self, entity: 'Entity') -> None:
        """(USES відношення)"""
        if entity not in self.uses_entities:
            self.uses_entities.append(entity)
    
    def get_all_parts(self) -> List['Entity']:
        """ всі частини"""
        all_parts = []
        for part in self.has_parts:
            all_parts.append(part)
            all_parts.extend(part.get_all_parts())
        return all_parts
    
    def is_related_to(self, target: 'Entity', max_depth: int = 5) -> tuple[bool, List[str]]:
        return self._find_path(target, set(), [], max_depth)
    
    def _find_path(self, target: 'Entity', visited: Set[str], 
                   path: List[str], max_depth: int) -> tuple[bool, List[str]]:
        """Рекурсивний пошук шляху між сутностями"""
        if max_depth == 0:
            return False, []
        
        if self.name in visited:
            return False, []
        
        visited.add(self.name)
        current_path = path + [self.name]
        
        # Знайшли цільову сутність!
        if self == target:
            return True, current_path
        
        # Перевіряємо HAS-A відношення
        for part in self.has_parts:
            found, result_path = part._find_path(target, visited.copy(), 
                                                 current_path + ["HAS-A"], max_depth - 1)
            if found:
                return True, result_path
        
        # Перевіряємо USES відношення
        for used in self.uses_entities:
            found, result_path = used._find_path(target, visited.copy(), 
                                                  current_path + ["USES"], max_depth - 1)
            if found:
                return True, result_path
        
        # Перевіряємо IS-A (батьківський клас)
        parent_classes = self.__class__.__mro__[1:-1]  # Всі батьківські класи крім object
        for parent_class in parent_classes:
            if parent_class == Entity or parent_class == ABC:
                continue
            # Шукаємо інстанси батьківського класу
            for instance in Entity._instances.values():
                if isinstance(instance, parent_class) and instance != self:
                    found, result_path = instance._find_path(target, visited.copy(),
                                                            current_path + ["IS-A"], max_depth - 1)
                    if found:
                        return True, result_path
        
        return False, []
    
    @classmethod
    def get_instance(cls, name: str) -> Optional['Entity']:
        """Отримує екземпляр за іменем"""
        return cls._instances.get(name)
    
    @classmethod
    def get_all_instances(cls) -> List['Entity']:
        """Отримує всі створені екземпляри"""
        return list(cls._instances.values())
    
    @classmethod
    def clear_instances(cls) -> None:
        """Очищає всі створені екземпляри (для тестування)"""
        cls._instances.clear()
    
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"


# ============================================================================
# РІВЕНЬ 2: Основні категорії
# ============================================================================

class LivingBeing(Entity):
    """РІВЕНЬ 2: Жива істота"""
    
    def __init__(self, name: str, age: int):
        super().__init__(name)
        self.age = age
    
    @abstractmethod
    def make_sound(self) -> str:
        """Кожна жива істота має звук"""
        pass
    
    def describe(self) -> str:
        return f"{self.name} - жива істота, вік: {self.age}"


class Building(Entity):
    """РІВЕНЬ 2: Будівля"""
    
    def __init__(self, name: str, address: str, floors: int):
        super().__init__(name)
        self.address = address
        self.floors = floors
    
    def describe(self) -> str:
        return f"{self.name} - будівля за адресою {self.address}, поверхів: {self.floors}"


class Vehicle(Entity):
    """РІВЕНЬ 2: Транспортний засіб"""
    
    def __init__(self, name: str, max_speed: int):
        super().__init__(name)
        self.max_speed = max_speed
    
    @abstractmethod
    def move(self) -> str:
        """Кожен транспорт рухається по-своєму"""
        pass
    
    def describe(self) -> str:
        return f"{self.name} - транспорт, макс. швидкість: {self.max_speed} км/год"


class Part(Entity):
    """РІВЕНЬ 2: Частина/компонент"""
    
    def __init__(self, name: str, material: str):
        super().__init__(name)
        self.material = material
    
    def describe(self) -> str:
        return f"{self.name} - компонент з матеріалу: {self.material}"