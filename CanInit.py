import can

def Can_INIT(channel='can0', bustype='socketcan'):
    try:
        bus = can.interface.Bus(channel=channel, bustype=bustype)
        print("CAN bus initialized successfully.")
        return bus
    except can.CanError as e:
        print(f"Error initializing CAN bus: {e}")
        return None
