from vex import *

# Initialize Brain and Controller
brain = Brain()
controller = Controller()

# Motor Setup
front_right = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
front_left  = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
back_right  = Motor(Ports.PORT16, GearSetting.RATIO_18_1, True)
back_left   = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)

# Sensors Setup
ai_cam_left  = AiVision(Ports.PORT15)
ai_cam_right = AiVision(Ports.PORT20)


def handle_ai_cam():
    left_objects = ai_cam_left.take_snapshot(AiVision.ALL_TAGS)
    right_objects = ai_cam_right.take_snapshot(AiVision.ALL_TAGS)

    if left_objects and left_objects[0].exists:
        print("OBJECT ID ON LEFT:", left_objects[0].id)
    elif right_objects and right_objects[0].exists:
        print("OBJECT ID ON RIGHT:", right_objects[0].id)
    else:
        print("NO OBJECT DETECTED")


def move_forward(AMOUNT, SPEED):
    front_left.spin(FORWARD, SPEED, PERCENT)
    front_right.spin(FORWARD, SPEED, PERCENT)
    back_left.spin(FORWARD, SPEED, PERCENT)
    back_right.spin(FORWARD, SPEED, PERCENT)
    wait(AMOUNT, MSEC)
    front_left.stop()
    front_right.stop()
    back_left.stop()
    back_right.stop()


def move_backward(AMOUNT, SPEED):
    front_left.spin(REVERSE, SPEED, PERCENT)
    front_right.spin(REVERSE, SPEED, PERCENT)
    back_left.spin(REVERSE, SPEED, PERCENT)
    back_right.spin(REVERSE, SPEED, PERCENT)
    wait(AMOUNT, MSEC)
    front_left.stop()
    front_right.stop()
    back_left.stop()
    back_right.stop()


def move_left(AMOUNT, SPEED):
    front_left.spin(REVERSE, SPEED, PERCENT)
    front_right.spin(FORWARD, SPEED, PERCENT)
    back_left.spin(FORWARD, SPEED, PERCENT)
    back_right.spin(REVERSE, SPEED, PERCENT)
    wait(AMOUNT, MSEC)
    front_left.stop()
    front_right.stop()
    back_left.stop()
    back_right.stop()


def move_right(AMOUNT, SPEED):
    front_left.spin(FORWARD, SPEED, PERCENT)
    front_right.spin(REVERSE, SPEED, PERCENT)
    back_left.spin(REVERSE, SPEED, PERCENT)
    back_right.spin(FORWARD, SPEED, PERCENT)
    wait(AMOUNT, MSEC)
    front_left.stop()
    front_right.stop()
    back_left.stop()
    back_right.stop()


def drive_mecanum():
    """
    Control scheme:
    - Left Joystick Y (Axis 3): Forward / Backward
    - Left Joystick X (Axis 4): Strafe Left / Right
    - Right Joystick X (Axis 1): Turn Left / Right
    """
    deadband = 5
    cam_interval = 20 
    cam_timer = 0

    while True:
        forward = controller.axis3.position()
        strafe  = controller.axis4.position()
        turn    = controller.axis1.position()

        if abs(forward) < deadband:
            forward = 0
        if abs(strafe) < deadband:
            strafe = 0
        if abs(turn) < deadband:
            turn = 0

        fl_power = forward + strafe + turn
        fr_power = forward - strafe - turn
        bl_power = forward - strafe + turn
        br_power = forward + strafe - turn

        max_power = max(abs(fl_power), abs(fr_power), abs(bl_power), abs(br_power))
        if max_power > 100:
            fl_power = (fl_power / max_power) * 100
            fr_power = (fr_power / max_power) * 100
            bl_power = (bl_power / max_power) * 100
            br_power = (br_power / max_power) * 100

        front_left.spin(FORWARD, fl_power, PERCENT)
        front_right.spin(FORWARD, fr_power, PERCENT)
        back_left.spin(FORWARD, bl_power, PERCENT)
        back_right.spin(FORWARD, br_power, PERCENT)

        cam_timer += 20
        if cam_timer >= cam_interval:
            handle_ai_cam()
            cam_timer = 0

        wait(20, MSEC)


drive_mecanum()
