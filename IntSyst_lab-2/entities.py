"""
Конкретні класи онтології
Рівень 3-4: Підкатегорії та конкретні реалізації
"""
from abc import abstractmethod
from base import LivingBeing, Building, Vehicle, Part


# ============================================================================
# РІВЕНЬ 3: Підкатегорії
# ============================================================================

class Human(LivingBeing):
    """РІВЕНЬ 3: Людина"""
    
    def __init__(self, name: str, age: int, profession: str):
        super().__init__(name, age)
        self.profession = profession
    
    def make_sound(self) -> str:
        return f"{self.name} каже: Привіт!"
    
    def describe(self) -> str:
        return f"{self.name} - людина, {self.age} років, професія: {self.profession}"


class Animal(LivingBeing):
    """РІВЕНЬ 3: Тварина"""
    
    def __init__(self, name: str, age: int, species: str):
        super().__init__(name, age)
        self.species = species
    
    @abstractmethod
    def make_sound(self) -> str:
        pass
    
    def describe(self) -> str:
        return f"{self.name} - {self.species}, вік: {self.age}"


class ResidentialBuilding(Building):
    """РІВЕНЬ 3: Житлова будівля"""
    
    def __init__(self, name: str, address: str, floors: int, apartments_count: int):
        super().__init__(name, address, floors)
        self.apartments_count = apartments_count
    
    def describe(self) -> str:
        return f"{self.name} - житловий будинок, {self.apartments_count} квартир"


class PublicBuilding(Building):
    """РІВЕНЬ 3: Громадська будівля"""
    
    def __init__(self, name: str, address: str, floors: int, building_type: str):
        super().__init__(name, address, floors)
        self.building_type = building_type
    
    def describe(self) -> str:
        return f"{self.name} - {self.building_type}"


class GroundVehicle(Vehicle):
    """РІВЕНЬ 3: Наземний транспорт"""
    
    def __init__(self, name: str, max_speed: int, wheels_count: int):
        super().__init__(name, max_speed)
        self.wheels_count = wheels_count
    
    def move(self) -> str:
        return f"{self.name} їде по дорозі"
    
    def describe(self) -> str:
        return f"{self.name} - наземний транспорт, {self.wheels_count} коліс"


class BodyPart(Part):
    """РІВЕНЬ 3: Частина тіла"""
    
    def __init__(self, name: str, material: str, function: str):
        super().__init__(name, material)
        self.function = function
    
    def describe(self) -> str:
        return f"{self.name} - частина тіла, функція: {self.function}"


class MechanicalPart(Part):
    """РІВЕНЬ 3: Механічна частина"""
    
    def __init__(self, name: str, material: str, weight: float):
        super().__init__(name, material)
        self.weight = weight
    
    def describe(self) -> str:
        return f"{self.name} - механічна частина, вага: {self.weight} кг"


# ============================================================================
# РІВЕНЬ 4: Конкретні класи - Люди
# ============================================================================

class Teacher(Human):
    """РІВЕНЬ 4: Вчитель"""
    
    def __init__(self, name: str, age: int, subject: str):
        super().__init__(name, age, "Вчитель")
        self.subject = subject
    
    def teach(self) -> str:
        return f"{self.name} викладає {self.subject}"
    
    def describe(self) -> str:
        return f"{self.name} - вчитель, викладає {self.subject}"


class Driver(Human):
    """РІВЕНЬ 4: Водій"""
    
    def __init__(self, name: str, age: int, license_type: str):
        super().__init__(name, age, "Водій")
        self.license_type = license_type
    
    def drive(self, vehicle: Vehicle) -> str:
        return f"{self.name} керує {vehicle.name}"
    
    def describe(self) -> str:
        return f"{self.name} - водій, категорія: {self.license_type}"


# ============================================================================
# РІВЕНЬ 4: Конкретні класи - Тварини
# ============================================================================

class Dog(Animal):
    """РІВЕНЬ 4: Собака"""
    
    def __init__(self, name: str, age: int, breed: str):
        super().__init__(name, age, "Собака")
        self.breed = breed
    
    def make_sound(self) -> str:
        return f"{self.name} гавкає: Гав-гав!"
    
    def describe(self) -> str:
        return f"{self.name} - собака породи {self.breed}"


