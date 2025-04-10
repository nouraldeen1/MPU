import pandas as pd
import numpy as np

def generate_moving_xyz_sample(output_file, duration=30.0, dt=0.1, max_acc_x=6.0, max_acc_y=40.0, max_acc_z=0.6, noise_level=0.1):
    """
    Generate a CSV sample simulating 3D movement (X, Y, Z) with noise.
    
    Parameters:
        output_file (str): Path to save the CSV file.
        duration (float): Total duration in seconds (default: 30.0 s).
        dt (float): Time step in seconds (default: 0.1 s, fs = 10 Hz).
        max_acc_x, max_acc_y, max_acc_z (float): Peak acceleration in g for each axis.
        noise_level (float): Standard deviation of Gaussian noise in g (default: 0.1 g).
    
    Notes:
        - Each axis: Accelerates (0-5 s), constant velocity (5-25 s), decelerates (25-30 s).
        - Z-axis includes +1 g for gravity.
        - Output in g units, compatible with denoise.py.
    """
    # Calculate number of samples
    n_samples = int(duration / dt) + 1
    
    # Generate time array
    time = np.arange(0, n_samples * dt, dt)
    
    # Define motion phases (in seconds)
    acc_phase = 5.0  # 0 to 5 s: accelerate
    const_phase_start = 5.0
    const_phase_end = duration - 5.0  # 5 to 25 s: constant velocity
    dec_phase = 5.0  # 25 to 30 s: decelerate
    
    # Acceleration profiles for X, Y, Z
    acc_x = np.zeros(n_samples)
    acc_y = np.zeros(n_samples)
    acc_z = np.zeros(n_samples)
    
    for i, t in enumerate(time):
        if t <= acc_phase:  # Accelerate from 0 to max_acc
            acc_x[i] = max_acc_x * (t / acc_phase)
            acc_y[i] = max_acc_y * (t / acc_phase)
            acc_z[i] = max_acc_z * (t / acc_phase)
        elif t <= const_phase_end:  # Constant velocity (acceleration ≈ 0)
            acc_x[i] = 0.0
            acc_y[i] = 0.0
            acc_z[i] = 0.0
        else:  # Decelerate from 0 to -max_acc
            acc_x[i] = max_acc_x * (1 - (t - const_phase_end) / dec_phase) - max_acc_x
            acc_y[i] = max_acc_y * (1 - (t - const_phase_end) / dec_phase) - max_acc_y
            acc_z[i] = max_acc_z * (1 - (t - const_phase_end) / dec_phase) - max_acc_z
    
    # Add noise and gravity (Z-axis: +1 g)
    acc_x_data = acc_x + np.random.normal(0, noise_level, n_samples)
    acc_y_data = acc_y + np.random.normal(0, noise_level, n_samples)
    acc_z_data = acc_z + 1.0 + np.random.normal(0, noise_level, n_samples)  # Gravity included
    
    # Create DataFrame
    data = pd.DataFrame({
        'Time': time,
        'AccX': acc_x_data,
        'AccY': acc_y_data,
        'AccZ': acc_z_data
    })
    
    # Save to CSV
    data.to_csv(output_file, index=False)
    print(f"Generated 3D movement sample saved to '{output_file}'")
    print(f"Duration: {duration} s, Samples: {n_samples}, dt: {dt} s, fs: {1/dt} Hz")
    print(f"AccX: 0 to {max_acc_x} g (acc), 0 g (const), {max_acc_x} to 0 g (dec) ± {noise_level} g")
    print(f"AccY: 0 to {max_acc_y} g (acc), 0 g (const), {max_acc_y} to 0 g (dec) ± {noise_level} g")
    print(f"AccZ: 0 to {max_acc_z} g (acc), 0 g (const), {max_acc_z} to 0 g (dec) + 1 g ± {noise_level} g")
    
    # Theoretical displacement (integrate NumPy arrays)
    for axis, max_acc in [('X', max_acc_x), ('Y', max_acc_y), ('Z', max_acc_z)]:
        acc = data[f'Acc{axis}'].to_numpy() - (1.0 if axis == 'Z' else 0.0)  # Subtract gravity for Z
        acc_ms2 = acc * 9.81
        velocity = np.cumsum(acc_ms2) * dt
        position = np.cumsum(velocity) * dt
        print(f"Theoretical {axis}-axis: Final Velocity = {velocity[-1]:.2f} m/s, Total Displacement = {position[-1]:.2f} m")

if __name__ == "__main__":
    output_file = "sample5/move.csv"
    generate_moving_xyz_sample(output_file, duration=30.0, dt=0.1, max_acc_x=6.0, max_acc_y=40.0, max_acc_z=0.6, noise_level=0.1)