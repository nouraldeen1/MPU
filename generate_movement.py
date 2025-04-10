import pandas as pd
import numpy as np

def generate_moving_x_sample(output_file, duration=22.4, dt=0.1, acc_x=5, noise_level=0.02):

 # Calculate number of samples
    n_samples = int(duration / dt) + 1
    
    # Generate time array (e.g., 0.0, 0.1, ..., 22.4)
    time = np.arange(0, n_samples * dt, dt)
    
    # Acceleration data
    # X: Constant acceleration (e.g., 0.1 g) across ALL time points + noise
    acc_x_data = np.full(n_samples, acc_x) + np.random.normal(0, noise_level, n_samples)
    
    # Y: Stationary (0 g) + noise, no motion
    acc_y_data = np.random.normal(0, noise_level, n_samples)
    
    # Z: Gravity (1 g) + noise, stationary vertically
    acc_z_data = np.full(n_samples, 1.0) + np.random.normal(0, noise_level, n_samples)
    
    # Create DataFrame
    data = pd.DataFrame({
        'Time': time,
        'AccX': acc_x_data,
        'AccY': acc_y_data,
        'AccZ': acc_z_data
    })
    
    # Save to CSV
    data.to_csv(output_file, index=False)
    print(f"Generated moving X-axis sample saved to '{output_file}'")
    print(f"Duration: {duration} s, Samples: {n_samples}, dt: {dt} s, fs: {1/dt} Hz")
    print(f"AccX: {acc_x} g (constant) ± {noise_level} g (noise), AccY: 0 g ± {noise_level} g, AccZ: 1 g ± {noise_level} g")
    
    # Theoretical position drift (for validation)
    acc_x_ms2 = acc_x * 9.81  # Convert to m/s²
    final_velocity = acc_x_ms2 * duration
    final_position = 0.5 * acc_x_ms2 * duration**2
    print(f"Theoretical X-axis: Final Velocity = {final_velocity:.2f} m/s, Position Drift = {final_position:.2f} m")

if __name__ == "__main__":
    output_file = "sample4/nomove.csv"
    generate_moving_x_sample(output_file, duration=22.4, dt=0.1, acc_x=10, noise_level=0.2)