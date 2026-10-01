from dataclasses import dataclass

# Values must be in SI units

@dataclass
class Vehicle:
    mass: float
    max_speed: float
    acceleration: float
    deceleration: float

    drag_coefficient: float
    frontal_area: float

    d_front: float
    d_back: float
    cg_height: float
    drag_height_offset: float

    corner_radius: float

@dataclass
class ShaftGeometry:
    length: float
    bearing_position: float

    wheel_diameter: float
    brake_position: float
    brake_radius: float

    sprocket_position: float
    sprocket_radius: float

    shaft_diameter: float
    fillet_radius: float

    @property
    def bearing_diameter(self) -> float:
        return 0.6 * self.shaft_diameter

@dataclass
class WheelForces:
    front_left_vertical: float
    front_right_vertical: float

    rear_left_vertical: float
    rear_right_vertical: float

    rear_left_longitudinal: float
    rear_right_longitudinal: float

    front_left_lateral: float = 0
    front_right_lateral: float = 0

    rear_left_lateral: float = 0
    rear_right_lateral: float = 0

@dataclass
class BearingForces:
    left_vertical: float
    right_vertical: float

@dataclass
class Material:
    yield_strength: float
    fatigue_strength: float

@dataclass
class SafteyFactors:
    safety_yield: float
    safety_fatigue: float
