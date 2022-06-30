#!/usr/bin/python
import socket
import struct
import math
import time

echoCmd = 1


#   SOCKET SETUP

def instrConnect(ksocket, myaddress, myport, timeOut, doReset, doIdQuery):
   ksocket.connect((myaddress, myport))
   print("Keithley Connected")
   ksocket.settimeout(timeOut)
   if doReset == 1:
       instrSend(ksocket, "*RST")
   if doIdQuery == 1:
       tmpId = instrQuery(ksocket, "*IDN?", 1024)
   return ksocket, tmpId


def instrSend(ksocket, cmd):
    if echoCmd == 1:
       print(cmd)
    cmd = "{0}\n".format(cmd)
    ksocket.send(cmd.encode())
    return

def instrQuery(ksocket, cmd, rcvSize):
    instrSend(ksocket, cmd)
    time.sleep(0.1)
    return ksocket.recv(rcvSize).decode()

def instrDisconnect(ksocket):
    ksocket.close()
    print("Keithley Disconnected")
    return


#   CONNECTING TO KEITHLEY 2281S

def PowerSupply_Connect(ksocket, myaddress, myport, timeOut, doEcho, doReset, doIdQuery):
   ksocket, myId = instrConnect(ksocket, myaddress, myport, timeOut, doReset, doIdQuery)
   return ksocket, myId

def PowerSupply_Disconnect(ksocket):
    instrDisconnect(ksocket)

#   SYSTEM FUNCTIONS
def PowerSupply_SetFunction(ksocket, activeFunc):
    if activeFunc == 0:
        # Set to Power Supply
        instrSend(ksocket, ":ENTR:FUNC POW")
    elif activeFunc == 1:
        # Set to Battery Test
        instrSend(ksocket, ":ENTR:FUNC TEST")
    elif activeFunc == 2:
        # Set to Battery Simulator
        instrSend(ksocket, ":ENTR:FUNC SIM")
    return

def PowerSupply_SetOutputState(ksocket, myState):
    if myState == 0:
        instrSend(ksocket, "OUTP:STAT OFF")
    else:
        instrSend(ksocket, "OUTP:STAT ON")

def PowerSupply_GetOutputState(ksocket):
    return instrQuery(ksocket, "OUTP:STAT?", 16)


#   GETTING BATTERY DATA FROM SIMULATOR MODE

def PowerSupply_GetCurrent(ksocket):
    sndBuffer = "SOUR1:CURR?"
    return instrQuery(ksocket, sndBuffer, 32)

def PowerSupply_GetVoltage(kocket):
    sndBuffer = "SOUR1:VOLT?"
    return instrQuery(kocket, sndBuffer, 32)

def BatterySimulator_GetCapacity(ksocket):
    return instrQuery(ksocket, ":BATT:SIM:CAP?", 16)

def BatterySimulator_GetSOC(ksocket):
    return instrQuery(ksocket, ":BATT:SIM:SOC?", 16)

def BatterySimulator_GetESR(ksocket):
    return instrQuery(ksocket, ":BATT:SIM:RES?", 16)

def BatterySimulator_GetOverVoltageProtection(ksocket):
    return instrQuery(ksocket, ":BATT:SIM:TVOL:PROT?", 16)

def BatterySimulator_GetOverCurrentProtection(ksocket):
    return instrQuery(ksocket, ":BATT:SIM:CURR:PROT?", 16)


