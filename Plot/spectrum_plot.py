import sys
sys.path.insert(0, "/home/pawel1/Pulpit/PyLabDevice/Device")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

from Device import Device


ldc = Device().get_ldc4005_instance()
pm100 = Device().get_pm100_instance()

ldc.set_ld_current_in_amper(0.015)
ldc.on()
time.sleep(2)

min_wavelength = pm100.get_minimum_wavelength_in_nm()
max_wavelength = pm100.get_maximum_wavelength_in_nm()

wavelength = np.linspace(min_wavelength, max_wavelength, max_wavelength-min_wavelength+1)
power = np.zeros(len(wavelength))

for i in range(0, len(wavelength)):
    pm100.set_wavelength_in_nm(wavelength[i])
    time.sleep(0.1)
    power[i] = pm100.get_power()

plt.plot(wavelength, power)
plt.show()

