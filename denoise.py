import pandas as pd
import numpy as np

class KalmanFilter:
    def __init__(self, process_variance=0.01, measurement_variance=0.5):
        self.Q = process_variance
        self.R = measurement_variance
        self.x = 0  # Initial estimate
        self.P = 1  # Initial covariance
    
    def update(self, measurement):
        self.P = self.P + self.Q
        K = self.P / (self.P + self.R)  # Kalman gain
        self.x = self.x + K * (measurement - self.x)
        self.P = (1 - K) * self.P
        return self.x

def process_data(input_file="nomove.csv", output_file="denoised_nomove.csv"):
    # Load raw data
    data = pd.read_csv(input_file)
    time = data["Time"].values
    acc_x = data["AccX"].values
    acc_y = data["AccY"].values
    acc_z = data["AccZ"].values

    # Offset calibration (assume at rest initially, gravity on Z-axis)
    offset_x = np.mean(acc_x[:100])  # Average of first 100 samples
    offset_y = np.mean(acc_y[:100])
    offset_z = np.mean(acc_z[:100]) - 16384  # MPU6050 default scale: 16384 = 1g

    calibrated_x = acc_x - offset_x
    calibrated_y = acc_y - offset_y
    calibrated_z = acc_z - offset_z

    # Apply Kalman Filter to each axis
    kf_x = KalmanFilter()
    kf_y = KalmanFilter()
    kf_z = KalmanFilter()

    denoised_x = [kf_x.update(x) for x in calibrated_x]
    denoised_y = [kf_y.update(y) for y in calibrated_y]
    denoised_z = [kf_z.update(z) for z in calibrated_z]

    # Save denoised data
    denoised_df = pd.DataFrame({
        "Time": time,
        "Raw_AccX": acc_x,
        "Raw_AccY": acc_y,
        "Raw_AccZ": acc_z,
        "Denoised_AccX": denoised_x,
        "Denoised_AccY": denoised_y,
        "Denoised_AccZ": denoised_z
    })
    denoised_df.to_csv(output_file, index=False)
    print(f"Denoised data saved to '{output_file}'.")

if __name__ == "__main__":
    process_data()