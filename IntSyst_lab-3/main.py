"""
Головний файл для запуску генетичного алгоритму оптимізації розкладу
Запуск: python main.py
"""
from models import DayOfWeek
from algorithm import GeneticScheduler
from utils import (
    create_school_data, 
    print_schedule, 
    print_schedule_statistics,
    export_schedule_to_text
)


def main():
    """Головна функція програми"""
    print("=" * 80)
    print("🧬 ГЕНЕТИЧНИЙ АЛГОРИТМ - ОПТИМІЗАЦІЯ РОЗКЛАДУ ЗАНЯТЬ")
    print("=" * 80)
    
    # ========================================================================
    # 1. Створюємо дані школи
    # ========================================================================
    classes, teachers, subjects = create_school_data()
    
    print(f"\n📊 Дані школи:")
    print(f"   Класи: {len(classes)}")
    print(f"   Вчителі: {len(teachers)}")
    print(f"   Предмети: {len(subjects)}")
    print(f"   Всього уроків на тиждень: {sum(s.lessons_per_week for s in subjects) * len(classes)}")
    
    # ========================================================================
    # 2. Створюємо генетичний алгоритм
    # ========================================================================
    ga = GeneticScheduler(
        classes=classes,
        teachers=teachers,
        subjects=subjects,
        population_size=100,      # Розмір популяції
        mutation_rate=0.15,       # 15% ймовірність мутації
        crossover_rate=0.8,       # 80% ймовірність схрещування
        elitism_count=10          # 10 найкращих переходять без змін
    )
    
    # ========================================================================
    # 3. Запускаємо алгоритм
    # ========================================================================
    best_history, avg_history = ga.run(
        max_generations=200,      # Максимум 200 поколінь
        target_fitness=9000.0     # Зупинитись якщо досягнуто 9000
    )
    
    # ========================================================================
    # 4. Отримуємо найкращий розклад
    # ========================================================================
    best_schedule = ga.get_best_schedule()
    
    # ========================================================================
    # 5. Виводимо результати
    # ========================================================================
    print_schedule(best_schedule, list(DayOfWeek))
    
    # Детальна статистика
    print_schedule_statistics(best_schedule)
    
    # ========================================================================
    # 6. Експортуємо у файл
    # ========================================================================
    export_schedule_to_text(best_schedule, "schedule_output.txt")
    
    print("\n" + "=" * 80)
    print("✅ Завершено!")
    print("=" * 80)


def demo_comparison():
    """Демонстрація порівняння різних налаштувань алгоритму"""
    from utils import compare_schedules
    
    print("\n" + "=" * 80)
    print("🔬 ДЕМОНСТРАЦІЯ: Порівняння налаштувань")
    print("=" * 80)
    
    classes, teachers, subjects = create_school_data()
    
    # Варіант 1: Мало мутацій
    print("\n📊 Варіант 1: Мало мутацій (5%)")
    ga1 = GeneticScheduler(
        classes=classes, teachers=teachers, subjects=subjects,
        population_size=50, mutation_rate=0.05, crossover_rate=0.8
    )
    ga1.run(max_generations=50, target_fitness=9500.0)
    schedule1 = ga1.get_best_schedule()
    
    # Варіант 2: Багато мутацій
    print("\n📊 Варіант 2: Багато мутацій (25%)")
    ga2 = GeneticScheduler(
        classes=classes, teachers=teachers, subjects=subjects,
        population_size=50, mutation_rate=0.25, crossover_rate=0.8
    )
    ga2.run(max_generations=50, target_fitness=9500.0)
    schedule2 = ga2.get_best_schedule()
    
    # Порівняння
    compare_schedules(schedule1, schedule2)


def demo_evolution():
    """Демонстрація еволюції через багато поколінь"""
    print("\n" + "=" * 80)
    print("🔬 ДЕМОНСТРАЦІЯ: Довга еволюція")
    print("=" * 80)
    
    classes, teachers, subjects = create_school_data()
    
    ga = GeneticScheduler(
        classes=classes, teachers=teachers, subjects=subjects,
        population_size=30,       # Менша популяція
        mutation_rate=0.2,        # Більше мутацій
        crossover_rate=0.7,
        elitism_count=3
    )
    
    # Запускаємо на багато поколінь з високою ціллю
    best_history, avg_history = ga.run(
        max_generations=500, 
        target_fitness=9800.0  
    )
    
    best_schedule = ga.get_best_schedule()
    print_schedule(best_schedule, list(DayOfWeek))
    print_schedule_statistics(best_schedule)


if __name__ == "__main__":
    main()
    