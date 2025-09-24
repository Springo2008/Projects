from datetime import date
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('/Users/husby/Downloads/Raw Data.csv')
time = data["Time (s)"]
accelerationx = data["Linear Acceleration x (m/s^2)"]
accelerationy = data["Linear Acceleration y (m/s^2)"]
accelerationz = data["Linear Acceleration z (m/s^2)"]

plt.plot(time, accelerationx, label='Akselerasjon x (m/s^2)')
plt.plot(time, accelerationy, label='Akselerasjon y (m/s^2)')
plt.plot(time, accelerationz, label='Akselerasjon z (m/s^2)')
plt.legend()
plt.show()

print("accelerationy:", data["Linear Acceleration y (m/s^2)"].mean())
