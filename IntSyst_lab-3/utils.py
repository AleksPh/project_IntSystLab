"""
Допоміжні функції для системи генерації розкладу
"""
from typing import List, Tuple
from models import Class, Teacher, Subject, Schedule, DayOfWeek


def create_school_data() -> Tuple[List[Class], List[Teacher], List[Subject]]:
    """
    Створює тестові дані школи
    
    Returns:
        (список класів, список вчителів, список предметів)
    """
    
    # Предмети
    subjects = [
        Subject("Математика", 4, 3),      # 4 рази на тиждень, важкий
        Subject("Українська мова", 3, 2),
        Subject("Англійська мова", 3, 2),
        Subject("Фізика", 2, 3),
        Subject("Хімія", 2, 3),
        Subject("Біологія", 2, 2),
        Subject("Історія", 2, 2),
        Subject("Географія", 1, 1),
        Subject("Фізкультура", 3, 1),
        Subject("Інформатика", 2, 2),
    ]
    
    # Вчителі
    teachers = [
        Teacher("Петренко І.П.", ["Математика", "Інформатика"], 
                [DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY, DayOfWeek.FRIDAY]),
        Teacher("Іваненко О.М.", ["Українська мова", "Історія"]),
        Teacher("Коваленко С.В.", ["Англійська мова"]),
        Teacher("Сидоренко Л.А.", ["Фізика", "Інформатика"]),
        Teacher("Мельник В.І.", ["Хімія", "Біологія"]),
        Teacher("Шевченко Н.П.", ["Географія", "Біологія"]),
        Teacher("Морозов А.С.", ["Фізкультура"]),
    ]
    
    # Класи
    classes = [
        Class("10-А"),
        Class("10-Б"),
        Class("11-А"),
    ]
    
    return classes, teachers, subjects


def print_schedule(schedule: Schedule, days: List[DayOfWeek]):
    """
    Виводить розклад у зручному форматі
    
    Args:
        schedule: Розклад для виведення
        days: Список днів тижня
    """
    if not schedule:
        print("Немає розкладу для відображення")
        return
    
    print("\n" + "=" * 80)
    print(f"📅 РОЗКЛАД (Fitness: {schedule.fitness:.2f})")
    print("=" * 80)
    
    # Групуємо по класах та днях
    schedule_by_class = {}
    for lesson in schedule.lessons:
        if lesson.class_name not in schedule_by_class:
            schedule_by_class[lesson.class_name] = {}
        if lesson.day not in schedule_by_class[lesson.class_name]:
            schedule_by_class[lesson.class_name][lesson.day] = []
        schedule_by_class[lesson.class_name][lesson.day].append(lesson)
    
    # Виводимо для кожного класу
    for class_name in sorted(schedule_by_class.keys()):
        print(f"\n📚 {class_name}")
        print("-" * 80)
        
        for day in days:
            if day in schedule_by_class[class_name]:
                lessons = sorted(schedule_by_class[class_name][day], 
                               key=lambda l: l.time_slot)
                print(f"\n  {day.value}:")
                for lesson in lessons:
                    print(f"    {lesson.time_slot}. {lesson.subject:15s} - {lesson.teacher}")


