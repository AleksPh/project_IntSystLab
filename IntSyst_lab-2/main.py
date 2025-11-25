"""
Демонстрація системи онтології міського життя
Запуск: python main.py
"""
from entities import (
    Teacher, Driver, Dog, Cat,
    Apartment, School, Hospital,
    Car, Bus, Engine, Wheel,
    Tail, Fur
)
from query import OntologyQuery


def create_world():
    """Створює світ з сутностями та відношеннями"""
    print("=" * 70)
    print("🏙️  ОНТОЛОГІЯ МІСЬКОГО ЖИТТЯ")
    print("=" * 70)
    print("\n📦 Створення світу...")
    
    # ========================================================================
    # ЛЮДИ
    # ========================================================================
    teacher = Teacher("Марія Іванівна", 35, "Математика")
    driver = Driver("Петро", 42, "D")
    
    # ========================================================================
    # ТВАРИНИ
    # ========================================================================
    dog = Dog("Рекс", 5, "Німецька вівчарка")
    cat = Cat("Мурчик", 3, "Рудий")
    
    # ========================================================================
    # ЧАСТИНИ ТІЛА
    # ========================================================================
    dog_tail = Tail("Хвіст Рекса", 30)
    dog_fur = Fur("Шерсть Рекса", "Коричнева")
    cat_tail = Tail("Хвіст Мурчика", 25)
    cat_fur = Fur("Шерсть Мурчика", "Руда")
    
    # ========================================================================
    # БУДІВЛІ
    # ========================================================================
    school = School("Школа №5", "вул. Шевченка, 10", 3, 500)
    hospital = Hospital("Міська лікарня", "вул. Грушевського, 15", 5, 200)
    apartment = Apartment("Квартира 42", "вул. Лесі Українки, 5", 7, 3)
    
    # ========================================================================
    # ТРАНСПОРТ
    # ========================================================================
    car = Car("BMW X5", 210, "BMW")
    bus = Bus("Маршрут 23", 90, 40)
    
    # ========================================================================
    # МЕХАНІЧНІ ЧАСТИНИ
    # ========================================================================
    car_engine = Engine("Двигун BMW", "Алюміній", 300)
    bus_engine = Engine("Двигун автобуса", "Сталь", 250)
    
    wheel1 = Wheel("Колесо 1", 18)
    wheel2 = Wheel("Колесо 2", 18)
    wheel3 = Wheel("Колесо 3", 18)
    wheel4 = Wheel("Колесо 4", 18)
    
    # ========================================================================
    # HAS-A ВІДНОШЕННЯ (композиція)
    # ========================================================================
    
    # Тварини мають частини тіла
    dog.add_part(dog_tail)
    dog_tail.add_part(dog_fur)
    
    cat.add_part(cat_tail)
    cat_tail.add_part(cat_fur)
    
    # Транспорт має частини
    car.add_part(car_engine)
    car.add_part(wheel1)
    car.add_part(wheel2)
    
    bus.add_part(bus_engine)
    bus.add_part(wheel3)
    bus.add_part(wheel4)
    
    # ========================================================================
    # USES ВІДНОШЕННЯ (асоціація)
    # ========================================================================
    
    # Вчитель використовує школу
    teacher.add_usage(school)
    
    # Водій використовує транспорт
    driver.add_usage(bus)
    driver.add_usage(car)
    
    # Людина використовує будівлі
    teacher.add_usage(apartment)
    driver.add_usage(hospital)
    
    from base import Entity
    print(f"✅ Створено {len(Entity.get_all_instances())} сутностей")
    
    return {
        'people': [teacher, driver],
        'animals': [dog, cat],
        'buildings': [school, hospital, apartment],
        'vehicles': [car, bus],
        'parts': [dog_tail, dog_fur, cat_tail, cat_fur, 
                 car_engine, bus_engine, wheel1, wheel2, wheel3, wheel4]
    }


