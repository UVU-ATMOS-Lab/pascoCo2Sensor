from pasco.pasco_ble_device import PASCOBLEDevice
import time
import csv
import matplotlib.pyplot as plt
from pydoc import resolve
from pathlib import Path
sensor = PASCOBLEDevice()
devices = sensor.scan()
if not devices:
    print("No devices found.")
    quit()
    
sensor.connect(devices[0])

print("Connected!")
print("Live graph running. Press Ctrl+C to stop.")

# Data storage
times = []
co2_values = []
# Set the output path for the plots
plot_output_path = Path(__file__).resolve().parent.parent / "output" / "plots"
plot_output_path.mkdir(parents=True, exist_ok=True)
# Set up graph once
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-')
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("CO₂ concentration (ppm)")
ax.set_title("Live CO₂ Measurement")
plt.rcParams["savefig.directory"] = str(plot_output_path)
start_time = time.time()

#Set the file name and output path for the CSV file
data_dir = Path(__file__).resolve().parent.parent / "output" / "data"
data_dir.mkdir(parents=True, exist_ok=True)

file_name = "c02_live_data.csv"
data_output_path = data_dir / file_name
i = 1

while data_output_path.exists():
    file_name = f"c02_live_data_({i}).csv"
    data_output_path = data_dir / file_name
    i += 1

# Save data
with open(data_output_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time (seconds)", "CO2 (ppm)"])
    try:
        while True:
            elapsed = time.time() - start_time
            co2 = sensor.read_data("CO2Concentration")

            # Store data
            times.append(elapsed)
            co2_values.append(co2)

            # Save data
            writer.writerow([elapsed, co2])
            file.flush()

            # Update existing line (no redraw)
            line.set_data(times, co2_values)

            # Rescale axes
            ax.relim()
            ax.autoscale_view()

            # Refresh display
            fig.canvas.draw()
            fig.canvas.flush_events()
            print(f"{elapsed:.1f} s {co2:.1f} ppm")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping...")
        sensor.disconnect()

plt.ioff()
plt.show()
print(f"Saved as {file_name}")
