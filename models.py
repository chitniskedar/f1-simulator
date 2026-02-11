from dataclasses import dataclass

@dataclass
class Driver:
    name: str
    quali_skill: float
    race_pace: float
    tyre_management: float
    overtaking: float
    consistency: float
    aggression: float


@dataclass
class Car:
    team: str
    raw_performance: float
    straight_line_speed: float
    downforce: float
    reliability: float


@dataclass
class Track:
    name: str
    base_quali_time: float
    base_race_time: float
    degradation_level: float
    overtaking_difficulty: float
    safety_car_probability: float