def demo_basic_queries():
    """Демонстрація базових запитів"""
    print("\n" + "=" * 70)
    print("🔍 БАЗОВІ ЗАПИТИ")
    print("=" * 70)
    
    # Запит 1: Чи пов'язана собака з шерстю?
    OntologyQuery.find_connection("Рекс", "Шерсть Рекса")
    
    # Запит 2: Чи пов'язаний водій з двигуном?
    OntologyQuery.find_connection("Петро", "Двигун BMW")
    
    # Запит 3: Чи пов'язаний вчитель зі школою?
    OntologyQuery.find_connection("Марія Іванівна", "Школа №5")
    
    # Запит 4: Чи пов'язаний кіт з машиною? (має бути НІ)
    OntologyQuery.find_connection("Мурчик", "BMW X5")


def demo_hierarchy():
    """Демонстрація ієрархій"""
    print("\n" + "=" * 70)
    print("📊 ІЄРАРХІЇ КЛАСІВ (IS-A відношення)")
    print("=" * 70)
    
    OntologyQuery.show_hierarchy("Рекс")
    OntologyQuery.show_hierarchy("BMW X5")
    OntologyQuery.show_hierarchy("Марія Іванівна")
    OntologyQuery.show_hierarchy("Двигун BMW")


def demo_composition():
    """Демонстрація композиції"""
    print("\n" + "=" * 70)
    print("🔧 КОМПОЗИЦІЯ (HAS-A відношення)")
    print("=" * 70)
    
    OntologyQuery.show_parts("Рекс")
    OntologyQuery.show_parts("BMW X5")
    OntologyQuery.show_parts("Маршрут 23")


def demo_usage():
    """Демонстрація використання"""
    print("\n" + "=" * 70)
    print("🔗 ВИКОРИСТАННЯ (USES відношення)")
    print("=" * 70)
    
    OntologyQuery.show_usage("Марія Іванівна")
    OntologyQuery.show_usage("Петро")


def demo_complex_queries():
    """Демонстрація складних запитів"""
    print("\n" + "=" * 70)
    print("🌐 СКЛАДНІ ЗАПИТИ")
    print("=" * 70)
    
    # Аналіз сутності
    OntologyQuery.analyze_entity("Рекс")
    
    # Всі зв'язки від сутності
    OntologyQuery.find_all_connections("Петро", max_depth=3)


def demo_statistics():
    """Показує статистику онтології"""
    OntologyQuery.statistics()


def demo_custom_queries():
    """Демонстрація користувацьких запитів"""
    print("\n" + "=" * 70)
    print("💡 КОРИСТУВАЦЬКІ ЗАПИТИ")
    print("=" * 70)
    
    # Приклад 1: Чи є собака ссавцем? (через IS-A)
    print("\n❓ Чи є Рекс ссавцем (Animal)?")
    from base import Entity
    dog = Entity.get_instance("Рекс")
    from entities import Animal
    if isinstance(dog, Animal):
        print("✅ ТАК, Рекс є екземпляром Animal (через IS-A)")
    
    # Приклад 2: Скільки коліс у машини?
    print("\n❓ Скільки частин у BMW X5?")
    car = Entity.get_instance("BMW X5")
    parts_count = len(car.has_parts)
    print(f"✅ У BMW X5 є {parts_count} частини:")
    for part in car.has_parts:
        print(f"   • {part.name}")
    
    # Приклад 3: Які будівлі використовує вчитель?
    print("\n❓ Які будівлі використовує Марія Іванівна?")
    teacher = Entity.get_instance("Марія Іванівна")
    from entities import Building
    buildings = [e for e in teacher.uses_entities if isinstance(e, Building)]
    if buildings:
        print(f"✅ Марія Іванівна використовує {len(buildings)} будівлю:")
        for building in buildings:
            print(f"   • {building.describe()}")
    
    # Приклад 4: Який транспорт використовує водій?
    print("\n❓ Який транспорт використовує Петро?")
    driver = Entity.get_instance("Петро")
    from entities import Vehicle
    vehicles = [e for e in driver.uses_entities if isinstance(e, Vehicle)]
    if vehicles:
        print(f"✅ Петро використовує {len(vehicles)} транспортних засоби:")
        for vehicle in vehicles:
            print(f"   • {vehicle.describe()}")


