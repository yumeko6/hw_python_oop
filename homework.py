from typing import List, Dict, Type
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        info = (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')
        return info


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: float = 1000
    H_IN_MIN: float = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / Training.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определи get_spent_calories в %s.'
                                  % self.__class__.__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    KAL_RUN_1: float = 18
    KAL_RUN_2: float = 20

    def get_spent_calories(self) -> float:
        calories: float = ((self.KAL_RUN_1 * self.get_mean_speed()
                            - self.KAL_RUN_2) * self.weight
                           / Training.M_IN_KM
                           * (self.duration * self.H_IN_MIN))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    KAL_WLK_1: float = 0.035
    KAL_WLK_2: float = 0.029
    KAL: float = 2

    def __init__(self, action, duration, weight, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories_1: float = self.KAL_WLK_1 * self.weight
        calories_2: float = (self.get_mean_speed() ** self.KAL) // self.height
        calories_3: float = self.KAL_WLK_2 * self.weight
        calories_4: float = self.duration * self.H_IN_MIN
        calories: float = (calories_1 + (calories_2 * calories_3)) * calories_4
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    KAL_SWM: float = 1.1
    KAL: float = 2

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
        calories: float = ((self.get_mean_speed() + self.KAL_SWM)
                           * self.KAL * self.weight)
        return calories


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