def print_schedule_statistics(schedule: Schedule):
    """
    Виводить статистику про розклад
    
    Args:
        schedule: Розклад для аналізу
    """
    print("\n" + "=" * 80)
    print("📊 СТАТИСТИКА РОЗКЛАДУ")
    print("=" * 80)
    
    # Загальна інформація
    print(f"\n📋 Загальна інформація:")
    print(f"   Всього уроків: {len(schedule.lessons)}")
    print(f"   Fitness: {schedule.fitness:.2f}")
    print(f"   Валідний: {'✅ ТАК' if schedule.is_valid() else '❌ НІ'}")
    
    # Кількість конфліктів
    conflicts = 0
    for i, lesson1 in enumerate(schedule.lessons):
        for lesson2 in schedule.lessons[i+1:]:
            if lesson1.conflicts_with(lesson2):
                conflicts += 1
    print(f"   Конфлікти: {conflicts}")
    
    # Вікна в розкладі
    windows = schedule._count_windows()
    print(f"   Вікна: {windows}")
    
    # Розподіл по днях
    print(f"\n📅 Розподіл по днях:")
    days_count = {}
    for lesson in schedule.lessons:
        days_count[lesson.day] = days_count.get(lesson.day, 0) + 1
    
    for day in DayOfWeek:
        count = days_count.get(day, 0)
        print(f"   {day.value:12s}: {count:2d} уроків")
    
    # Навантаження вчителів
    print(f"\n👨‍🏫 Навантаження вчителів:")
    teacher_load = {}
    for lesson in schedule.lessons:
        teacher_load[lesson.teacher] = teacher_load.get(lesson.teacher, 0) + 1
    
    for teacher, count in sorted(teacher_load.items(), key=lambda x: x[1], reverse=True):
        print(f"   {teacher:20s}: {count:2d} уроків")
    
    # Навантаження класів
    print(f"\n🎓 Навантаження класів:")
    class_load = {}
    for lesson in schedule.lessons:
        class_load[lesson.class_name] = class_load.get(lesson.class_name, 0) + 1
    
    for class_name, count in sorted(class_load.items()):
        print(f"   {class_name:10s}: {count:2d} уроків")
    
    print("\n" + "=" * 80)


def compare_schedules(schedule1: Schedule, schedule2: Schedule):
    """
    Порівнює два розклади
    
    Args:
        schedule1: Перший розклад
        schedule2: Другий розклад
    """
    print("\n" + "=" * 80)
    print("🔄 ПОРІВНЯННЯ РОЗКЛАДІВ")
    print("=" * 80)
    
    print(f"\nРозклад 1:")
    print(f"   Fitness: {schedule1.fitness:.2f}")
    print(f"   Уроки: {len(schedule1.lessons)}")
    print(f"   Валідний: {'✅' if schedule1.is_valid() else '❌'}")
    print(f"   Вікна: {schedule1._count_windows()}")
    
    print(f"\nРозклад 2:")
    print(f"   Fitness: {schedule2.fitness:.2f}")
    print(f"   Уроки: {len(schedule2.lessons)}")
    print(f"   Валідний: {'✅' if schedule2.is_valid() else '❌'}")
    print(f"   Вікна: {schedule2._count_windows()}")
    
    print(f"\nПорівняння:")
    diff = schedule1.fitness - schedule2.fitness
    if diff > 0:
        print(f"   ✅ Розклад 1 кращий на {diff:.2f} балів")
    elif diff < 0:
        print(f"   ✅ Розклад 2 кращий на {abs(diff):.2f} балів")
    else:
        print(f"   ⚖️  Розклади однакові")
    
    print("\n" + "=" * 80)


def export_schedule_to_text(schedule: Schedule, filename: str):
    """
    Експортує розклад у текстовий файл
    
    Args:
        schedule: Розклад для експорту
        filename: Ім'я файлу
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(f"РОЗКЛАД ЗАНЯТЬ (Fitness: {schedule.fitness:.2f})\n")
        f.write("=" * 80 + "\n\n")
        
        # Групуємо по класах та днях
        schedule_by_class = {}
        for lesson in schedule.lessons:
            if lesson.class_name not in schedule_by_class:
                schedule_by_class[lesson.class_name] = {}
            if lesson.day not in schedule_by_class[lesson.class_name]:
                schedule_by_class[lesson.class_name][lesson.day] = []
            schedule_by_class[lesson.class_name][lesson.day].append(lesson)
        
        # Виводимо для кожного класу
        for class_name in sorted(schedule_by_class.keys()):
            f.write(f"\n{class_name}\n")
            f.write("-" * 80 + "\n")
            
            for day in DayOfWeek:
                if day in schedule_by_class[class_name]:
                    lessons = sorted(schedule_by_class[class_name][day], 
                                   key=lambda l: l.time_slot)
                    f.write(f"\n  {day.value}:\n")
                    for lesson in lessons:
                        f.write(f"    {lesson.time_slot}. {lesson.subject:15s} - {lesson.teacher}\n")
        
        f.write("\n" + "=" * 80 + "\n")
    
    print(f"✅ Розклад експортовано у файл: {filename}")