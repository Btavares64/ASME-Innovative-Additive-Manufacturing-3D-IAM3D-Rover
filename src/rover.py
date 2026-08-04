import curses
from smbus2 import SMBus
import time

ADDR = 0x40
MODE1, MODE2, PRESCALE = 0x00, 0x01, 0xFE

LEFT_SIDE = [2, 4]  
RIGHT_SIDE = [6, 8]  
CLAW = [0]
LIFT = [10]
REACH = [12]

def setup_pca(bus):
    bus.write_byte_data(ADDR, MODE1, 0x00)
    time.sleep(0.01)
    bus.write_byte_data(ADDR, MODE1, 0x11) 
    bus.write_byte_data(ADDR, PRESCALE, 0x06)
    bus.write_byte_data(ADDR, MODE1, 0x01) 
    time.sleep(0.01)
    bus.write_byte_data(ADDR, MODE2, 0x04)

def set_group(bus, channels, speed, forward=True):
    for pwm_ch in channels:
        dir_ch = pwm_ch + 1
        
        if forward:
            bus.write_byte_data(ADDR, 0x06 + (4 * dir_ch) + 1, 0x00) 
            bus.write_byte_data(ADDR, 0x06 + (4 * dir_ch) + 3, 0x10)
        else:
            bus.write_byte_data(ADDR, 0x06 + (4 * dir_ch) + 1, 0x10) 
            bus.write_byte_data(ADDR, 0x06 + (4 * dir_ch) + 3, 0x00)

        bus.write_byte_data(ADDR, 0x06 + (4 * pwm_ch) + 2, speed & 0xFF)
        bus.write_byte_data(ADDR, 0x06 + (4 * pwm_ch) + 3, speed >> 8)

def arm_movement(bus, channel, speed, forward=True):
    for pwm_ch in channel:
        dir_ch = pwm_ch + 1
        
        if forward:
            bus.write_byte_data(ADDR, 0x06 + (4 * dir_ch) + 1, 0x00) 
            bus.write_byte_data(ADDR, 0x06 + (4 * dir_ch) + 3, 0x10)
        else:
            bus.write_byte_data(ADDR, 0x06 + (4 * dir_ch) + 1, 0x10)
            bus.write_byte_data(ADDR, 0x06 + (4 * dir_ch) + 3, 0x00)

        bus.write_byte_data(ADDR, 0x06 + (4 * pwm_ch) + 2, speed & 0xFF)
        bus.write_byte_data(ADDR, 0x06 + (4 * pwm_ch) + 3, speed >> 8)

def stop_all(bus):
    for i in range(16):
        bus.write_byte_data(ADDR, 0x06 + (4 * i) + 1, 0x00)
        bus.write_byte_data(ADDR, 0x06 + (4 * i) + 3, 0x10)

def main(stdscr):
    curses.cbreak()
    stdscr.nodelay(True)
    stdscr.keypad(True)
    
    with SMBus(1) as bus:
        setup_pca(bus)
        stdscr.addstr(0, 0, "W=Fwd, S=Back, A=Left, D=Right\nI=Claw Up, O=Claw Down, U=Lift, J=Lift, I=Reach, K=Reach\n Q=Quit")
        
        last_key_time = time.time()
        moving = False

        while True:
            char = stdscr.getch()
            speed = 4095
            speed_for_arm = 1500

            if char == ord('q'):
                stop_all(bus)
                break
            
            if char != -1:
                curses.flushinp() 
                last_key_time = time.time()
                moving = True
                if char == ord('a'):
                    set_group(bus, LEFT_SIDE, speed, forward=True)
                    set_group(bus, RIGHT_SIDE, speed, forward=True)

                elif char == ord('d'):
                    set_group(bus, LEFT_SIDE, speed, forward=False)
                    set_group(bus, RIGHT_SIDE, speed, forward=False)

                elif char == ord('w'):
                    set_group(bus, LEFT_SIDE, speed, forward=False)
                    set_group(bus, RIGHT_SIDE, speed, forward=True)

                elif char == ord('s'):
                    set_group(bus, LEFT_SIDE, speed, forward=True)
                    set_group(bus, RIGHT_SIDE, speed, forward=False)

                elif char == ord("o"):
                    arm_movement(bus, CLAW, speed_for_arm, forward=True)

                elif char == ord("l"):
                    arm_movement(bus, CLAW, speed_for_arm, forward=False)

                elif char == ord("u"):
                    arm_movement(bus, LIFT, speed_for_arm, forward=True)

                elif char == ord("j"):
                    arm_movement(bus, LIFT, speed_for_arm, forward=False)

                elif char == ord("i"):
                    arm_movement(bus, REACH, speed_for_arm, forward=True)

                elif char == ord("k"):
                    arm_movement(bus, REACH, speed_for_arm, forward=False)

            if moving and (time.time() - last_key_time > 0.15):
                stop_all(bus)
                moving = False

            time.sleep(0.02)

if __name__ == "__main__":
    curses.wrapper(main)

