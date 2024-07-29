import serial
import time

def decode_packet_hex(hex_string):
    packet = bytes.fromhex(hex_string)

    HEADER = b'H00T!'  # Expected header bytes

    # Check header
    if not packet.startswith(HEADER):
        raise ValueError("Invalid packet header")

    # Extract data fields
    high_byte = packet[5]
    low_byte = packet[6]
    mode = packet[7]
    score = packet[8]
    checksum = packet[9]

    # Calculate expected checksum
    packet_sum = sum(packet[:-1])
    expected_checksum = (512 - packet_sum) % 256

    if checksum != expected_checksum:
        raise ValueError("Invalid checksum")

    badge_id = (high_byte << 8) | low_byte

    return {
        'badge_id': badge_id,
        'mode': mode,
        'score': score
    }

def listen_to_serial(port='/dev/tty.usbserial-TG1101910', baudrate=4800):
    with serial.Serial(port, baudrate, timeout=1) as ser:
        buffer = bytearray()
        print(f"Listening to serial port {port} at {baudrate} baud...")

        while True:
            if ser.in_waiting > 0:
                byte = ser.read()
                buffer.append(byte[0])

                # Check if the buffer has the H00T! header
                header_index = buffer.find(b'H00T!')
                if header_index != -1:
                    # Extract packet starting from H00T! header
                    buffer = buffer[header_index:]
                    
                    # Ensure we have at least 10 bytes for a full packet
                    while len(buffer) < 10:
                        if ser.in_waiting > 0:
                            byte = ser.read()
                            buffer.append(byte[0])
                        else:
                            time.sleep(0.01)  # Small delay to avoid busy-waiting
                            break

                    if len(buffer) >= 10:  # Check if we have a full packet
                        hex_string = buffer[:10].hex().upper()
                        remaining_buffer = buffer[10:]
                        try:
                            decoded_data = decode_packet_hex(hex_string)
                            print("Decoded Packet:", decoded_data)
                        except ValueError as e:
                            print(f"Error decoding packet: {e}")
                        
                        # Update buffer to keep any remaining data
                        buffer = remaining_buffer

if __name__ == "__main__":
    listen_to_serial()
