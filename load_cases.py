"""
F_L : drag_force

F_D : drive_force

F_B : braking_force

F_C : lateral_force

M_v : motor_torque

M_B : brake_torque

F_b : brake_disc_force

N_f : front_vertical

N_b : rear_vertical

V_i : inner_vertical

V_y : outer_vertical

V_{fi} : front_inner_vertical

V_{fy} : front_outer_vertical

V_{bi} : rear_inner_vertical

V_{by} : rear_outer_vertical

H_f : front_lateral

H_b : rear_lateral

H_{fi} : front_inner_lateral

H_{fy} : front_outer_lateral

H_{bi} : rear_inner_lateral

H_{by} : rear_outer_lateral

d_f+d_b : wheelbase

v_c= gamma * v : cornering_speed

R : corner_radius
"""

import math
from models import Vehicle, ShaftGeometry, WheelForces, BearingForces
from constants import G, AIR_DENSITY

class AccelerationCase:
    def __init__(self, vehicle: Vehicle, shaft: ShaftGeometry):
        self.vehicle = vehicle
        self.shaft = shaft

    def air_drag(self, speed: float) -> float:
        v = self.vehicle
        return (0.5 * AIR_DENSITY
                * v.drag_coefficient
                * v.frontal_area
                * speed**2
            )

    def drive_force(self, speed: float) -> float:
        v = self.vehicle
        return (
            v.mass * v.acceleration + self.air_drag(speed)
        )

    def wheel_forces(self, speed: float) -> WheelForces:
        v = self.vehicle
        drive_force = self.drive_force(speed)
        drag_force = self.air_drag(speed)
        d_total = v.d_front + v.d_back

        rear_vertical = (v.mass * G * v.d_front
               + drive_force * v.cg_height
               - drag_force * v.drag_height_offset
               )/(d_total)
        
        front_vertical = (v.mass * G * v.d_back
               - drive_force * v.cg_height
               + drag_force * v.drag_height_offset
               )/(d_total)

        # Symmetry, for left and right wheel forces
        return WheelForces(
            front_left_vertical=front_vertical / 2,
            front_right_vertical=front_vertical / 2,

            rear_left_vertical=rear_vertical / 2,
            rear_right_vertical=rear_vertical / 2,

            rear_left_longitudinal=drive_force / 2,
            rear_right_longitudinal=drive_force / 2
        )

    def motor_torque(self, speed: float) -> float:
        drive_force = self.drive_force(speed)
        wheel_radius = self.shaft.wheel_diameter / 2
        return drive_force * wheel_radius

    def sprocket_force(self, speed: float) -> float:
        motor_torque = self.motor_torque(speed)
        return motor_torque / self.shaft.sprocket_radius

    def bearing_forces(self, speed: float) -> float:
        forces = self.wheel_forces(speed)

        return BearingForces( 
            left_vertical=forces.rear_left_vertical,
            right_vertical=forces.rear_right_vertical
        ) # Osäker på denna

class BrakingCase:
    def __init__(self, vehicle: Vehicle, shaft: ShaftGeometry):
        self.vehicle = vehicle
        self.shaft = shaft

    def air_drag(self) -> float:
        v = self.vehicle
        speed = v.max_speed # braking from top speed
        return (0.5 * AIR_DENSITY
                * v.drag_coefficient
                * v.frontal_area
                * speed**2
            )

    def braking_force(self) -> float:
        v = self.vehicle

        return (v.mass * v.deceleration
                - self.air_drag())

    def wheel_forces(self) -> WheelForces:
        v = self.vehicle
        braking_force = self.braking_force()
        drag_force = self.air_drag()
        d_total = v.d_front + v.d_back

        rear_vertical = (v.mass * G * v.d_front
               - braking_force * v.cg_height
               - drag_force * v.drag_height_offset
               )/(d_total)
        
        front_vertical = (v.mass * G * v.d_back
               + braking_force * v.cg_height
               + drag_force * v.drag_height_offset
               )/(d_total)

        # Symmetry, for left and right wheel forces
        return WheelForces(
            front_left_vertical=front_vertical / 2,
            front_right_vertical=front_vertical / 2,

            rear_left_vertical=rear_vertical / 2,
            rear_right_vertical=rear_vertical / 2,

            rear_left_longitudinal=-braking_force / 2,
            rear_right_longitudinal=-braking_force / 2
        )

    def brake_torque(self) -> float:
        braking_force = self.braking_force()
        wheel_radius = self.shaft.wheel_diameter / 2

        return braking_force * wheel_radius

    def brake_disc_torque(self) -> float:
        total_torque = self.brake_torque()
        return total_torque / 2

    def brake_disc_force(self) -> float:
        s = self.shaft
        brake_disc_torque = self.brake_disc_torque()

        return brake_disc_torque / s.brake_radius # Osäker på denna


