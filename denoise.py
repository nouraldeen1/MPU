import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt, medfilt, savgol_filter as scipy_savgol_filter

class KalmanFilter1D:
    def __init__(self, process_noise=0.01, measurement_noise=0.1, error_estimate=1.0):
        self.Q = process_noise
        self.R = measurement_noise
        self.P = error_estimate
        self.x = 0.0

    def update(self, measurement):
        self.P = self.P + self.Q
        K = self.P / (self.P + self.R)
        self.x = self.x + K * (measurement - self.x)
        self.P = (1 - K) * self.P
        return self.x

def offset_calibration(data, stationary_samples=10):
    offset = np.mean(data[:stationary_samples])
    return data - offset

def low_pass_filter(data, fs, cutoff=4):
    nyquist = fs / 2
    if cutoff >= nyquist:
        raise ValueError(f"Cutoff frequency ({cutoff} Hz) must be less than Nyquist ({nyquist} Hz)")
    b, a = butter(2, cutoff/nyquist, btype='low', analog=False)
    return filtfilt(b, a, data)

def median_filter(data, window_size=5):
    return medfilt(data, kernel_size=window_size)

def kalman_filter(data, process_noise=0.01, measurement_noise=0.1):
    kf = KalmanFilter1D(process_noise, measurement_noise)
    return np.array([kf.update(x) for x in data])

def apply_savgol_filter(data, window_size=11, polyorder=2):
    if window_size % 2 == 0:
        window_size += 1
    return scipy_savgol_filter(data, window_size, polyorder)

# New helper function for time conversion
def convert_time(data):
    if "Time" in data.columns:
        time_ms = data["Time"].values
        time_s = time_ms / 1000  # Convert to seconds
        time = time_s - time_s[0]  # Start at 0s
        dt = time[1] - time[0]  # Time step in seconds
        if dt > 0:
            fs = 1 / dt
            print(f"Time converted from ms to s, offset removed. dt = {dt:.6f}s, fs = {fs:.2f} Hz")
        else:
            fs = 10
            time = np.arange(0, len(data) * 0.1, 0.1)
            print(f"Invalid dt ({dt}s), using default fs = 10 Hz")
    else:
        fs = 10
        time = np.arange(0, len(data) * 0.1, 0.1)
        print("No 'Time' column, assuming fs = 10 Hz")
    return time, fs

def denoise_data(input_file="raw_mpu6050_data.csv", output_file="denoised_nomove.csv",
                 use_offset=True, use_lowpass=True, use_median=True, use_kalman=True, use_savgol=True):
    # Load data
    data = pd.read_csv(input_file)
    
    # Convert time and get sampling frequency
    #time, fs = convert_time(data)
    if "Time" in data.columns:
        time = data["Time"].values
        dt = time[1] - time[0]  # Time step in seconds
        fs = 1 / dt


    # Raw acceleration (assuming m/s²)
    acc_x = data["AccX"].values
    acc_y = data["AccY"].values
    acc_z = data["AccZ"].values

    # Denoising pipeline
    def apply_denoising(acc):
        result = acc.copy()
        if use_offset:
            result = offset_calibration(result, stationary_samples=10)
        if use_lowpass:
            result = low_pass_filter(result, fs, cutoff=4)
        if use_median:
            result = median_filter(result, window_size=5)
        if use_kalman:
            result = kalman_filter(result, process_noise=0.01, measurement_noise=0.1)
        if use_savgol:
            result = apply_savgol_filter(result, window_size=11, polyorder=2)
        return result

    # Apply to each axis
    acc_x_denoised = apply_denoising(acc_x)
    acc_y_denoised = apply_denoising(acc_y)
    acc_z_denoised = apply_denoising(acc_z)

    # Save results
    output_df = pd.DataFrame({
        "Time": time,
        "Raw_AccX": acc_x,
        "Denoised_AccX": acc_x_denoised,
        "Raw_AccY": acc_y,
        "Denoised_AccY": acc_y_denoised,
        "Raw_AccZ": acc_z,
        "Denoised_AccZ": acc_z_denoised
    })
    output_df.to_csv(output_file, index=False)
    print(f"Denoised data saved to '{output_file}' with methods: "
          f"Offset={use_offset}, LowPass={use_lowpass}, Median={use_median}, "
          f"Kalman={use_kalman}, SavGol={use_savgol}")

if __name__ == "__main__":
    # Process multiple samples with different combinations
    denoise_data("sample1/nomove.csv", "sample1/denoised_nomove.csv",
                 use_offset=True, use_lowpass=True, use_median=True, use_kalman=True, use_savgol=True)
    denoise_data("sample2/nomove.csv", "sample2/denoised_nomove.csv",
                 use_offset=True, use_lowpass=True, use_median=True, use_kalman=True, use_savgol=True)
    denoise_data("sample3/nomove.csv", "sample3/denoised_nomove.csv",
                 use_offset=True, use_lowpass=True, use_median=True, use_kalman=True, use_savgol=True)
    denoise_data("sample4/nomove.csv", "sample4/denoised_nomove.csv",
                 use_offset=True, use_lowpass=True, use_median=True, use_kalman=True, use_savgol=True)
    denoise_data("sample5/move.csv", "sample5/denoised_move.csv",
                use_offset=True, use_lowpass=True, use_median=True, use_kalman=True, use_savgol=True)

