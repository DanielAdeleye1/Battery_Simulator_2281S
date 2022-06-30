#!/usr/bin/python
import socket
import struct
import math
import time
import keithley_driver as sim

# IP ADDRESS ----------------------
echoCmd = 1
ipAddress = "169.254.192.151"
port = 5025
timeout = 20.0


t1 = time.time()

# SOCKET ---------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1, idStr = sim.PowerSupply_Connect(s, ipAddress, port, timeout, echoCmd, 1, 1)
print(idStr)

# MAIN FUNCTION CALLS --------------
sim.PowerSupply_SetFunction(s, 2)
print(sim.PowerSupply_GetCurrent(s))
print(sim.PowerSupply_GetVoltage(s))

print(sim.BatterySimulator_GetCapacity(s))
print(sim.BatterySimulator_GetSOC(s))
print(sim.BatterySimulator_GetESR(s))

sim.PowerSupply_Disconnect(s)

t2 = time.time()
exit()