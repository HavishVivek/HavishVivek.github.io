---
layout: post
title: range game
tags: ble electronics
---

I learned about so many components in the past few months. So, I devised a plan which was to build a game. That game is called the "Range Sensing Game.”Here are the components that I have used and their purpose of them. If you wish, use the circuit and code to replicate the project at your house.

**Components:**

# Level Shifting with Resistors

1. Used for lower voltage from high voltage
2. from 1.4v to 2.5v can trigger the gpio pins to go high
3. voltage divider can be created with just 2 resistor or more

# Absolute value in python

1. absolute value tell how far away th number is from 0
2. It remove he negive/positive sign

# Modifying a File for Import use

1. when you import a python file to different python file it runs line by line

```
if __name__ == "__main__":
	while True:
		print("hello world")
```

1. This code will run if the code ran from orginall program but not from a import file

**Circuit:**

![game](../pics/game.png)

1. rgb red to pin 13, green to 19, blue to pin 26
2. oled gnd to gnd, vcc to 3.3v scl to scl, sda to sda
3. switch middle pin to gnd, left pin to pin 16
4. ultra sonic sensor gnd to gnd, vcc to 5v, echo pin to voltage divider of 2 1k resistor is siries to gnd, trigger to pin 21

**Code:**
