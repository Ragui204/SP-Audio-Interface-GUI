import can
import struct

# Initialize CAN bus
try:
    bus = can.interface.Bus(channel="can0", bustype="socketcan")
except Exception as e:
    print(f"CAN Bus Initialization Failed: {e}")
    bus = None  # Avoid crashing the GUI

# Parameter ID mapping for ID 0x100-based control
PARAM_IDS = {
    # MIDI
    "Reverb Mix": 1,
    "Reverb Size": 2,
    "Reverb Decay": 3,
    "Delay Time": 4,
    "Delay Mix": 5,
    "Delay Feedback": 6,
    "Delay Color": 7,
    "Delay Mod": 8,
    "Note Volume": 9,
    "Master Volume": 10,
    "Waveform": 11,

    # Guitar1 Controls (match your checkCAN logic)
    "Input Volume": 11,
    "BPM": 12,
    "DIVISION_MODE": 13,
    "NUMBER_OF_DELAYS": 14,
    "DELAY_GAIN": 15,
    "REVERB_TIME": 16,
    "REVERB_GAIN": 17,
    "CHORUS_GAIN": 18,
    "BASE_DELAY_MS": 19,
    "MOD_DEPTH_MS": 20,
    "MOD_RATE_HZ": 21,
    "NUMBER_OF_VOICES": 22,
    "BITCRUSHER_BITS": 23,
    "BITCRUSHER_GAIN": 24,
    "DRY_SIGNAL": 25,
    "FX": 26,

    #Guitar Toggles
    "Delay Toggle": 32,
    "Reverb Toggle": 33,
    "Chorus Toggle": 34,
    "Distortion Toggle": 35
}


def send_can_message(teensy_id, parameter, value):
    """Send CAN message using ID 0x100 format with param ID and float."""
    if bus:
        param_id = PARAM_IDS.get(parameter)
        if param_id is None:
            print(f"Unknown CAN parameter: {parameter}")
            return

        data = bytearray(8)
        data[0] = param_id
        data[1:5] = struct.pack('<f', float(value))

        msg = can.Message(arbitration_id=teensy_id, data=data, is_extended_id=False)
        try:
            bus.send(msg)
            print(f"📤 Sent to Teensy {teensy_id}: {parameter} = {value:.2f} [Param ID {param_id}]")
        except can.CanError as e:
            print(f"CAN Error: {e}")
    else:
        print(f"CAN bus not initialized. Could not send {parameter} -> {value}")
