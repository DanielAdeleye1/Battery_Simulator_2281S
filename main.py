#!/usr/bin/python
import socket
import struct
import math
import time
import csv
from threading import Thread
from csv_logger import CsvLogger
import logging
from time import sleep, perf_counter
import keithley_driver as sim

# IP ADDRESS ----------------------
echoCmd = 1
ipAddress = "169.254.85.36"
port = 5025
timeout = 20.0


# SOCKET ---------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1, idStr = sim.PowerSupply_Connect(s, ipAddress, port, timeout, echoCmd, 1, 1)
print(idStr)

# MAIN FUNCTION CALLS --------------
sim.PowerSupply_SetFunction(s, 2)
sim.BatterySimulator_SelectModel(s, 9)

print(sim.PowerSupply_GetVoc(s))
print(sim.PowerSupply_GetCurrent(s))
print(sim.PowerSupply_GetVoltage(s))

#print(sim.BatterySimulator_SetSOC(s, 30))
print(sim.BatterySimulator_GetCapacity(s))
print(sim.BatterySimulator_GetSOC(s))
print(sim.BatterySimulator_GetESR(s))

def Log_Battery_Data(s):
    time_stamp = time.time()

    Batt_Profile = sim.BatterySimulator_GetModel(s)
    Voc = sim.PowerSupply_GetVoc(s)
    Curr = sim.PowerSupply_GetCurrent(s)
    Vt = sim.PowerSupply_GetVoltage(s)
    SoC = sim.BatterySimulator_GetSOC(s)
    Cap = sim.BatterySimulator_GetCapacity(s)
    Res = sim.BatterySimulator_GetESR(s)

    

    filename = 'logs/log.csv'
    delimiter = ','
    level = logging.INFO
    custom_additional_levels = ['Profile_9']
    fmt = f'%(asctime)s{delimiter}%(levelname)s{delimiter}%(message)s'
    datefmt = '%Y/%m/%d %H:%M:%S'
    max_size = 1024  # 1 kilobyte
    max_files = 4  # 4 rotating files
    header = ['Time', 'Batt_Profile', 'SOC', 'Voc', 'Vt', 'Current', 'Res', 'Capacity']

# Creat logger with csv rotating handler
    csvlogger = CsvLogger(filename=filename,
                      delimiter=delimiter,
                      level=level,
                      add_level_names=custom_additional_levels,
                      add_level_nums=None,
                      fmt=fmt,
                      datefmt=datefmt,
                      max_size=max_size,
                      max_files=max_files,
                      header=header)

# Log some records
    for i in range(10):
        csvlogger.Profile_9([SoC, Voc, Vt, Curr, Res, Cap])
        sleep(0.1)


    # print(f'Battery Voc: {Voc: 0.2f}V')
    # print(f'Current: {Curr: 0.2f}A')
    # print(f'Vt: {Vt: 0.2f}V')
    # print(f'SOC: {SoC: 0.2f}%')
    # print(f'Capacity: {Cap: 0.2f}AH')
    # print(f'Resistance: {Res: 0.2f}Ohms')

    # f = open("bat_log.csv", "w")
    # write = csv.writer(f)
    # write.writerow([idStr])
    # write.writerow([Batt_Profile])
    # write.writerow([header])

    # while True:
    #     write.writerow([time_stamp, SoC, Voc, Vt, Curr, Res, Cap])


start_time = perf_counter()

# create thread for logging data
log_thread = Thread(target = Log_Battery_Data, args = (s,))

# start the thread
log_thread.start()

log_thread.join()

end_time = perf_counter()




sim.PowerSupply_Disconnect(s)

exit()
