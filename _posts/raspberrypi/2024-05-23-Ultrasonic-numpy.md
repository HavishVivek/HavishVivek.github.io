---
layout: post
title: Ultrasonic Sensor numpy
tags: electronics,raspberrypi
---

I was building a range sensing game. I didn't known how to use Ultrasonic sensor and the numpy libary. So I came up with a plan to learn about ultrasonic sensor and the numpy libary.Here are the components that I have used and their purpose of them. If you wish, use the circuit and code to replicate the project at your house.

**Components:**

# ultrasonic sensor

1. Made up of an ultrasonic emitter and receiver and a small circuit to control the emitter and receiver
2. It needs to be connected with level shifting IC chip not directly to the Raspberry Pi but the input/trigger pin is safe to connect directly to GPIO pins and the output pin should be connected to the level-shifting
3. A signal is sound waves protected by the emitter which is higher than the human hearing range. That signal is bounced off an object and received by the receiver.
4. The signal travels through the air at 343 meters per second
5. rangefinder sends out a signal because the program triggers it. From the program, the ultrasonic sensor sends a short signal at 40kHz from the emitter. When the ultrasonic sensor receives a signal of 40kHz then the echo pin goes high. If the echo pin is low then keep resetting the starting counter value. If the echo pin is high then update the end-counting value

**Circuit:**

![Ultrasonic Circuit](../pics/ultrasonic.png)

1. The rgb is connected to 1k ohms resistor and red is connected to pin 13, green to pin 19, and blue to pin 26
2. DIR and vcc pin of the ic chip is connected and DIR pin is connected 3.3v
3. A1 is connected to the echo pin of the sensor
4. GND is connected to OE of the ic chip and GND is connected to the gnd of the raspberrypi

**Code:**

Here is the code for the ultrasonic sensor with numpy and rgb led control.:

[ultrasonic](https://github.com/HavishVivek/projectLab/blob/raspberrypi/42Electronics/lesson%20B-14/ultrasonic.py)
