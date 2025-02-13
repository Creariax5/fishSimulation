# Fish Collective Behavior Simulation

A PyGame simulation demonstrating emergent collective behavior in fish schools with predator-prey dynamics.

![2025-01-01 16_49_49-fps_ 61    bobs_ 343](https://github.com/user-attachments/assets/7ad3e2ad-51f8-4681-b142-cc2fc7ed0323)

## Features

### Fish (Blue)
- Form schools based on neighbor positions
- Avoid predators
- Seek food
- Reproduce when eating food

### Shark (Red)
- Hunts nearby fish
- Removes caught fish from simulation

### Environment
- Food particles spawn periodically
- Wraparound borders
- Real-time FPS and population counter

## Controls
- **Show GUI**: Toggle control buttons
- **Show Direction**: Toggle movement vectors

## Running the Simulation

1. Install dependencies:
```bash
pip install pygame
```

2. Run:
```bash
python main.py
```

## How It Works

The simulation demonstrates emergent collective behavior through simple rules:
1. Fish maintain optimal distances from neighbors
2. Align swimming direction with nearby fish
3. Flee from predators
4. Seek food for reproduction

These basic individual behaviors result in complex group patterns like school formation, predator avoidance, and dynamic population balance.

## Dependencies
- Python 3.x
- PyGame

## License
MIT License
