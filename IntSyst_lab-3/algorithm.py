"""
Генетичний алгоритм для оптимізації розкладу
"""
import random
from typing import List, Tuple, Dict
from models import Class, Teacher, Subject, Lesson, Schedule, DayOfWeek


class GeneticScheduler:
    """Генетичний алгоритм для створення оптимального розкладу"""
    
    def __init__(self, 
                 classes: List[Class],
                 teachers: List[Teacher],
                 subjects: List[Subject],
                 population_size: int = 50,
                 mutation_rate: float = 0.1,
                 crossover_rate: float = 0.7,
                 elitism_count: int = 5):
        """
        Ініціалізує генетичний алгоритм
        
        Args:
            classes: Список класів
            teachers: Список вчителів
            subjects: Список предметів
            population_size: Розмір популяції
            mutation_rate: Ймовірність мутації (0-1)
            crossover_rate: Ймовірність схрещування (0-1)
            elitism_count: Кількість найкращих особин що переходять без змін
        """
        self.classes = {c.name: c for c in classes}
        self.teachers = {t.name: t for t in teachers}
        self.subjects = {s.name: s for s in subjects}
        
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        
        self.population: List[Schedule] = []
        self.generation = 0
        self.best_schedule: Schedule = None
        
        # Всі можливі дні та часи
        self.days = list(DayOfWeek)
        self.time_slots = list(range(1, 9))  # 8 уроків на день
    
    def initialize_population(self):
        """Створює початкову популяцію випадкових розкладів"""
        print(f"🧬 Генерація початкової популяції ({self.population_size} особин)...")
        
        self.population = []
        for i in range(self.population_size):
            schedule = self._create_random_schedule()
            self.population.append(schedule)
        
        self._evaluate_population()
        print(f"✅ Початкова популяція створена")
    
    def _create_random_schedule(self) -> Schedule:
        """
        Створює випадковий розклад з мінімумом конфліктів
        
        Returns:
            Новий розклад
        """
        schedule = Schedule()
        
        # Відслідковуємо зайняті слоти для кожного класу та вчителя
        class_slots = {c: set() for c in self.classes.keys()}
        teacher_slots = {t: set() for t in self.teachers.keys()}
        
        # Для кожного класу додаємо всі необхідні уроки
        for class_obj in self.classes.values():
            for subject_obj in self.subjects.values():
                # Знаходимо вчителів що можуть викладати цей предмет
                available_teachers = [
                    t for t in self.teachers.values() 
                    if t.can_teach(subject_obj.name)
                ]
                
                if not available_teachers:
                    continue
                
                # Додаємо необхідну кількість уроків
                for _ in range(subject_obj.lessons_per_week):
                    teacher = random.choice(available_teachers)
                    
                    # Намагаємось знайти вільний слот (максимум 50 спроб)
                    attempts = 0
                    day = random.choice(self.days)
                    time_slot = random.choice(self.time_slots)
                    
                    while attempts < 50:
                        day = random.choice(self.days)
                        time_slot = random.choice(self.time_slots)
                        slot = (day, time_slot)
                        
                        # Перевіряємо чи слот вільний
                        if slot not in class_slots[class_obj.name] and \
                           slot not in teacher_slots[teacher.name]:
                            # Слот вільний - використовуємо
                            class_slots[class_obj.name].add(slot)
                            teacher_slots[teacher.name].add(slot)
                            break
                        attempts += 1
                    
                    # Створюємо урок
                    lesson = Lesson(
                        class_name=class_obj.name,
                        teacher=teacher.name,
                        subject=subject_obj.name,
                        day=day,
                        time_slot=time_slot
                    )
                    schedule.add_lesson(lesson)
        
        return schedule
    
    def _evaluate_population(self):
        """Оцінює всю популяцію та сортує за fitness"""
        for schedule in self.population:
            schedule.calculate_fitness(self.subjects, self.teachers)
        
        # Сортуємо за fitness (найкращі спочатку)
        self.population.sort(key=lambda s: s.fitness, reverse=True)
        
        # Зберігаємо найкращий розклад
        if not self.best_schedule or self.population[0].fitness > self.best_schedule.fitness:
            self.best_schedule = self.population[0].copy()
            self.best_schedule.calculate_fitness(self.subjects, self.teachers)
    
    def selection(self) -> Tuple[Schedule, Schedule]:
        """
        Відбір батьків методом турнірної селекції
        Вибираємо 3 випадкові особини, повертаємо найкращу
        
        Returns:
            Два батьківські розклади
        """
        def tournament():
            contestants = random.sample(self.population, 3)
            return max(contestants, key=lambda s: s.fitness)
        
        parent1 = tournament()
        parent2 = tournament()
        return parent1, parent2
    
    def crossover(self, parent1: Schedule, parent2: Schedule) -> Tuple[Schedule, Schedule]:
        """
        Схрещування (одноточковий кросовер)
        Обмінюємо частини розкладів між батьками
        
        Args:
            parent1: Перший батько
            parent2: Другий батько
            
        Returns:
            Два нащадки
        """
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        # Вибираємо точку розрізу
        cut_point = random.randint(1, min(len(parent1.lessons), len(parent2.lessons)) - 1)
        
        # Створюємо нащадків
        child1 = Schedule(parent1.lessons[:cut_point] + parent2.lessons[cut_point:])
        child2 = Schedule(parent2.lessons[:cut_point] + parent1.lessons[cut_point:])
        
        return child1, child2
    
    def mutate(self, schedule: Schedule):
        """
        Мутація - випадкова зміна параметрів уроків
        
        Args:
            schedule: Розклад для мутації
        """
        for lesson in schedule.lessons:
            if random.random() < self.mutation_rate:
                # Вибираємо що мутувати
                mutation_type = random.randint(1, 3)
                
                if mutation_type == 1:
                    # Змінюємо день
                    lesson.day = random.choice(self.days)
                elif mutation_type == 2:
                    # Змінюємо час
                    lesson.time_slot = random.choice(self.time_slots)
                else:
                    # Змінюємо вчителя (якщо можливо)
                    available_teachers = [
                        t.name for t in self.teachers.values()
                        if t.can_teach(lesson.subject)
                    ]
                    if available_teachers:
                        lesson.teacher = random.choice(available_teachers)
    
    def evolve(self):
        """Еволюція - створення нового покоління"""
        new_population = []
        
        # Елітизм - зберігаємо найкращих
        elite = self.population[:self.elitism_count]
        new_population.extend([s.copy() for s in elite])
        
        # Створюємо решту популяції
        while len(new_population) < self.population_size:
            # Відбір батьків
            parent1, parent2 = self.selection()
            
            # Схрещування
            child1, child2 = self.crossover(parent1, parent2)
            
            # Мутація
            self.mutate(child1)
            self.mutate(child2)
            
            new_population.append(child1)
            if len(new_population) < self.population_size:
                new_population.append(child2)
        
        self.population = new_population
        self._evaluate_population()
        self.generation += 1
    
    def run(self, max_generations: int = 100, target_fitness: float = 9500.0) -> Tuple[List[float], List[float]]:
        """
        Запускає генетичний алгоритм
        
        Args:
            max_generations: Максимальна кількість поколінь
            target_fitness: Цільове значення fitness (зупинитись якщо досягнуто)
            
        Returns:
            (історія найкращого fitness, історія середнього fitness)
        """
        print(f"\n🚀 Запуск генетичного алгоритму")
        print(f"   Популяція: {self.population_size}")
        print(f"   Мутація: {self.mutation_rate * 100}%")
        print(f"   Кросовер: {self.crossover_rate * 100}%")
        print(f"   Макс. поколінь: {max_generations}")
        print(f"   Цільовий fitness: {target_fitness}")
        print()
        
        self.initialize_population()
        
        best_fitness_history = []
        avg_fitness_history = []
        
        for gen in range(max_generations):
            self.evolve()
            
            best_fitness = self.population[0].fitness
            avg_fitness = sum(s.fitness for s in self.population) / len(self.population)
            
            best_fitness_history.append(best_fitness)
            avg_fitness_history.append(avg_fitness)
            
            # Виводимо прогрес кожні 10 поколінь
            if (gen + 1) % 10 == 0 or gen == 0:
                print(f"Покоління {gen + 1:3d} | "
                      f"Найкращий: {best_fitness:6.2f} | "
                      f"Середній: {avg_fitness:6.2f} | "
                      f"Валідний: {'✅' if self.population[0].is_valid() else '❌'}")
            
            # Перевірка досягнення цілі
            if best_fitness >= target_fitness:
                print(f"\n🎯 Досягнуто цільовий fitness {target_fitness}!")
                break
        
        print(f"\n✅ Алгоритм завершено після {self.generation} поколінь")
        print(f"   Найкращий fitness: {self.best_schedule.fitness:.2f}")
        print(f"   Валідний розклад: {'✅ ТАК' if self.best_schedule.is_valid() else '❌ НІ'}")
        
        return best_fitness_history, avg_fitness_history
    
    def get_best_schedule(self) -> Schedule:
        """
        Повертає найкращий знайдений розклад
        
        Returns:
            Найкращий розклад
        """
        return self.best_schedule