#Micrbit dropp med finne til m/s
import pandas as pd         
import matplotlib.pyplot as plt

# Conversion factor from raw accelerometer data to m/s^2
g_to_m_s2 = 9.81 / 512

v = 0
v_liste = [v]

# Load the CSV file
data = pd.read_csv(r'/Users/husby/Downloads/Microbit Data Log.csv', sep=",")  # Adjust separator if needed

# Strip any leading/trailing spaces from column names
data.columns = data.columns.str.strip()

# Print the column names to verify they are correct
print(data.columns)


# Extract data
time = data["Time (seconds)"]
accelerationx = data["accelerationx"] * g_to_m_s2
accelerationy = data["accelerationy"] * g_to_m_s2
accelerationz = data["accelerationz"] * g_to_m_s2


# Plot acceleration data
plt.figure(figsize=(12, 6))
plt.plot(time, accelerationx, label="Acceleration X (m/s²)")
plt.plot(time, accelerationy, label="Acceleration Y (m/s²)")
plt.plot(time, accelerationz, label="Acceleration Z (m/s²)")
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s²)")
plt.title("Acceleration Over Time")
plt.grid()
plt.show()

# Subtract mean of y acceleration to center the values
acceleration_y_centered = accelerationy - accelerationy.mean()

# Calculate velocity over time using numerical integration
for i in range(len(time) - 1):
    dt = time[i + 1] - time[i]
    delta_v = dt * acceleration_y_centered[i]
    v = v + delta_v
    v_liste.append(v)

# Plot the velocity function
plt.figure(figsize=(12, 6))
plt.plot(time, v_liste, label="Velocity (m/s)")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("Velocity Over Time")
plt.legend()
plt.grid()
plt.show()

# Print the highest velocity
print("Høyeste hastigheten til heisen er:", round(max(v_liste), 2), "m/s")