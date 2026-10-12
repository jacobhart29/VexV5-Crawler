from vex import *

# Initialize Brain and Controller
brain = Brain()
controller = Controller()

# Motor Setup
# GearSetting.RATIO_18_1 is standard green. Change to RATIO_6_1 (blue) or RATIO_36_1 (red) if needed.
# Right-side motors are inverted (True) so positive values move the robot forward consistently.
front_right = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
front_left  = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
back_right  = Motor(Ports.PORT16, GearSetting.RATIO_18_1, True)
back_left   = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)

# Sensors & Receiver Setup
ai_cam_left  = Aivision(Ports.PORT15)
ai_cam_right = Aivision(Ports.PORT20)
rf_receiver  = Radio(Ports.PORT2)

def drive_mecanum():
    """
    Control scheme:
    - Left Joystick Y (Axis 3): Forward / Backward
    - Left Joystick X (Axis 4): Strafe Left / Right
    - Right Joystick X (Axis 1): Turn Left / Right
    """
    deadband = 5  # Prevents motor drift when joysticks are resting

    while True:
        # Read controller joystick positions (-100 to 100)
        forward = controller.axis3.position()
        strafe  = controller.axis4.position()
        turn    = controller.axis1.position()

        # Apply deadband filtering
        if abs(forward) < deadband:
            forward = 0
        if abs(strafe) < deadband:
            strafe = 0
        if abs(turn) < deadband:
            turn = 0

        # Mecanum drive kinematics matrix
        fl_power = forward + strafe + turn
        fr_power = forward - strafe - turn
        bl_power = forward - strafe + turn
        br_power = forward + strafe - turn

        # Normalize motor speeds if any value exceeds 100%
        max_power = max(abs(fl_power), abs(fr_power), abs(bl_power), abs(br_power))
        if max_power > 100:
            fl_power = (fl_power / max_power) * 100
            fr_power = (fr_power / max_power) * 100
            bl_power = (bl_power / max_power) * 100
            br_power = (br_power / max_power) * 100

        # Send power outputs to drive motors
        front_left.spin(FORWARD, fl_power, PERCENT)
        front_right.spin(FORWARD, fr_power, PERCENT)
        back_left.spin(FORWARD, bl_power, PERCENT)
        back_right.spin(FORWARD, br_power, PERCENT)

        # Brief sleep to yield execution to the V5 OS scheduler
        wait(20, MSEC)

# Execute main driver loop
drive_mecanum()