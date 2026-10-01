from models import Vehicle, ShaftGeometry
from load_cases import AccelerationCase, BrakingCase


vehicle = Vehicle(
    mass=150.0,
    max_speed=100 / 3.6,
    acceleration=6.0,
    deceleration=15.0,

    drag_coefficient=0.30,
    frontal_area=0.50,

    d_front=0.80,
    d_back=0.30,
    cg_height=0.45,
    drag_height_offset=0.20
)


shaft = ShaftGeometry(
    length=1.10,
    bearing_position=0.15,

    wheel_diameter=0.32,

    brake_position=0.10,
    brake_radius=0.08,

    sprocket_position=0.25,
    sprocket_radius=0.10,

    shaft_diameter=0.03,
    fillet_radius=0.002
)


case = AccelerationCase(vehicle, shaft)

speed = 10.0  # m/s

print("Air drag:", case.air_drag(speed), "N")
print("Drive force:", case.drive_force(speed), "N")

forces = case.wheel_forces(speed)

print("\nWheel forces:")
print(forces)

print("\nMotor torque:", case.motor_torque(speed), "Nm")
print("\nSprocket torque:", case.sprocket_force(speed), "Nm")


braking = BrakingCase(vehicle, shaft)

speed = vehicle.max_speed

print("\n--- BRAKING CASE ---")
print("Speed:", speed, "m/s")
print("Air drag:", braking.air_drag(speed), "N")
print("Braking force:", braking.braking_force(speed), "N")

forces = braking.wheel_forces(speed)

print("\nWheel forces:")
print(forces)

print("\nTotal brake torque:",
      braking.brake_torque(speed), "Nm")

print("Torque per brake disc:",
      braking.brake_disc_torque(speed), "Nm")

print("Force per brake disc:",
      braking.brake_disc_force(speed), "N")