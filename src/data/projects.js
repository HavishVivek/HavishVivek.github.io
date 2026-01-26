// ===== PROJECTS DATA =====
// Add your projects here

export const projects = [
  {
    id: 1,
    title: "Smart Home Automation Hub",
    description: "A central hub for controlling all smart devices in your home using ESP32 and MQTT protocol with a custom mobile app.",
    category: "IoT",
    image: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=400&fit=crop",
    tech: ["ESP32", "MQTT", "React Native", "Node.js"],
    demo: "https://demo.example.com",
    github: "https://github.com/yourusername/smart-home",
    // Extended content for project page
    content: `
## Overview

This Smart Home Automation Hub serves as the central nervous system for all IoT devices in your home. Built with an ESP32 microcontroller at its core, it communicates with various sensors and actuators throughout the house using the MQTT protocol.

## Key Features

- **Centralized Control**: Manage all smart devices from a single dashboard
- **Real-time Monitoring**: Live sensor data with historical charts
- **Automation Rules**: Create custom triggers and schedules
- **Voice Integration**: Works with Alexa and Google Assistant
- **Mobile App**: Control your home from anywhere

## Technical Details

The system uses a hub-and-spoke architecture where the ESP32 acts as the main controller. Each room has sensor nodes that communicate via MQTT to a local broker running on a Raspberry Pi.

### Hardware Components
- ESP32-WROOM-32 as the main controller
- DHT22 temperature/humidity sensors
- PIR motion sensors
- Relay modules for controlling appliances
- OLED displays for local status

### Software Stack
- PlatformIO for ESP32 firmware development
- Mosquitto MQTT broker
- Node.js backend API
- React Native mobile application
- InfluxDB for time-series data
    `,
    // Optional: Link to a video demo (use videoId from your videos data)
    videoId: "1x8C_1eKAoo",
    // Optional: Blog post content
    blogPost: {
      title: "Building a Smart Home Hub from Scratch",
      content: `
# Building a Smart Home Hub from Scratch

In this post, I'll walk you through how I built my own smart home automation hub using affordable components and open-source software.

## Why Build Your Own?

Commercial smart home solutions often lock you into proprietary ecosystems. By building your own, you get:

1. **Complete control** over your data and privacy
2. **Flexibility** to integrate any device
3. **Cost savings** in the long run
4. **Learning experience** in IoT and embedded systems

## Getting Started

The first step was choosing the right microcontroller. I went with the ESP32 because of its built-in WiFi and Bluetooth, dual-core processor, and excellent community support.

## Challenges Faced

The biggest challenge was ensuring reliable communication between all devices. MQTT solved this elegantly with its publish-subscribe model and QoS levels.

## Results

After three months of development, I now have a fully functional smart home system that controls:
- 12 smart lights
- 4 temperature sensors
- 2 motion-activated cameras
- Automated blinds
- Smart thermostat integration

## What's Next?

I'm currently working on adding machine learning to predict occupancy patterns and optimize energy usage automatically.
      `
    },
    // Components used in the project
    components: [
      {
        name: "ESP32-WROOM-32",
        description: "The brain of the smart home hub. This powerful dual-core microcontroller handles all sensor data processing, WiFi communication, and MQTT messaging.",
        image: "https://images.unsplash.com/photo-1608564697071-ddf911d81370?w=600&h=400&fit=crop",
        specs: [
          "240 MHz dual-core processor",
          "520 KB SRAM",
          "Built-in WiFi & Bluetooth",
          "34 programmable GPIO pins",
          "Ultra-low power consumption"
        ],
        role: "Acts as the central hub coordinator, receiving sensor data from nodes and sending commands to actuators via MQTT protocol."
      },
      {
        name: "DHT22 Temperature Sensor",
        description: "High-precision digital sensor for measuring ambient temperature and humidity levels throughout the home.",
        image: "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&h=400&fit=crop",
        specs: [
          "Temperature range: -40°C to 80°C",
          "Humidity range: 0-100% RH",
          "±0.5°C temperature accuracy",
          "Single-wire digital interface",
          "2-second sampling period"
        ],
        role: "Monitors room temperature and humidity for climate control automation and energy optimization."
      },
      {
        name: "PIR Motion Sensor",
        description: "Passive infrared sensor that detects movement by measuring changes in infrared radiation from warm bodies.",
        image: "https://images.unsplash.com/photo-1580584126903-c17d41830450?w=600&h=400&fit=crop",
        specs: [
          "Detection range: up to 7 meters",
          "120° detection angle",
          "Adjustable sensitivity",
          "Low power standby mode",
          "3.3V - 5V operating voltage"
        ],
        role: "Triggers automated lighting, security alerts, and occupancy-based climate adjustments."
      },
      {
        name: "4-Channel Relay Module",
        description: "Optically isolated relay module for safely controlling high-voltage AC appliances from low-voltage microcontroller signals.",
        image: "https://images.unsplash.com/photo-1597225244660-1cd128c64284?w=600&h=400&fit=crop",
        specs: [
          "4 independent channels",
          "10A @ 250VAC capacity",
          "Optocoupler isolation",
          "LED status indicators",
          "Active-low trigger"
        ],
        role: "Switches power to lights, fans, and other appliances based on automation rules and user commands."
      },
      {
        name: "0.96\" OLED Display",
        description: "Compact monochrome display for showing real-time status, sensor readings, and system information locally.",
        image: "https://images.unsplash.com/photo-1601134467661-3d775b999c8b?w=600&h=400&fit=crop",
        specs: [
          "128x64 pixel resolution",
          "I2C interface (SSD1306)",
          "High contrast ratio",
          "Wide viewing angle",
          "3.3V compatible"
        ],
        role: "Displays current temperature, humidity, device status, and network connection info without needing a phone."
      }
    ],
    // Schematic images
    schematic: {
      title: "System Wiring Diagram",
      description: "Complete circuit diagram showing how all components connect to the ESP32 hub",
      images: [
        "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&h=600&fit=crop",
        "https://images.unsplash.com/photo-1597225244660-1cd128c64284?w=800&h=600&fit=crop"
      ],
      notes: [
        "Use 10kΩ pull-up resistors on I2C lines",
        "Add 100µF capacitor near ESP32 power pins",
        "Keep relay module wiring separate from sensor wiring",
        "Use shielded cables for longer sensor runs"
      ]
    }
  },
  {
    id: 2,
    title: "AI-Powered Plant Monitor",
    description: "Uses computer vision and ML to identify plant diseases and monitor soil conditions with automated watering.",
    category: "ML/AI",
    image: "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=600&h=400&fit=crop",
    tech: ["Raspberry Pi", "TensorFlow", "Python", "OpenCV"],
    demo: "https://demo.example.com",
    github: "https://github.com/yourusername/plant-monitor",
    content: `
## Overview

This project combines computer vision with IoT sensors to create an intelligent plant monitoring system. It can identify plant diseases from leaf images and automatically adjust watering based on soil conditions.

## Key Features

- **Disease Detection**: Identifies 38 different plant diseases using a trained CNN model
- **Soil Monitoring**: Measures moisture, pH, and nutrient levels
- **Automated Watering**: Smart irrigation based on plant needs
- **Growth Tracking**: Time-lapse photography and growth analytics
- **Mobile Alerts**: Push notifications for plant health issues

## How It Works

A Raspberry Pi with a camera module takes periodic photos of your plants. The images are processed through a TensorFlow Lite model trained on the PlantVillage dataset to detect any signs of disease.

### The ML Pipeline

1. Image capture and preprocessing
2. Inference using TensorFlow Lite
3. Disease classification with confidence scores
4. Alert generation if disease detected
5. Historical tracking and trends

## Hardware Setup

- Raspberry Pi 4 (4GB)
- Pi Camera Module v2
- Capacitive soil moisture sensors
- Peristaltic pumps for watering
- Custom 3D printed enclosure
    `,
    videoId: "8vqFXcyE1nk",
    blogPost: null
  },
  {
    id: 3,
    title: "Custom Mechanical Keyboard",
    description: "Designed and built a custom split ergonomic keyboard with custom PCB, firmware, and RGB lighting.",
    category: "Electronics",
    image: "https://images.unsplash.com/photo-1595225476474-87563907a212?w=600&h=400&fit=crop",
    tech: ["KiCad", "QMK", "C", "3D Printing"],
    demo: "https://demo.example.com",
    github: "https://github.com/yourusername/custom-keyboard",
    content: `
## Overview

A fully custom split ergonomic mechanical keyboard designed from scratch. This project includes custom PCB design, 3D printed case, QMK firmware, and per-key RGB lighting.

## Design Goals

- **Ergonomic Layout**: Split design with column stagger to reduce strain
- **Portable**: Compact 36-key layout (18 per half)
- **Wireless Option**: Bluetooth connectivity via nice!nano controllers
- **Hot-swappable**: Easy switch changes without soldering
- **Full RGB**: Per-key addressable LEDs

## PCB Design

The PCB was designed in KiCad with careful attention to:
- Minimal trace lengths for the key matrix
- Proper power delivery for LEDs
- ESD protection on USB lines
- Mounting holes aligned with case design

## Firmware Features

Running QMK firmware with custom features:
- Multiple layers (Base, Symbols, Numbers, Navigation)
- Tap-dance for dual-function keys
- RGB animations and per-key colors
- Mouse keys for trackpad-free operation

## Build Process

1. PCB design and ordering from JLCPCB
2. Case design in Fusion 360
3. 3D printing in matte black PLA
4. SMD component soldering
5. Switch and keycap installation
6. Firmware flashing and testing
    `,
    videoId: null,
    blogPost: {
      title: "Designing Your First Custom Keyboard PCB",
      content: `
# Designing Your First Custom Keyboard PCB

Creating a custom mechanical keyboard from scratch is one of the most rewarding electronics projects. Here's my complete guide.

## Tools You'll Need

- **KiCad**: Free and open-source PCB design software
- **Keyboard Layout Editor**: For planning your layout
- **Ergogen**: Optional tool for generating keyboard PCBs
- **Fusion 360**: For case design

## The Key Matrix

Understanding the key matrix is crucial. Instead of one wire per key (which would need 36+ GPIO pins), we use a matrix of rows and columns.

For a 6x6 matrix, we only need 12 GPIO pins to read 36 keys. The firmware scans each row and reads which columns are active.

## Diode Direction

Each switch needs a diode to prevent ghosting. The convention in QMK is COL2ROW, meaning the diode's cathode (stripe) points toward the row.

## Lessons Learned

1. Always double-check your footprints
2. Order extra PCBs - they're cheap in quantity
3. Test with a multimeter before soldering switches
4. Document your pinout for the firmware

Happy building!
      `
    }
  },
  {
    id: 4,
    title: "Edge AI Object Detection",
    description: "Real-time object detection running on edge devices for security and automation applications.",
    category: "ML/AI",
    image: "https://images.unsplash.com/photo-1555255707-c07966088b7b?w=600&h=400&fit=crop",
    tech: ["Jetson Nano", "YOLO", "TensorRT", "Python"],
    demo: "https://demo.example.com",
    github: "https://github.com/yourusername/edge-detection",
    content: `
## Overview

This project brings real-time object detection to edge devices using optimized neural networks. Running YOLO on a Jetson Nano achieves 25+ FPS while consuming only 10W of power.

## Use Cases

- **Home Security**: Detect people, vehicles, and packages
- **Wildlife Monitoring**: Track animals without cloud connectivity
- **Industrial Automation**: Quality control and safety monitoring
- **Smart Retail**: Customer counting and behavior analysis

## Performance Optimization

Getting real-time performance on edge devices requires careful optimization:

### TensorRT Conversion
Converting PyTorch models to TensorRT provides 3-4x speedup through:
- Layer fusion
- Kernel auto-tuning
- FP16/INT8 quantization
- Memory optimization

### Model Selection
After testing various architectures:
- YOLOv5s: 30 FPS, good accuracy
- YOLOv5n: 45 FPS, slightly lower accuracy
- Custom trained: 35 FPS, best for specific use case

## System Architecture

The system uses a modular pipeline:
1. Camera capture (GStreamer)
2. Preprocessing (CUDA)
3. Inference (TensorRT)
4. Post-processing (NumPy)
5. Visualization (OpenCV)
6. MQTT alerts
    `,
    videoId: "rZ3txAetVzQ",
    blogPost: null
  },
  {
    id: 5,
    title: "Weather Station Network",
    description: "Distributed weather monitoring system with multiple nodes reporting to a central dashboard.",
    category: "IoT",
    image: "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=600&h=400&fit=crop",
    tech: ["Arduino", "LoRa", "Grafana", "InfluxDB"],
    demo: "https://demo.example.com",
    github: "https://github.com/yourusername/weather-station",
    content: `
## Overview

A network of solar-powered weather stations that communicate via LoRa radio to a central gateway. Data is stored in InfluxDB and visualized with Grafana dashboards.

## Network Architecture

Each node operates independently with:
- Solar panel + battery for power
- LoRa radio for long-range communication (up to 10km)
- Multiple environmental sensors
- Local data logging as backup

## Sensors Per Node

- **BME280**: Temperature, humidity, pressure
- **Wind Speed**: Cup anemometer with Hall sensor
- **Wind Direction**: Magnetic encoder
- **Rain Gauge**: Tipping bucket design
- **UV Index**: VEML6075 sensor
- **Soil Temperature**: DS18B20 probe

## Data Pipeline

1. Sensors read every 5 minutes
2. Data packaged into LoRa packet
3. Gateway receives and validates
4. Stored in InfluxDB
5. Grafana queries and displays
6. Alerts via Telegram bot

## Dashboard Features

- Real-time current conditions
- Historical trends and comparisons
- Weather predictions using ML
- Automated frost/storm alerts
- Data export for analysis
    `,
    videoId: null,
    blogPost: null
  },
  {
    id: 6,
    title: "Voice-Controlled Robot Arm",
    description: "A 6-DOF robot arm controlled by voice commands using speech recognition and inverse kinematics.",
    category: "Electronics",
    image: "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600&h=400&fit=crop",
    tech: ["Servo Motors", "Python", "Speech Recognition", "ROS"],
    demo: "https://demo.example.com",
    github: "https://github.com/yourusername/robot-arm",
    content: `
## Overview

A 6 degree-of-freedom robot arm that responds to natural language voice commands. "Pick up the red block" triggers a sequence of computer vision, path planning, and precise motor control.

## Degrees of Freedom

1. **Base Rotation**: 180° horizontal sweep
2. **Shoulder**: 135° vertical movement
3. **Elbow**: 135° arm extension
4. **Wrist Pitch**: 180° up/down
5. **Wrist Roll**: 360° rotation
6. **Gripper**: Variable grip force

## Voice Command Processing

The speech pipeline uses:
1. **Wake Word**: "Hey Robot" using Porcupine
2. **Speech-to-Text**: Whisper (local) or Google Speech API
3. **Intent Parsing**: Custom NLU for robotic commands
4. **Action Mapping**: Convert intent to motion sequence

## Inverse Kinematics

Given a target position (x, y, z), the IK solver calculates the required joint angles. I implemented:
- Analytical IK for the arm
- Numerical IK using scipy.optimize for complex poses
- Collision avoidance using workspace boundaries

## Safety Features

- Soft torque limits on all joints
- Emergency stop button
- Workspace boundary enforcement
- Gradual acceleration/deceleration
    `,
    videoId: "2og7jTySUs4",
    blogPost: {
      title: "Implementing Inverse Kinematics for Robot Arms",
      content: `
# Implementing Inverse Kinematics for Robot Arms

Inverse kinematics (IK) is the mathematical process of calculating joint angles needed to reach a target position. Here's how I implemented it.

## Forward vs Inverse Kinematics

**Forward Kinematics**: Given joint angles → Calculate end position
**Inverse Kinematics**: Given target position → Calculate joint angles

Forward kinematics is straightforward trigonometry. Inverse kinematics is much harder because:
- Multiple solutions may exist
- No solution may exist (out of reach)
- Singularities cause numerical issues

## My Approach

For a 6-DOF arm, I used a combination:

### Analytical Solution (Joints 1-3)
The first three joints determine the wrist position. Using geometric relationships:

\`\`\`python
def calculate_base_angle(x, y):
    return math.atan2(y, x)

def calculate_shoulder_elbow(x, y, z, l1, l2):
    r = math.sqrt(x**2 + y**2)
    d = math.sqrt(r**2 + z**2)
    # Law of cosines for elbow
    cos_elbow = (l1**2 + l2**2 - d**2) / (2 * l1 * l2)
    # ... continues
\`\`\`

### Numerical Solution (Joints 4-6)
The wrist orientation uses scipy.optimize to minimize the error between current and target orientation.

## Testing Tips

1. Start with forward kinematics - verify your math
2. Test IK at known positions
3. Add joint limits gradually
4. Visualize the workspace

Good luck with your robot arm project!
      `
    },
    components: [
      {
        name: "MG996R Servo Motors",
        description: "High-torque digital servo motors providing the muscle for each joint of the robot arm. These metal-gear servos handle the heavy lifting.",
        image: "https://images.unsplash.com/photo-1597225244660-1cd128c64284?w=600&h=400&fit=crop",
        specs: [
          "Stall torque: 11 kg-cm @ 6V",
          "Operating speed: 0.17s/60°",
          "Metal gear train",
          "PWM control signal",
          "4.8V - 7.2V operating range"
        ],
        role: "Powers the base rotation, shoulder, and elbow joints requiring high torque for lifting objects."
      },
      {
        name: "SG90 Micro Servos",
        description: "Lightweight micro servos perfect for the wrist joints where precision matters more than raw power.",
        image: "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&h=400&fit=crop",
        specs: [
          "Stall torque: 1.8 kg-cm",
          "Operating speed: 0.1s/60°",
          "Plastic gear train",
          "9g weight",
          "4.8V operating voltage"
        ],
        role: "Controls wrist pitch, roll, and gripper mechanisms where weight needs to be minimized."
      },
      {
        name: "Arduino Mega 2560",
        description: "The main controller board with enough PWM outputs to control all six servo motors simultaneously with precise timing.",
        image: "https://images.unsplash.com/photo-1608564697071-ddf911d81370?w=600&h=400&fit=crop",
        specs: [
          "ATmega2560 microcontroller",
          "54 digital I/O pins",
          "15 PWM outputs",
          "16 MHz clock speed",
          "256 KB flash memory"
        ],
        role: "Runs the inverse kinematics calculations and generates PWM signals for all servo motors."
      },
      {
        name: "PCA9685 PWM Driver",
        description: "16-channel PWM driver that offloads servo control from the main processor, providing smoother motion control.",
        image: "https://images.unsplash.com/photo-1601134467661-3d775b999c8b?w=600&h=400&fit=crop",
        specs: [
          "16 independent PWM channels",
          "12-bit resolution (4096 steps)",
          "I2C interface",
          "Adjustable frequency 24-1526Hz",
          "Chainable for more channels"
        ],
        role: "Provides precise PWM signals to all servos with smooth interpolation between positions."
      },
      {
        name: "USB Microphone Array",
        description: "Multi-element microphone for voice command input with noise cancellation and beamforming capabilities.",
        image: "https://images.unsplash.com/photo-1580584126903-c17d41830450?w=600&h=400&fit=crop",
        specs: [
          "4-microphone array",
          "Far-field voice capture",
          "Built-in noise reduction",
          "USB audio interface",
          "360° voice pickup"
        ],
        role: "Captures voice commands and feeds them to the Raspberry Pi running speech recognition."
      }
    ],
    schematic: {
      title: "Robot Arm Wiring Diagram",
      description: "Complete electrical connections for the 6-DOF robot arm with voice control",
      images: [
        "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&h=600&fit=crop"
      ],
      notes: [
        "Use a separate 5V 10A power supply for servos",
        "Add 1000µF capacitor on servo power rail",
        "Keep logic and servo grounds connected",
        "Use level shifter for 3.3V to 5V PWM signals"
      ]
    }
  }
];

export const projectFilters = ['All', 'IoT', 'ML/AI', 'Electronics'];

// Helper function to get project by ID
export const getProjectById = (id) => {
  return projects.find(p => p.id === parseInt(id));
};
