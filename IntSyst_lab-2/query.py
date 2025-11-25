"""
Система запитів до онтології
Виконання складних запитів та аналізу зв'язків
"""
from base import Entity, RelationType
from typing import List, Dict, Set, Optional


class OntologyQuery:
    """Система для виконання запитів до онтології"""
    
    @staticmethod
    def find_connection(entity1_name: str, entity2_name: str, verbose: bool = True) -> tuple[bool, List[str]]:
        """
        Знаходить зв'язок між двома сутностями
        
        Args:
            entity1_name: Ім'я першої сутності
            entity2_name: Ім'я другої сутності
            verbose: Чи виводити детальну інформацію
            
        Returns:
            (чи є зв'язок, шлях зв'язку)
        """
        entity1 = Entity.get_instance(entity1_name)
        entity2 = Entity.get_instance(entity2_name)
        
        if not entity1:
            if verbose:
                print(f"❌ Сутність '{entity1_name}' не знайдена")
            return False, []
        if not entity2:
            if verbose:
                print(f"❌ Сутність '{entity2_name}' не знайдена")
            return False, []
        
        if verbose:
            print(f"\n🔍 Пошук зв'язку: {entity1_name} → {entity2_name}")
            print(f"   {entity1.describe()}")
            print(f"   {entity2.describe()}")
        
        is_related, path = entity1.is_related_to(entity2)
        
        if verbose:
            if is_related:
                print(f"✅ ТАК, є зв'язок!")
                print(f"   Шлях: {' → '.join(path)}")
            else:
                print(f"❌ НІ, зв'язку не знайдено")
        
        return is_related, path
    
    @staticmethod
    def show_hierarchy(entity_name: str) -> None:
        """
        Показує ієрархію класів для сутності (IS-A відношення)
        
        Args:
            entity_name: Ім'я сутності
        """
        entity = Entity.get_instance(entity_name)
        if not entity:
            print(f"❌ Сутність '{entity_name}' не знайдена")
            return
        
        print(f"\n📊 Ієрархія класів для '{entity_name}':")
        classes = [cls.__name__ for cls in entity.__class__.__mro__[:-2]]  # Без object та ABC
        for i, cls_name in enumerate(classes):
            indent = "  " * i
            level = i + 1
            print(f"{indent}└─ Рівень {level}: {cls_name}")
    
    @staticmethod
    def show_parts(entity_name: str, recursive: bool = True) -> None:
        """
        Показує всі частини сутності (HAS-A відношення)
        
        Args:
            entity_name: Ім'я сутності
            recursive: Чи показувати вкладені частини
        """
        entity = Entity.get_instance(entity_name)
        if not entity:
            print(f"❌ Сутність '{entity_name}' не знайдена")
            return
        
        print(f"\n🔧 Частини '{entity_name}':")
        
        if not entity.has_parts:
            print("   (немає частин)")
            return
        
        if recursive:
            parts = entity.get_all_parts()
            for part in parts:
                print(f"   • {part.describe()}")
        else:
            for part in entity.has_parts:
                print(f"   • {part.describe()}")
    
    @staticmethod
    def show_usage(entity_name: str) -> None:
        """
        Показує що використовує сутність (USES відношення)
        
        Args:
            entity_name: Ім'я сутності
        """
        entity = Entity.get_instance(entity_name)
        if not entity:
            print(f"❌ Сутність '{entity_name}' не знайдена")
            return
        
        print(f"\n🔗 '{entity_name}' використовує:")
        
        if not entity.uses_entities:
            print("   (нічого не використовує)")
            return
        
        for used in entity.uses_entities:
            print(f"   • {used.describe()}")
    
    @staticmethod
    def show_all_entities(group_by_type: bool = False) -> None:
        """
        Показує всі створені сутності
        
        Args:
            group_by_type: Чи групувати за типом класу
        """
        entities = Entity.get_all_instances()
        
        if not entities:
            print("\n📋 Немає створених сутностей")
            return
        
        print(f"\n📋 Всі сутності в системі ({len(entities)}):")
        
        if group_by_type:
            # Групуємо за класами
            grouped: Dict[str, List[Entity]] = {}
            for entity in entities:
                class_name = entity.__class__.__name__
                if class_name not in grouped:
                    grouped[class_name] = []
                grouped[class_name].append(entity)
            
            for class_name in sorted(grouped.keys()):
                print(f"\n  [{class_name}]:")
                for entity in grouped[class_name]:
                    print(f"    • {entity.describe()}")
        else:
            for entity in entities:
                print(f"  • {entity.describe()}")
    
    @staticmethod
    def find_all_connections(entity_name: str, max_depth: int = 3) -> Dict[str, List[str]]:
        """
        Знаходить всі зв'язки від даної сутності до інших
        
        Args:
            entity_name: Ім'я сутності
            max_depth: Максимальна глибина пошуку
            
        Returns:
            Словник {ім'я_сутності: шлях_до_неї}
        """
        entity = Entity.get_instance(entity_name)
        if not entity:
            print(f"❌ Сутність '{entity_name}' не знайдена")
            return {}
        
        connections = {}
        all_entities = Entity.get_all_instances()
        
        print(f"\n🌐 Пошук всіх зв'язків від '{entity_name}'...")
        
        for target in all_entities:
            if target == entity:
                continue
            
            is_related, path = entity.is_related_to(target, max_depth)
            if is_related:
                connections[target.name] = path
        
        if connections:
            print(f"✅ Знайдено {len(connections)} зв'язків:")
            for target_name, path in connections.items():
                print(f"   → {target_name}: {' → '.join(path)}")
        else:
            print(f"❌ Не знайдено зв'язків")
        
        return connections
    
    @staticmethod
    def analyze_entity(entity_name: str) -> None:
        """
        Повний аналіз сутності: ієрархія, частини, використання
        
        Args:
            entity_name: Ім'я сутності
        """
        entity = Entity.get_instance(entity_name)
        if not entity:
            print(f"❌ Сутність '{entity_name}' не знайдена")
            return
        
        print("\n" + "=" * 70)
        print(f"📊 ПОВНИЙ АНАЛІЗ СУТНОСТІ: {entity_name}")
        print("=" * 70)
        
        print(f"\n📝 Опис:")
        print(f"   {entity.describe()}")
        
        # Ієрархія IS-A
        OntologyQuery.show_hierarchy(entity_name)
        
        # Частини HAS-A
        OntologyQuery.show_parts(entity_name, recursive=True)
        
        # Використання USES
        OntologyQuery.show_usage(entity_name)
        
        print("\n" + "=" * 70)
    
    @staticmethod
    def find_shortest_path(entity1_name: str, entity2_name: str) -> Optional[List[str]]:
        """
        Знаходить найкоротший шлях між двома сутностями
        
        Args:
            entity1_name: Ім'я першої сутності
            entity2_name: Ім'я другої сутності
            
        Returns:
            Найкоротший шлях або None
        """
        entity1 = Entity.get_instance(entity1_name)
        entity2 = Entity.get_instance(entity2_name)
        
        if not entity1 or not entity2:
            return None
        
        # BFS для пошуку найкоротшого шляху
        from collections import deque
        
        queue = deque([(entity1, [entity1.name])])
        visited = {entity1.name}
        
        while queue:
            current, path = queue.popleft()
            
            if current == entity2:
                return path
            
            # Перевіряємо всі зв'язки
            for part in current.has_parts:
                if part.name not in visited:
                    visited.add(part.name)
                    queue.append((part, path + ["HAS-A", part.name]))
            
            for used in current.uses_entities:
                if used.name not in visited:
                    visited.add(used.name)
                    queue.append((used, path + ["USES", used.name]))
        
        return None
    
    @staticmethod
    def statistics() -> None:
        """Показує статистику онтології"""
        entities = Entity.get_all_instances()
        
        print("\n📈 СТАТИСТИКА ОНТОЛОГІЇ")
        print("=" * 70)
        
        print(f"\n📊 Загальна кількість сутностей: {len(entities)}")
        
        # Підраховуємо за типами
        type_counts: Dict[str, int] = {}
        for entity in entities:
            class_name = entity.__class__.__name__
            type_counts[class_name] = type_counts.get(class_name, 0) + 1
        
        print(f"\n🏷️  Розподіл за типами:")
        for class_name in sorted(type_counts.keys()):
            count = type_counts[class_name]
            print(f"   • {class_name}: {count}")
        
        # Підраховуємо відношення
        has_a_count = sum(len(e.has_parts) for e in entities)
        uses_count = sum(len(e.uses_entities) for e in entities)
        
        print(f"\n🔗 Відношення:")
        print(f"   • HAS-A (композиція): {has_a_count}")
        print(f"   • USES (асоціація): {uses_count}")
        
        # Знаходимо найбільш зв'язані сутності
        print(f"\n⭐ Топ-3 найбільш зв'язаних сутностей:")
        entity_connections = [(e.name, len(e.has_parts) + len(e.uses_entities)) 
                             for e in entities]
        entity_connections.sort(key=lambda x: x[1], reverse=True)
        
        for i, (name, count) in enumerate(entity_connections[:3], 1):
            if count > 0:
                print(f"   {i}. {name}: {count} зв'язків")
        
        print("\n" + "=" * 70)