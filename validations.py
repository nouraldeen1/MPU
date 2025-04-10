import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

def estimate_position(acc, dt):
    """Double integrate acceleration to get position."""
    velocity = cumulative_trapezoid(acc, dx=dt, initial=0)
    position = cumulative_trapezoid(velocity, dx=dt, initial=0)
    return position

def validate_data(input_file="denoised_nomove.csv", output_csv="validation_results.csv"):
    # Load data
    data = pd.read_csv(input_file)
    time = data["Time"].values
    dt = time[1] - time[0]  # Assume constant time step

    # Convert raw and denoised data to physical units (m/s², ±2g scale)
    raw_x = data["Raw_AccX"].values / 16384 * 9.81
    raw_y = data["Raw_AccY"].values / 16384 * 9.81
    raw_z = data["Raw_AccZ"].values / 16384 * 9.81
    denoised_x = data["Denoised_AccX"].values / 16384 * 9.81
    denoised_y = data["Denoised_AccY"].values / 16384 * 9.81
    denoised_z = data["Denoised_AccZ"].values / 16384 * 9.81

    # Estimate position for all axes
    pos_raw_x = estimate_position(raw_x, dt)
    pos_denoised_x = estimate_position(denoised_x, dt)
    pos_raw_y = estimate_position(raw_y, dt)
    pos_denoised_y = estimate_position(denoised_y, dt)
    pos_raw_z = estimate_position(raw_z, dt)
    pos_denoised_z = estimate_position(denoised_z, dt)

    # Plot X-axis
    plt.figure(figsize=(10, 6))
    plt.plot(time, raw_x, label="Raw AccX", alpha=0.5)
    plt.plot(time, denoised_x, label="Denoised AccX", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/s²)")
    plt.title("Raw vs Denoised Acceleration (X-axis)")
    plt.legend()
    plt.savefig("acceleration_x_comparison.png")
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(time, pos_raw_x, label="Raw Position X", alpha=0.5)
    plt.plot(time, pos_denoised_x, label="Denoised Position X", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.title("Raw vs Denoised Position (X-axis)")
    plt.legend()
    plt.savefig("position_x_comparison.png")
    plt.close()

    # Plot Y-axis
    plt.figure(figsize=(10, 6))
    plt.plot(time, raw_y, label="Raw AccY", alpha=0.5)
    plt.plot(time, denoised_y, label="Denoised AccY", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/s²)")
    plt.title("Raw vs Denoised Acceleration (Y-axis)")
    plt.legend()
    plt.savefig("acceleration_y_comparison.png")
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(time, pos_raw_y, label="Raw Position Y", alpha=0.5)
    plt.plot(time, pos_denoised_y, label="Denoised Position Y", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.title("Raw vs Denoised Position (Y-axis)")
    plt.legend()
    plt.savefig("position_y_comparison.png")
    plt.close()

    # Plot Z-axis
    plt.figure(figsize=(10, 6))
    plt.plot(time, raw_z, label="Raw AccZ", alpha=0.5)
    plt.plot(time, denoised_z, label="Denoised AccZ", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/s²)")
    plt.title("Raw vs Denoised Acceleration (Z-axis)")
    plt.legend()
    plt.savefig("acceleration_z_comparison.png")
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(time, pos_raw_z, label="Raw Position Z", alpha=0.5)
    plt.plot(time, pos_denoised_z, label="Denoised Position Z", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.title("Raw vs Denoised Position (Z-axis)")
    plt.legend()
    plt.savefig("position_z_comparison.png")
    plt.close()

    # Evaluate drift for all axes
    drift_raw_x = abs(pos_raw_x[-1])
    drift_denoised_x = abs(pos_denoised_x[-1])
    drift_raw_y = abs(pos_raw_y[-1])
    drift_denoised_y = abs(pos_denoised_y[-1])
    drift_raw_z = abs(pos_raw_z[-1])
    drift_denoised_z = abs(pos_denoised_z[-1])

    print("\nFinal Position Drift:")
    print(f"X-axis: Raw = {drift_raw_x:.2f}m, Denoised = {drift_denoised_x:.2f}m")
    print(f"Y-axis: Raw = {drift_raw_y:.2f}m, Denoised = {drift_denoised_y:.2f}m")
    print(f"Z-axis: Raw = {drift_raw_z:.2f}m, Denoised = {drift_denoised_z:.2f}m")

    # Save results to a new CSV
    results_df = pd.DataFrame({
        "Time": time,
        "Raw_AccX_m/s2": raw_x,
        "Denoised_AccX_m/s2": denoised_x,
        "Raw_PosX_m": pos_raw_x,
        "Denoised_PosX_m": pos_denoised_x,
        "Raw_AccY_m/s2": raw_y,
        "Denoised_AccY_m/s2": denoised_y,
        "Raw_PosY_m": pos_raw_y,
        "Denoised_PosY_m": pos_denoised_y,
        "Raw_AccZ_m/s2": raw_z,
        "Denoised_AccZ_m/s2": denoised_z,
        "Raw_PosZ_m": pos_raw_z,
        "Denoised_PosZ_m": pos_denoised_z
    })
    results_df.to_csv(output_csv, index=False)
    print(f"\nResults saved to '{output_csv}'.")

if __name__ == "__main__":
    validate_data()