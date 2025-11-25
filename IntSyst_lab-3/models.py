"""
Класи даних для системи генерації розкладу
"""
import copy
from typing import List, Dict
from dataclasses import dataclass
from enum import Enum


class DayOfWeek(Enum):
    """Дні тижня"""
    MONDAY = "Понеділок"
    TUESDAY = "Вівторок"
    WEDNESDAY = "Середа"
    THURSDAY = "Четвер"
    FRIDAY = "П'ятниця"


@dataclass
class Subject:
    """Предмет"""
    name: str
    lessons_per_week: int  # Скільки разів на тиждень
    difficulty: int  # 1-легкий, 2-середній, 3-важкий
    
    def __repr__(self):
        return self.name


@dataclass
class Teacher:
    """Вчитель"""
    name: str
    subjects: List[str]  # Які предмети може викладати
    preferred_days: List[DayOfWeek] = None  # Переважні дні
    
    def can_teach(self, subject: str) -> bool:
        """Перевіряє чи може викладати предмет"""
        return subject in self.subjects
    
    def __repr__(self):
        return self.name


@dataclass
class Class:
    """Клас (група учнів)"""
    name: str
    
    def __repr__(self):
        return self.name


@dataclass
class Lesson:
    """Один урок у розкладі"""
    class_name: str
    teacher: str
    subject: str
    day: DayOfWeek
    time_slot: int  # 1-8 (номер уроку)
    
    def __repr__(self):
        return f"{self.class_name} | {self.subject} | {self.teacher} | {self.day.value} {self.time_slot}"
    
    def conflicts_with(self, other: 'Lesson') -> bool:
        """
        Перевіряє чи конфліктує з іншим уроком
        
        Args:
            other: Інший урок для порівняння
            
        Returns:
            True якщо є конфлікт (той самий час, той самий вчитель або клас)
        """
        if self.day != other.day or self.time_slot != other.time_slot:
            return False
        
        # Один вчитель не може вести 2 уроки одночасно
        if self.teacher == other.teacher:
            return True
        
        # Один клас не може мати 2 уроки одночасно
        if self.class_name == other.class_name:
            return True
        
        return False


class Schedule:
    """
    Розклад (один індивід в популяції)
    Представляє повний розклад занять для всіх класів
    """
    
    def __init__(self, lessons: List[Lesson] = None):
        self.lessons: List[Lesson] = lessons or []
        self.fitness: float = 0.0
    
    def add_lesson(self, lesson: Lesson):
        """Додає урок до розкладу"""
        self.lessons.append(lesson)
    
    def calculate_fitness(self, subjects: Dict[str, Subject], 
                         teachers: Dict[str, Teacher]) -> float:
        """
        Функція пристосованості (fitness function)
        Оцінює якість розкладу
        
        Args:
            subjects: Словник предметів
            teachers: Словник вчителів
            
        Returns:
            Оцінка якості (чим більше - тим краще)
        """
        score = 10000.0  # Стартовий бал
        
        # ====================================================================
        # 1. ЖОРСТКІ ОБМЕЖЕННЯ (великі штрафи)
        # ====================================================================
        
        # Конфлікти (вчитель/клас одночасно в 2 місцях)
        conflicts = 0
        for i, lesson1 in enumerate(self.lessons):
            for lesson2 in self.lessons[i+1:]:
                if lesson1.conflicts_with(lesson2):
                    conflicts += 1
        
        score -= conflicts * 50
        
        # Перевірка що вчитель може викладати предмет
        invalid_assignments = 0
        for lesson in self.lessons:
            teacher = teachers.get(lesson.teacher)
            if teacher and not teacher.can_teach(lesson.subject):
                invalid_assignments += 1
        
        score -= invalid_assignments * 20
        
        # Перевірка кількості уроків предмета на тиждень
        subject_counts = {}
        for lesson in self.lessons:
            key = (lesson.class_name, lesson.subject)
            subject_counts[key] = subject_counts.get(key, 0) + 1
        
        for (class_name, subject_name), count in subject_counts.items():
            subject = subjects.get(subject_name)
            if subject:
                diff = abs(count - subject.lessons_per_week)
                score -= diff * 10
        
        # ====================================================================
        # 2. М'ЯКІ ОБМЕЖЕННЯ (невеликі штрафи за незручності)
        # ====================================================================
        
        # Вікна в розкладі (пропущені часові слоти)
        windows = self._count_windows()
        score -= windows * 5
        
        # Важкі предмети краще на початку дня
        for lesson in self.lessons:
            subject = subjects.get(lesson.subject)
            if subject and subject.difficulty == 3:  # Важкий предмет
                if lesson.time_slot > 4:  # Після обіду
                    score -= 2
        
        # Переваги вчителів за днями
        for lesson in self.lessons:
            teacher = teachers.get(lesson.teacher)
            if teacher and teacher.preferred_days:
                if lesson.day not in teacher.preferred_days:
                    score -= 1
        
        self.fitness = max(0, score)  # Не може бути негативним
        return self.fitness
    
    def _count_windows(self) -> int:
        """
        Рахує кількість вікон (пропущених слотів) у розкладі
        Вікно - це пропущений урок між двома іншими уроками
        
        Returns:
            Кількість вікон
        """
        windows = 0
        
        # Для кожного класу та дня
        class_schedules = {}
        for lesson in self.lessons:
            key = (lesson.class_name, lesson.day)
            if key not in class_schedules:
                class_schedules[key] = []
            class_schedules[key].append(lesson.time_slot)
        
        # Рахуємо вікна
        for slots in class_schedules.values():
            if len(slots) > 1:
                slots_sorted = sorted(slots)
                for i in range(len(slots_sorted) - 1):
                    gap = slots_sorted[i+1] - slots_sorted[i] - 1
                    windows += gap
        
        return windows
    
    def is_valid(self) -> bool:
        """
        Перевіряє чи розклад валідний (немає конфліктів)
        
        Returns:
            True якщо розклад валідний
        """
        for i, lesson1 in enumerate(self.lessons):
            for lesson2 in self.lessons[i+1:]:
                if lesson1.conflicts_with(lesson2):
                    return False
        return True
    
    def copy(self) -> 'Schedule':
        """
        Створює глибоку копію розкладу
        
        Returns:
            Новий об'єкт Schedule з копіями уроків
        """
        new_schedule = Schedule(copy.deepcopy(self.lessons))
        new_schedule.fitness = self.fitness
        return new_schedule
    
    def __repr__(self):
        return f"Schedule(lessons={len(self.lessons)}, fitness={self.fitness:.2f})"