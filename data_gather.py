import serial
import csv
import time

# Serial port configuration
PORT = "COM3"  # Replace with your Arduino port (e.g., /dev/ttyUSB0 on Linux/Mac)
BAUD_RATE = 9600
DURATION = 10  # Seconds to collect data

# Arduino sketch to upload beforehand (see below in notes)
def collect_data():
    # Initialize serial connection
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for connection to stabilize

    # Open CSV file for writing
    with open("raw_mpu6050_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "AccX", "AccY", "AccZ"])  # Header

        print("Collecting data...")
        start_time = time.time()
        while time.time() - start_time < DURATION:
            if ser.in_waiting > 0:
                # Read and parse serial data
                line = ser.readline().decode("utf-8").strip()
                try:
                    ax, ay, az = map(int, line.split(","))
                    elapsed_time = time.time() - start_time
                    writer.writerow([elapsed_time, ax, ay, az])
                    print(f"Time: {elapsed_time:.2f}s, AccX: {ax}, AccY: {ay}, AccZ: {az}")
                except ValueError:
                    print("Invalid data received, skipping...")
    
    ser.close()
    print("Data collection complete. Saved to 'raw_mpu6050_data.csv'.")

if __name__ == "__main__":
    collect_data()