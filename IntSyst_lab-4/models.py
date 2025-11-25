"""
Класи для представлення CSP задачі
"""
from typing import List, Dict, Optional
from enum import Enum


class Color(Enum):
    """Доступні кольори для розфарбування"""
    RED = "Червоний"
    BLUE = "Синій"
    GREEN = "Зелений"
    YELLOW = "Жовтий"
    ORANGE = "Помаранчевий"
    PURPLE = "Фіолетовий"


class CSPVariable:
    """
    Змінна в CSP задачі
    Представляє одну область на карті
    """
    
    def __init__(self, name: str, domain: List[Color]):
        """
        Ініціалізує змінну
        
        Args:
            name: Назва змінної (область)
            domain: Список можливих значень (кольорів)
        """
        self.name = name
        self.domain = domain.copy()  # Можливі значення
        self.value: Optional[Color] = None  # Поточне призначене значення
        self.original_domain = domain.copy()  # Оригінальний домен для відновлення
    
    def assign(self, value: Color):
        """
        Призначає значення змінній
        
        Args:
            value: Колір для призначення
        """
        self.value = value
    
    def unassign(self):
        """Скасовує призначення"""
        self.value = None
    
    def is_assigned(self) -> bool:
        """
        Перевіряє чи призначене значення
        
        Returns:
            True якщо значення призначене
        """
        return self.value is not None
    
    def restore_domain(self):
        """Відновлює оригінальний домен"""
        self.domain = self.original_domain.copy()
    
    def __repr__(self):
        return f"{self.name}={self.value.value if self.value else 'None'}"


class Constraint:
    """
    Обмеження між двома змінними
    Представляє сусідство двох областей
    """
    
    def __init__(self, var1: str, var2: str):
        """
        Ініціалізує обмеження
        
        Args:
            var1: Перша змінна (область)
            var2: Друга змінна (область)
        """
        self.var1 = var1
        self.var2 = var2
    
    def is_satisfied(self, assignment: Dict[str, Color]) -> bool:
        """
        Перевіряє чи задовольняється обмеження
        Дві сусідні області мають бути різних кольорів
        
        Args:
            assignment: Поточне присвоєння змінних
            
        Returns:
            True якщо обмеження задоволене
        """
        # Якщо хоча б одна змінна не призначена - обмеження задоволене
        if self.var1 not in assignment or self.var2 not in assignment:
            return True
        
        # Перевіряємо що кольори різні
        return assignment[self.var1] != assignment[self.var2]
    
    def involves(self, var_name: str) -> bool:
        """
        Перевіряє чи обмеження стосується змінної
        
        Args:
            var_name: Назва змінної
            
        Returns:
            True якщо обмеження стосується цієї змінної
        """
        return self.var1 == var_name or self.var2 == var_name
    
    def get_other(self, var_name: str) -> Optional[str]:
        """
        Отримує іншу змінну в обмеженні
        
        Args:
            var_name: Назва однієї змінної
            
        Returns:
            Назва іншої змінної або None
        """
        if self.var1 == var_name:
            return self.var2
        elif self.var2 == var_name:
            return self.var1
        return None
    
    def __repr__(self):
        return f"{self.var1} != {self.var2}"