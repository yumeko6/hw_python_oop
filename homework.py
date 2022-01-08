from typing import List, Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float) -> None:
        self.training_type = training_type
        self.distance = format(distance, '.3f')
        self.duration = format(duration, '.3f')
        self.speed = format(speed, '.3f')
        self.calories = format(calories, '.3f')

    def get_message(self) -> str:
        info = (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потрачено ккал: {self.calories}.')
        return info
        pass


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: float = 1000
    H_IN_MIN: float = 60
    LEN_STEP: float = 0.65
    coeff_calorie_running_1: float = 18
    coeff_calorie_running_2: float = 20
    coeff_calorie_walking_1: float = 0.035
    coeff_calorie_walking_2: float = 0.029
    coeff_calorie_swimming_1: float = 1.1
    coeff_calorie_general: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / Training.M_IN_KM
        return distance
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())
        return info
        pass


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        # Формула: (18 * средняя_скорость - 20) *
        # вес_спортсмена / M_IN_KM * время_тренировки_в_минутах
        calories: float = ((Training.coeff_calorie_running_1
                            * self.get_mean_speed()
                            - Training.coeff_calorie_running_2)
                           * self.weight
                           / Training.M_IN_KM
                           * (self.duration * self.H_IN_MIN))
        return calories

    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action, duration, weight, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        # Формула: (0.035 * вес + (средняя_скорость**2 // рост) *
        # 0.029 * вес) * время_тренировки_в_минутах
        calories: float = ((Training.coeff_calorie_walking_1
                            * self.weight + (self.get_mean_speed()
                                             ** Training.coeff_calorie_general
                                             // self.height)
                            * Training.coeff_calorie_walking_2 * self.weight)
                           * self.duration * self.H_IN_MIN)
        return calories

    pass


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self, action, duration, weight, length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed: float = (self.length_pool * self.count_pool
                             / Training.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        # Формула: (средняя_скорость + 1.1) * 2 * вес
        calories: float = ((self.get_mean_speed()
                            + Training.coeff_calorie_swimming_1)
                           * Training.coeff_calorie_general * self.weight)
        return calories

    pass


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_type[workout_type](*data)
    pass


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
