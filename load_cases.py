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
        F_D = self.drive_force(speed)
        F_L = self.air_drag(speed)
        d_total = v.d_front + v.d_back

        N_b = (v.mass * G * v.d_front
               + F_D * v.cg_height
               - F_L * v.drag_height_offset
               )/(d_total)
        
        N_f = (v.mass * G * v.d_back
               - F_D * v.cg_height
               + F_L * v.drag_height_offset
               )/(d_total)

        # Symmetry, for left and right wheel forces
        return WheelForces(
            front_left_vertical=N_f / 2,
            front_right_vertical=N_f / 2,

            rear_left_vertical=N_b / 2,
            rear_right_vertical=N_b / 2,

            rear_left_longitudinal=F_D / 2,
            rear_right_longitudinal=F_D / 2
        )

    def motor_torque(self, speed: float) -> float:
        F_D = self.drive_force(speed)
        wheel_radius = self.shaft.wheel_diameter / 2
        return F_D * wheel_radius

    def sprocket_force(self, speed: float) -> float:
        M_v = self.motor_torque(speed)
        return M_v / self.shaft.sprocket_radius

    def bearing_forces(self, speed: float) -> float:
        forces = self.wheel_forces(speed)

        return BearingForces(
            left_vertical=forces.rear_left_vertical,
            right_vertical=forces.rear_right_vertical
        )

class BrakingCase:
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

    def braking_force(self, speed: float) -> float:
        v = self.vehicle

        return (v.mass * v.deceleration
                - self.air_drag(speed))

    def wheel_forces(self, speed: float) -> WheelForces:
        v = self.vehicle
        F_B = self.braking_force(speed)
        F_L = self.air_drag(speed)
        d_total = v.d_front + v.d_back

        N_b = (v.mass * G * v.d_front
               - F_B * v.cg_height
               - F_L * v.drag_height_offset
               )/(d_total)
        
        N_f = (v.mass * G * v.d_back
               + F_B * v.cg_height
               + F_L * v.drag_height_offset
               )/(d_total)

        # Symmetry, for left and right wheel forces
        return WheelForces(
            front_left_vertical=N_f / 2,
            front_right_vertical=N_f / 2,

            rear_left_vertical=N_b / 2,
            rear_right_vertical=N_b / 2,

            rear_left_longitudinal=-F_B / 2,
            rear_right_longitudinal=-F_B / 2
        )

    def brake_torque(self, speed: float) -> float:
        F_B = self.braking_force(speed)
        wheel_radius = self.shaft.wheel_diameter / 2

        return F_B * wheel_radius

    def brake_disc_torque(self, speed: float) -> float:
        total_torque = self.brake_torque(speed)
        return total_torque / 2

    def brake_disc_force(self, speed: float) -> float:
        s = self.shaft
        brake_disc_torque = self.brake_disc_torque(speed)

        return brake_disc_torque / s.brake_radius