class CorneringCase:
    def __init__(self, vehicle: Vehicle, shaft: ShaftGeometry):
        self.vehicle = vehicle
        self.shaft = shaft

    def max_gamma(self) -> float:
        v = self.vehicle
        s = self.shaft

        gamma = (
            math.sqrt(G * s.length * v.corner_radius / (2 * v.cg_height))
            / v.max_speed)
        
        return min(gamma, 1.0)

    def cornering_speed(self) -> float:
        return self.max_gamma() * self.vehicle.max_speed

    def lateral_force(self) -> float:
        v = self.vehicle
        speed = self.cornering_speed()
        
        return (
            v.mass
            * speed ** 2
            / v.corner_radius
        )

    def wheel_forces(self) -> WheelForces:
        vehicle = self.vehicle
        shaft = self.shaft

        drag_force = self.air_drag()

        drive_force = drag_force

        lateral_force = self.lateral_force()

        wheelbase = vehicle.d_front + vehicle.d_back

        rear_vertical = (
            vehicle.mass * G * vehicle.d_front
            + drive_force * vehicle.cg_height
            - drag_force * vehicle.drag_height_offset
        ) / wheelbase

        front_vertical = (
            vehicle.mass * G * vehicle.d_back
            - drive_force * vehicle.cg_height
            + drag_force * vehicle.drag_height_offset
        ) / wheelbase

        inner_vertical = (
            vehicle.mass * G / 2
            - lateral_force * vehicle.cg_height / shaft.length
        )

        outer_vertical = (
            vehicle.mass * G / 2
            + lateral_force * vehicle.cg_height / shaft.length
        )

        front_inner_vertical = (
            inner_vertical
            * front_vertical
            / (vehicle.mass * G)
        )

        rear_inner_vertical = (
            inner_vertical
            * rear_vertical
            / (vehicle.mass * G)
        )

        front_outer_vertical = (
            outer_vertical
            * front_vertical
            / (vehicle.mass * G)
        )

        rear_outer_vertical = (
            outer_vertical
            * rear_vertical
            / (vehicle.mass * G)
        )

        front_lateral = (
            lateral_force
            * vehicle.d_back
            / wheelbase
        )

        rear_lateral = (
            lateral_force
            * vehicle.d_front
            / wheelbase
        )

        front_inner_lateral = (
            front_lateral
            * front_inner_vertical
            / (front_inner_vertical + front_outer_vertical)
        )

        front_outer_lateral = (
            front_lateral
            * front_outer_vertical
            / (front_inner_vertical + front_outer_vertical)
        )

        rear_inner_lateral = (
            rear_lateral
            * rear_inner_vertical
            / (rear_inner_vertical + rear_outer_vertical)
        )

        rear_outer_lateral = (
            rear_lateral
            * rear_inner_vertical
            / (rear_inner_vertical + rear_outer_vertical)
        )
        return WheelForces(
            front_left_vertical=front_inner_vertical,
            front_right_vertical=front_outer_vertical,

            rear_left_vertical=rear_inner_vertical,
            rear_right_vertical=rear_outer_vertical,

            rear_left_longitudinal=drive_force / 2,
            rear_right_longitudinal=drive_force / 2,

            front_left_lateral=front_inner_lateral,
            front_right_lateral=front_outer_lateral,

            rear_left_lateral=rear_inner_lateral,
            rear_right_lateral=rear_outer_lateral,
        )

    def air_drag(self) -> float:
        v = self.vehicle
        speed = self.cornering_speed()

        return (
            0.5
            * AIR_DENSITY
            * v.drag_coefficient
            * v.frontal_area
            * speed**2
        )

    def motor_torque(self) -> float:
        drive_force = self.air_drag()
        wheel_radius = self.shaft.wheel_diameter / 2

        return drive_force * wheel_radius