def interactive_mode():
    """Інтерактивний режим запитів"""
    print("\n" + "=" * 70)
    print("💬 ІНТЕРАКТИВНИЙ РЕЖИМ")
    print("=" * 70)
    print("\nКоманди:")
    print("  find <сутність1> <сутність2> - знайти зв'язок")
    print("  hierarchy <сутність>         - показати ієрархію")
    print("  parts <сутність>             - показати частини")
    print("  uses <сутність>              - показати використання")
    print("  analyze <сутність>           - повний аналіз")
    print("  list                         - список всіх сутностей")
    print("  stats                        - статистика")
    print("  exit                         - вихід")
    
    while True:
        try:
            cmd = input("\n> ").strip().lower()
            
            if not cmd:
                continue
            
            if cmd == "exit":
                print("До побачення! 👋")
                break
            
            elif cmd == "list":
                OntologyQuery.show_all_entities(group_by_type=True)
            
            elif cmd == "stats":
                OntologyQuery.statistics()
            
            elif cmd.startswith("find "):
                parts = cmd.split()
                if len(parts) >= 3:
                    from base import Entity
                    entity1 = " ".join(parts[1:-1])
                    entity2 = parts[-1]
                    # Спробуємо знайти з великої літери
                    entities = {e.name.lower(): e.name for e in Entity.get_all_instances()}
                    entity1_real = entities.get(entity1.lower(), entity1)
                    entity2_real = entities.get(entity2.lower(), entity2)
                    OntologyQuery.find_connection(entity1_real, entity2_real)
                else:
                    print("❌ Використання: find <сутність1> <сутність2>")
            
            elif cmd.startswith("hierarchy "):
                from base import Entity
                entity_name = cmd[10:].strip()
                entities = {e.name.lower(): e.name for e in Entity.get_all_instances()}
                entity_real = entities.get(entity_name.lower(), entity_name)
                OntologyQuery.show_hierarchy(entity_real)
            
            elif cmd.startswith("parts "):
                from base import Entity
                entity_name = cmd[6:].strip()
                entities = {e.name.lower(): e.name for e in Entity.get_all_instances()}
                entity_real = entities.get(entity_name.lower(), entity_name)
                OntologyQuery.show_parts(entity_real)
            
            elif cmd.startswith("uses "):
                from base import Entity
                entity_name = cmd[5:].strip()
                entities = {e.name.lower(): e.name for e in Entity.get_all_instances()}
                entity_real = entities.get(entity_name.lower(), entity_name)
                OntologyQuery.show_usage(entity_real)
            
            elif cmd.startswith("analyze "):
                from base import Entity
                entity_name = cmd[8:].strip()
                entities = {e.name.lower(): e.name for e in Entity.get_all_instances()}
                entity_real = entities.get(entity_name.lower(), entity_name)
                OntologyQuery.analyze_entity(entity_real)
            
            else:
                print("❌ Невідома команда. Введіть 'exit' для виходу.")
        
        except KeyboardInterrupt:
            print("\n\nДо побачення! 👋")
            break
        except Exception as e:
            print(f"❌ Помилка: {e}")


def main():
    """Головна функція"""
    # Створюємо світ
    world = create_world()
    
    # Показуємо всі сутності
    OntologyQuery.show_all_entities(group_by_type=True)
    
    # Демонстрація різних запитів
    demo_basic_queries()
    demo_hierarchy()
    demo_composition()
    demo_usage()
    demo_complex_queries()
    demo_custom_queries()
    demo_statistics()
    
    # Інтерактивний режим (опціонально)
    print("\n" + "=" * 70)
    response = input("Запустити інтерактивний режим? (y/n): ").strip().lower()
    if response == 'y':
        interactive_mode()
    
    print("\n" + "=" * 70)
    print("✅ Демонстрація завершена!")
    print("=" * 70)


if __name__ == "__main__":
    main()