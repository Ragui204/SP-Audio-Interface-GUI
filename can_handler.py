import can
import struct

# Initialize CAN bus
try:
    bus = can.interface.Bus(channel="can0", bustype="socketcan")
except Exception as e:
    print(f"CAN Bus Initialization Failed: {e}")
    bus = None  # Avoid crashing the GUI

# CAN IDs mapping for MIDI1 (Teensy 1) and MIDI2 (Teensy 2)
CAN_IDS = {
    1: {  # Teensy 1 (MIDI1)
        "Master Volume": 0x100,
        "Reverb Size": 0x101,
        "Reverb Decay": 0x102,
        "Reverb Mix": 0x103,
        "Delay Time": 0x104,
        "Delay Mix": 0x106,
        "Delay Color": 0x107,
    },
    2: {  # Teensy 2 (MIDI2)
        "Master Volume": 0x200,
        "Reverb Size": 0x201,
        "Reverb Decay": 0x202,
        "Reverb Mix": 0x203,
        "Delay Time": 0x204,
        "Delay Mix": 0x206,
        "Delay Color": 0x207,
    }
}

def float_to_can_data(value):
    """Convert a float value to a CAN-compatible byte array."""
    return struct.pack('<f', float(value))

def send_can_message(teensy_id, parameter, value):
    """Send CAN message for a given Teensy device."""
    if bus:
        can_id = CAN_IDS.get(teensy_id, {}).get(parameter)
        if can_id:
            data = float_to_can_data(value)
            msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
            try:
                bus.send(msg)
                print(f"Sent CAN to Teensy {teensy_id}: {parameter} -> {value}")
            except can.CanError as e:
                print(f"CAN Error: {e}")
    else:
        print(f"CAN bus not initialized. Could not send {parameter} -> {value}")
