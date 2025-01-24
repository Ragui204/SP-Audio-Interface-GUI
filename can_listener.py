import can
import threading

def can_receive_loop(bus):
    print("Starting CAN receive loop...")
    while True:
        message = bus.recv()  # Blocks until a message is received
        handle_can_message(message)

def handle_can_message(message):
    print(f"Received CAN Message: ID=0x{message.arbitration_id:X}, Data={message.data}")

    if message.arbitration_id in [0x100, 0x120]:
        if message.data[0] == 0x01:  # Volume feedback
            print(f"Volume Feedback: {message.data[1]}")
        elif message.data[0] == 0x02:  # Reverb Decay feedback
            print(f"Reverb Decay Feedback: {message.data[1]}")

def start_can_listener(bus):
    listener_thread = threading.Thread(target=can_receive_loop, args=(bus,), daemon=True)
    listener_thread.start()
