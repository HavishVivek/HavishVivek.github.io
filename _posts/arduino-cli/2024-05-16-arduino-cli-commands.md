---
layout: post
title: Arduino-cli commands
tags: cli Terminal
---

In this tutorial, let's explore 10 different Arduino-cli commands

## 1. Arduino-cli version

This command will display the installed version of Arduino-cli

```
$ arduino-cli version
```

## 2. Arduino-cli compile

This command will compile your sketch

Arduino board compile

```
$ arduino-cli compile -b arduino:avr:uno the path to the arduino sketch
```

Esp32 board compile

```
$ arduino-cli compile -fqbn esp32:esp32:esp32 the path to the arduino sketch
```

## 3. Arduino-cli upload

This command will upload your sketch

Arduino board upload

```
$ arduino-cli upload the path to the arduino sketch -p the port where the board is connected -b arduino:avr:uno
```

Esp32 board upload

```
$ arduino-cli upload -p the port where the board is connected -fqbn esp32:esp32:esp32 the path to the arduino sketch
```

## 4. Arduino-cli monitor

```
$ arduino-cli monitor -p the port where the board is connected
```

## 5. Arduino-cli board list/posrt list

This command will list the available boards and ports

```
$ arduino-cli board list
```

## 6. Arduino-cli library list

This command will list the available libraries

```
$ arduino-cli lib list
```

## 7. Arduino-cli core list

This command will list the available cores

```
$ arduino-cli core list
```

## 8. Arduino-cli library upgrade

This command will upgrade the library

```
$ arduino-cli lib upgrade
```

## 9. Arduino-cli core upgrade

This command will upgrade the core

```
$ arduino-cli core upgrade
```

## 10. Arduino-cli sketch

This command will create a new sketch

```
$ arduino-cli sketch new name of the sketch
```
