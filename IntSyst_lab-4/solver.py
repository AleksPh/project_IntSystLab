"""
CSP Solver - алгоритм backtracking з евристиками
"""
from typing import Dict, List, Set, Optional
import time
from models import CSPVariable, Constraint, Color


class CSP:
    """
    Constraint Satisfaction Problem
    Розв'язує задачу за допомогою backtracking з евристиками
    """
    
    def __init__(self):
        """Ініціалізує CSP задачу"""
        self.variables: Dict[str, CSPVariable] = {}
        self.constraints: List[Constraint] = []
        self.neighbors: Dict[str, Set[str]] = {}  # Сусіди кожної змінної
        
        # Статистика
        self.steps = 0
        self.backtracks = 0
    
    def add_variable(self, name: str, domain: List[Color]):
        """
        Додає змінну до задачі
        
        Args:
            name: Назва змінної
            domain: Список можливих значень
        """
        self.variables[name] = CSPVariable(name, domain)
        self.neighbors[name] = set()
    
    def add_constraint(self, var1: str, var2: str):
        """
        Додає обмеження (сусідство двох змінних)
        
        Args:
            var1: Перша змінна
            var2: Друга змінна
        """
        constraint = Constraint(var1, var2)
        self.constraints.append(constraint)
        
        # Оновлюємо сусідів
        self.neighbors[var1].add(var2)
        self.neighbors[var2].add(var1)
    
    def is_consistent(self, var_name: str, value: Color, assignment: Dict[str, Color]) -> bool:
        """
        Перевіряє чи значення узгоджене з поточним присвоєнням
        
        Args:
            var_name: Ім'я змінної
            value: Значення для перевірки
            assignment: Поточне присвоєння
            
        Returns:
            True якщо значення узгоджене
        """
        # Тимчасово призначаємо значення
        temp_assignment = assignment.copy()
        temp_assignment[var_name] = value
        
        # Перевіряємо всі обмеження що стосуються цієї змінної
        for constraint in self.constraints:
            if constraint.involves(var_name):
                if not constraint.is_satisfied(temp_assignment):
                    return False
        
        return True
    
    def select_unassigned_variable(self, assignment: Dict[str, Color]) -> Optional[str]:
        """
        Вибирає наступну невизначену змінну
        Використовує евристику MRV (Minimum Remaining Values)
        
        Args:
            assignment: Поточне присвоєння
            
        Returns:
            Ім'я змінної або None
        """
        unassigned = [name for name in self.variables.keys() if name not in assignment]
        
        if not unassigned:
            return None
        
        # MRV евристика - вибираємо змінну з найменшою кількістю допустимих значень
        def count_legal_values(var_name: str) -> int:
            """Рахує кількість допустимих значень для змінної"""
            count = 0
            for value in self.variables[var_name].domain:
                if self.is_consistent(var_name, value, assignment):
                    count += 1
            return count
        
        # Якщо є змінна з 0 допустимих значень - повертаємо її (ранній виявлення тупика)
        for var_name in unassigned:
            if count_legal_values(var_name) == 0:
                return var_name
        
        # Вибираємо змінну з мінімальною кількістю допустимих значень
        # При рівності використовуємо degree heuristic (більше сусідів = вища пріоритет)
        return min(unassigned, key=lambda v: (count_legal_values(v), -len(self.neighbors[v])))
    
    def order_domain_values(self, var_name: str, assignment: Dict[str, Color]) -> List[Color]:
        """
        Упорядковує значення домену
        Використовує евристику LCV (Least Constraining Value)
        
        Args:
            var_name: Ім'я змінної
            assignment: Поточне присвоєння
            
        Returns:
            Упорядкований список значень
        """
        def count_conflicts(value: Color) -> int:
            """
            Рахує скільки сусідів будуть обмежені цим значенням
            
            Args:
                value: Колір для перевірки
                
            Returns:
                Кількість конфліктів
            """
            conflicts = 0
            for neighbor in self.neighbors[var_name]:
                if neighbor not in assignment:
                    # Перевіряємо чи це значення обмежить сусіда
                    if value in self.variables[neighbor].domain:
                        conflicts += 1
            return conflicts
        
        # Фільтруємо тільки узгоджені значення
        values = [v for v in self.variables[var_name].domain 
                 if self.is_consistent(var_name, v, assignment)]
        
        # Сортуємо за кількістю конфліктів (менше конфліктів = краще)
        return sorted(values, key=count_conflicts)
    
    def forward_check(self, var_name: str, value: Color, assignment: Dict[str, Color]) -> bool:
        """
        Forward checking - перевіряємо чи призначення не робить інші змінні безнадійними
        
        Args:
            var_name: Ім'я змінної
            value: Призначене значення
            assignment: Поточне присвоєння
            
        Returns:
            True якщо можна продовжувати, False якщо тупик
        """
        # Перевіряємо всіх непризначених сусідів
        for neighbor in self.neighbors[var_name]:
            if neighbor not in assignment:
                # Рахуємо скільки допустимих значень залишилось у сусіда
                legal_values = 0
                for neighbor_value in self.variables[neighbor].domain:
                    temp_assignment = assignment.copy()
                    temp_assignment[neighbor] = neighbor_value
                    if self.is_consistent(neighbor, neighbor_value, temp_assignment):
                        legal_values += 1
                
                # Якщо не залишилось допустимих значень - тупик
                if legal_values == 0:
                    return False
        
        return True
    
    def backtrack(self, assignment: Dict[str, Color]) -> Optional[Dict[str, Color]]:
        """
        Алгоритм backtracking для пошуку розв'язку
        
        Алгоритм:
        1. Якщо всі змінні призначені - повертаємо розв'язок
        2. Вибираємо наступну змінну (MRV)
        3. Для кожного значення з домену (LCV):
           - Перевіряємо узгодженість
           - Призначаємо значення
           - Forward checking
           - Рекурсивно продовжуємо
           - Якщо не вийшло - ВІДКАТ (backtrack)
        
        Args:
            assignment: Поточне присвоєння
            
        Returns:
            Повне присвоєння або None якщо розв'язку немає
        """
        self.steps += 1
        
        # Базовий випадок - всі змінні призначені
        if len(assignment) == len(self.variables):
            return assignment
        
        # Вибираємо наступну змінну (евристика MRV)
        var_name = self.select_unassigned_variable(assignment)
        
        if var_name is None:
            return assignment
        
        # Пробуємо всі значення з домену (евристика LCV)
        for value in self.order_domain_values(var_name, assignment):
            # Перевіряємо узгодженість
            if self.is_consistent(var_name, value, assignment):
                # Призначаємо значення
                assignment[var_name] = value
                
                # Forward checking - перевіряємо чи не створили безнадійну ситуацію
                if self.forward_check(var_name, value, assignment):
                    # Рекурсивно продовжуємо пошук
                    result = self.backtrack(assignment)
                    
                    if result is not None:
                        return result
                
                # ВІДКАТ (backtrack) - призначення не спрацювало
                del assignment[var_name]
                self.backtracks += 1
        
        # Не знайшли розв'язок для цієї гілки
        return None
    
    def solve(self) -> Optional[Dict[str, Color]]:
        """
        Розв'язує CSP задачу
        
        Returns:
            Словник присвоєнь або None якщо розв'язку немає
        """
        print("🔍 Початок пошуку розв'язку...")
        print(f"   Змінних: {len(self.variables)}")
        print(f"   Обмежень: {len(self.constraints)}")
        print(f"   Кольорів: {len(self.variables[list(self.variables.keys())[0]].domain)}")
        print()
        
        self.steps = 0
        self.backtracks = 0
        start_time = time.time()
        
        result = self.backtrack({})
        
        end_time = time.time()
        
        print(f"\n📊 Статистика:")
        print(f"   Кроків: {self.steps}")
        print(f"   Відкатів: {self.backtracks}")
        print(f"   Час: {(end_time - start_time) * 1000:.2f} мс")
        
        return result
    
    def verify_solution(self, solution: Dict[str, Color]) -> bool:
        """
        Перевіряє чи розв'язок задовольняє всі обмеження
        
        Args:
            solution: Розв'язок для перевірки
            
        Returns:
            True якщо розв'язок правильний
        """
        print("\n🔍 Перевірка розв'язку...")
        
        # Перевіряємо всі обмеження
        violations = 0
        for constraint in self.constraints:
            if not constraint.is_satisfied(solution):
                print(f"❌ Порушено обмеження: {constraint}")
                violations += 1
        
        if violations == 0:
            print("✅ Всі обмеження задоволені!")
            return True
        else:
            print(f"❌ Знайдено {violations} порушень")
            return False