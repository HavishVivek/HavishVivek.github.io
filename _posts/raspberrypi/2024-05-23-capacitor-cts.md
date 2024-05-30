---
layout: post
title: Capacitor CTS
tags: raspberrypi capacitor CTS electronics
---

I wanted to build a multimeter with different functionalities. I also wanted to build a secret password. So learned capacitor and capacitive touch sensors.

\*_component:_

# Capacitors

1. capacitor is used for storing energy and discharging it into other components
2. the amount of energy a capacitor can store is called a capacitance
3. capacitance is measured in Farad/microfarad
4. Symbol of microfarad = uF

   ## Capacitor Construction

   1. The energy is stored in two foil
   2. small capacitors are not polarized but big capacitors (electrolytic)are polarized

   ## Current limiting

   1. The capacitor charge will discharge as fast as electrons flow
   2. the fully discharged capacitor will act like a short circuit
   3. when more charge goes into the capacitor it can damage the power supply
   4. when a fully charged capacitor is connected to a low gpio it could damage it
   5. When connecting a fully changed capacitor into a gpio pin use a current limiting resistor so it does not exceed 16mA

   ### Charge time

   1. charge time = the time it for the capacitor to be fully charged
   2. The time will be affected by the capacitance value and voltage value

   ### Calculating charge time

   1. The value for calculating charge time is RC time constant
   2. One rc time constant = 63% charged up
   3. Five rc time constant = 100% charged up
   4. The more charge is stored in the first couple of RC time constant

   ### Parallel vs Series

   1. when calculating resistor is series. That can be achieved when capacitors are in parallel

# Capacitive Touch Sensor

1. when the pad is not touched it is low but when touched it becomes high
2. Safe to connect to gpio pin and they output 3.3v
3. The CTS uses a baseline measure to know when pads are touched
4. When CTS is first turned on do not touch it because it changes the baseline measurement

**Circuit:**

Capacitor

![image](../pics/cap.png)

1. Red is connected to gpio 13, green is connected to gpio 19, blue is connected to gpio 26
2. oled is connected to 5v and gnd. scl to scl pin and sda to sda pin
3. switch is connted to gnd and gpio 21
4. capacitors connted in parallel. Connected to gnd and gpio 20

![img](../pics/cts.png)
**Code:**
