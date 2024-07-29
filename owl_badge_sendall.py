import serial
import time

def encode_packet_hex(badge_id, mode, score):
    # Constants
    HEADER = b'H00T!'  # ASCII bytes

    # Convert badge_id to high and low bytes
    high_byte = (badge_id >> 8) & 0xFF
    low_byte = badge_id & 0xFF

    # Create packet bytes
    packet = HEADER + bytes([high_byte, low_byte, mode, score])

    # Calculate checksum
    packet_sum = sum(packet)
    checksum = (512 - packet_sum) % 256  # Checksum must be 1 byte

    # Append checksum to packet
    packet += bytes([checksum])
    
    return packet

def send_packets(port='/dev/tty.usbserial-TG1101910', baudrate=4800):
    # Get user input for badge ID range
    start_badge_id = int(input("Enter start badge ID (integer): "))
    end_badge_id = int(input("Enter end badge ID (integer): "))
    mode = int(input("Enter mode (integer): "))
    score = int(input("Enter score (integer): "))

    # Validate range
    if start_badge_id > end_badge_id:
        print("Start badge ID must be less than or equal to end badge ID.")
        return

    # Connect to the serial port
    with serial.Serial(port, baudrate, timeout=1) as ser:
        for badge_id in range(start_badge_id, end_badge_id + 1):
            # Encode the packet
            packet = encode_packet_hex(badge_id, mode, score)
            
            # Send the packet three times with delay
            for _ in range(5):
                ser.write(packet)
                time.sleep(0.1)

            print(f"Packet sent for badge ID: {badge_id}")

if __name__ == "__main__":
    send_packets()