class Cat(Animal):
    """РІВЕНЬ 4: Кіт"""
    
    def __init__(self, name: str, age: int, color: str):
        super().__init__(name, age, "Кіт")
        self.color = color
    
    def make_sound(self) -> str:
        return f"{self.name} нявчить: Мяу!"
    
    def describe(self) -> str:
        return f"{self.name} - кіт, колір: {self.color}"


# ============================================================================
# РІВЕНЬ 4: Конкретні класи - Будівлі
# ============================================================================

class Apartment(ResidentialBuilding):
    """РІВЕНЬ 4: Квартира"""
    
    def __init__(self, name: str, address: str, floor: int, rooms: int):
        super().__init__(name, address, floor, 1)
        self.rooms = rooms
    
    def describe(self) -> str:
        return f"{self.name} - квартира, {self.rooms} кімнат, поверх {self.floors}"


class School(PublicBuilding):
    """РІВЕНЬ 4: Школа"""
    
    def __init__(self, name: str, address: str, floors: int, students_count: int):
        super().__init__(name, address, floors, "Школа")
        self.students_count = students_count
    
    def describe(self) -> str:
        return f"{self.name} - школа, {self.students_count} учнів"


class Hospital(PublicBuilding):
    """РІВЕНЬ 4: Лікарня"""
    
    def __init__(self, name: str, address: str, floors: int, beds_count: int):
        super().__init__(name, address, floors, "Лікарня")
        self.beds_count = beds_count
    
    def describe(self) -> str:
        return f"{self.name} - лікарня, {self.beds_count} ліжок"


# ============================================================================
# РІВЕНЬ 4: Конкретні класи - Транспорт
# ============================================================================

class Car(GroundVehicle):
    """РІВЕНЬ 4: Автомобіль"""
    
    def __init__(self, name: str, max_speed: int, brand: str):
        super().__init__(name, max_speed, 4)
        self.brand = brand
    
    def describe(self) -> str:
        return f"{self.name} - автомобіль {self.brand}"


class Bus(GroundVehicle):
    """РІВЕНЬ 4: Автобус"""
    
    def __init__(self, name: str, max_speed: int, capacity: int):
        super().__init__(name, max_speed, 6)
        self.capacity = capacity
    
    def describe(self) -> str:
        return f"{self.name} - автобус, місткість: {self.capacity} пасажирів"


# ============================================================================
# РІВЕНЬ 4: Конкретні класи - Механічні частини
# ============================================================================

class Engine(MechanicalPart):
    """РІВЕНЬ 4: Двигун"""
    
    def __init__(self, name: str, material: str, power: int):
        super().__init__(name, material, 150.0)
        self.power = power
    
    def start(self) -> str:
        return f"{self.name} запущено, потужність {self.power} к.с."
    
    def describe(self) -> str:
        return f"{self.name} - двигун, потужність: {self.power} к.с."


class Wheel(MechanicalPart):
    """РІВЕНЬ 4: Колесо"""
    
    def __init__(self, name: str, diameter: int):
        super().__init__(name, "Гума+Метал", 15.0)
        self.diameter = diameter
    
    def rotate(self) -> str:
        return f"{self.name} обертається"
    
    def describe(self) -> str:
        return f"{self.name} - колесо, діаметр: {self.diameter} дюймів"


# ============================================================================
# РІВЕНЬ 4: Конкретні класи - Частини тіла
# ============================================================================

class Tail(BodyPart):
    """РІВЕНЬ 4: Хвіст"""
    
    def __init__(self, name: str, length: float):
        super().__init__(name, "М'язи та кістки", "Баланс та комунікація")
        self.length = length
    
    def wag(self) -> str:
        return f"{self.name} виляє"
    
    def describe(self) -> str:
        return f"{self.name} - хвіст, довжина: {self.length} см"


class Fur(BodyPart):
    """РІВЕНЬ 4: Шерсть"""
    
    def __init__(self, name: str, color: str):
        super().__init__(name, "Кератин", "Захист та теплоізоляція")
        self.color = color
    
    def shed(self) -> str:
        return f"{self.name} линяє"
    
    def describe(self) -> str:
        return f"{self.name} - шерсть, колір: {self.color}"