from pymavlink import mavutil
from time import sleep

def arm_vehicle():
    master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0)

    print("Waiting for the vehicle to arm")
    master.motors_armed_wait()
    print('Armed!')
    

def vehicle_mode(input_mode):
    mode = input_mode
    if mode not in master.mode_mapping():
        print('Unknown mode : {}'.format(mode))
        print('Try:', list(master.mode_mapping().keys()))
        sys.exit(1)


    mode_id = master.mode_mapping()[mode]

    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)
    

master = mavutil.mavlink_connection("/dev/serial0", baud=921600)
print(master)

master.wait_heartbeat()

vehicle_mode('STABILIZE')

arm_vehicle()


sleep(10)
vehicle_mode('LAND')
