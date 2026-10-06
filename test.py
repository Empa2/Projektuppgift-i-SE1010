# test.py

from models import Vehicle, ShaftGeometry
from load_cases import AccelerationCase, BrakingCase, CorneringCase


# ============================================================
# Test parameters
# ============================================================

vehicle = Vehicle(
    mass=150.0,                  # kg
    max_speed=100 / 3.6,         # 100 km/h -> m/s
    acceleration=6.0,            # m/s^2
    deceleration=15.0,           # m/s^2

    drag_coefficient=0.30,
    frontal_area=0.50,           # m^2

    d_front=0.80,                # m
    d_back=0.30,                 # m
    cg_height=0.45,              # m
    drag_height_offset=0.20,     # m

    corner_radius=10.0           # m
)


shaft = ShaftGeometry(
    track_width=1.10,            # L [m]
    bearing_position=0.15,       # m

    wheel_diameter=0.32,         # m

    brake_position=0.10,         # m
    brake_radius=0.08,           # m

    sprocket_position=0.25,      # m
    sprocket_radius=0.10,        # m

    shaft_diameter=0.03,         # m
    fillet_radius=0.002          # m
)


# ============================================================
# A) ACCELERATION
# ============================================================

acceleration = AccelerationCase(vehicle, shaft)

# Test acceleration at low speed
acceleration_speed = 10.0

print("\n" + "=" * 60)
print("A) ACCELERATION")
print("=" * 60)

print(f"Speed:             {acceleration_speed:.3f} m/s")
print(f"Air drag:          {acceleration.air_drag(acceleration_speed):.3f} N")
print(f"Drive force:       {acceleration.drive_force(acceleration_speed):.3f} N")
print(f"Motor torque:      {acceleration.motor_torque(acceleration_speed):.3f} Nm")
print(f"Sprocket force:    {acceleration.sprocket_force(acceleration_speed):.3f} N")

acceleration_forces = acceleration.wheel_forces(acceleration_speed)

print("\nWheel forces:")
print(acceleration_forces)

acc_vertical_sum = (
    acceleration_forces.front_left_vertical
    + acceleration_forces.front_right_vertical
    + acceleration_forces.rear_left_vertical
    + acceleration_forces.rear_right_vertical
)

print(f"\nVertical force sum: {acc_vertical_sum:.3f} N")


# ============================================================
# B) BRAKING
# ============================================================

braking = BrakingCase(vehicle, shaft)

# Project specifies braking from maximum speed


print("\n" + "=" * 60)
print("B) BRAKING")
print("=" * 60)

print(f"Speed:                  {vehicle.max_speed:.3f} m/s")
print(f"Air drag:               {braking.air_drag():.3f} N")
print(f"Braking force:          {braking.braking_force():.3f} N")
print(f"Total brake torque:     {braking.brake_torque():.3f} Nm")
print(f"Torque per brake disc:  {braking.brake_disc_torque():.3f} Nm")
print(f"Force per brake disc:   {braking.brake_disc_force():.3f} N")

braking_forces = braking.wheel_forces()

print("\nWheel forces:")
print(braking_forces)

brake_vertical_sum = (
    braking_forces.front_left_vertical
    + braking_forces.front_right_vertical
    + braking_forces.rear_left_vertical
    + braking_forces.rear_right_vertical
)

print(f"\nVertical force sum: {brake_vertical_sum:.3f} N")


# ============================================================
# C) CORNERING
# ============================================================

cornering = CorneringCase(vehicle, shaft)

print("\n" + "=" * 60)
print("C) CORNERING")
print("=" * 60)

print(f"Maximum gamma:      {cornering.max_gamma():.4f}")
print(f"Cornering speed:    {cornering.cornering_speed():.3f} m/s")
print(f"Lateral force:      {cornering.lateral_force():.3f} N")
print(f"Air drag:           {cornering.air_drag():.3f} N")
print(f"Motor torque:       {cornering.motor_torque():.3f} Nm")

cornering_forces = cornering.wheel_forces()

print("\nWheel forces:")
print(cornering_forces)

corner_vertical_sum = (
    cornering_forces.front_left_vertical
    + cornering_forces.front_right_vertical
    + cornering_forces.rear_left_vertical
    + cornering_forces.rear_right_vertical
)

corner_lateral_sum = (
    cornering_forces.front_left_lateral
    + cornering_forces.front_right_lateral
    + cornering_forces.rear_left_lateral
    + cornering_forces.rear_right_lateral
)

print(f"\nVertical force sum: {corner_vertical_sum:.3f} N")
print(f"Lateral force sum:  {corner_lateral_sum:.3f} N")