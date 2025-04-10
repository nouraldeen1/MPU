import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

def estimate_position(acc, dt):
    """Double integrate acceleration to get position."""
    velocity = cumulative_trapezoid(acc, dx=dt, initial=0)
    position = cumulative_trapezoid(velocity, dx=dt, initial=0)
    return position

def plot_comparison(time, raw_data, denoised_data, axis, output_dir):
    """Plot raw vs denoised data for acceleration and position."""
    # Acceleration plot
    plt.figure(figsize=(10, 6))
    plt.plot(time, raw_data["acc"], label=f"Raw Acc{axis}", alpha=0.5)
    plt.plot(time, denoised_data["acc"], label=f"Denoised Acc{axis}", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/s²)")
    plt.title(f"Raw vs Denoised Acceleration ({axis}-axis)")
    plt.legend()
    plt.savefig(f"{output_dir}/acceleration_{axis.lower()}_comparison.png")
    plt.close()

    # Position plot
    plt.figure(figsize=(10, 6))
    plt.plot(time, raw_data["pos"], label=f"Raw Position {axis}", alpha=0.5)
    plt.plot(time, denoised_data["pos"], label=f"Denoised Position {axis}", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.title(f"Raw vs Denoised Position ({axis}-axis)")
    plt.legend()
    plt.savefig(f"{output_dir}/position_{axis.lower()}_comparison.png")
    plt.close()

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

    # Organize data for plotting
    axes_data = {
        "X": {"raw": {"acc": raw_x, "pos": pos_raw_x}, "denoised": {"acc": denoised_x, "pos": pos_denoised_x}},
        "Y": {"raw": {"acc": raw_y, "pos": pos_raw_y}, "denoised": {"acc": denoised_y, "pos": pos_denoised_y}},
        "Z": {"raw": {"acc": raw_z, "pos": pos_raw_z}, "denoised": {"acc": denoised_z, "pos": pos_denoised_z}}
    }

    # Extract output directory from output_csv (e.g., "sample1/validation_results.csv" -> "sample1")
    output_dir = output_csv.rsplit("/", 1)[0] if "/" in output_csv else "."

    # Plot for each axis
    for axis, data_dict in axes_data.items():
        plot_comparison(time, data_dict["raw"], data_dict["denoised"], axis, output_dir)

    # Evaluate drift for all axes
    drift_raw_x = abs(pos_raw_x[-1])
    drift_denoised_x = abs(pos_denoised_x[-1])
    drift_raw_y = abs(pos_raw_y[-1])
    drift_denoised_y = abs(pos_denoised_y[-1])
    drift_raw_z = abs(pos_raw_z[-1])
    drift_denoised_z = abs(pos_denoised_z[-1])

    print(f"\nResults for '{input_file}':")
    print("Final Position Drift:")
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
    print(f"Results saved to '{output_csv}'.")

if __name__ == "__main__":
    validate_data("sample1/denoised_nomove.csv", "sample1/validation_results.csv")
    validate_data("sample2/denoised_nomove.csv", "sample2/validation_results.csv")
    validate_data("sample3/denoised_nomove.csv", "sample3/validation_results.csv")