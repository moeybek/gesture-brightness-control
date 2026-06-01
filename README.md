# Hand Gesture Brightness Control with OpenCV and MediaPipe

A real-time computer vision project that detects hand landmarks using MediaPipe and maps finger movement to a brightness-control value.

The original goal was to control the actual screen brightness using the distance between the thumb and index finger. On macOS, direct screen brightness control is hardware- and OS-dependent, so this version visualizes the brightness percentage inside the OpenCV window instead of changing the real display brightness.

## Project Purpose

This project demonstrates how hand gestures can be used as an input method for human-computer interaction.

The program uses a webcam to detect a hand, tracks the thumb and index fingertip positions, calculates the distance between them, and converts that distance into a brightness percentage from 0% to 100%.

## Features

- Real-time webcam capture
- Hand landmark detection using MediaPipe
- Thumb and index finger tracking
- Finger-distance calculation
- Brightness percentage mapping
- OpenCV visual overlay
- Brightness bar visualization
- macOS-compatible camera backend
- Safe handling when the camera is unavailable

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- Python virtual environment

## How It Works

MediaPipe detects 21 hand landmarks for each hand.

This project uses two specific landmarks:

| Landmark ID | Finger Part |
|---|---|
| 4 | Thumb tip |
| 8 | Index finger tip |

The distance between these two points is calculated using the Euclidean distance formula:

```python
L = hypot(x2 - x1, y2 - y1)
```

That distance is then mapped to a brightness percentage:

```python
brightness_percent = int(np.interp(L, [15, 220], [0, 100]))
```

Small distance:

```text
Thumb close to index finger → low brightness value
```

Large distance:

```text
Thumb far from index finger → high brightness value
```

## Demo Behavior

When the program runs:

1. The webcam opens.
2. The hand is detected.
3. Landmarks are drawn on the hand.
4. A circle is drawn on the thumb tip.
5. A circle is drawn on the index fingertip.
6. A line is drawn between the two fingertips.
7. The finger distance is converted into a value from 0% to 100%.
8. A brightness bar is shown on the screen.

## Project Structure

```text
gesture-brightness-control/
├── README.md
├── project.py
├── requirements.txt
├── .gitignore
└── demo/
    └── screenshot.png
```

## Installation

Create and activate a virtual environment.

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

## Requirements

Example `requirements.txt`:

```text
opencv-python
mediapipe==0.10.14
numpy
```

MediaPipe version `0.10.14` is used because this project relies on the classic MediaPipe `solutions` API:

```python
mp.solutions.hands
```

Newer MediaPipe versions may use the newer `tasks` API and may not expose `mp.solutions`.

## Running the Project

Run:

```bash
python project.py
```

Press `Esc` to close the camera window.

## macOS Camera Permission

If the camera does not open on macOS, enable camera access:

```text
System Settings → Privacy & Security → Camera
```

Enable access for:

```text
Terminal
Visual Studio Code
Python
```

Then restart the terminal or VS Code and run the script again.

## Main Code Logic

```python
x1, y1 = landmarkList[4][1], landmarkList[4][2]
x2, y2 = landmarkList[8][1], landmarkList[8][2]

L = hypot(x2 - x1, y2 - y1)

brightness_percent = int(np.interp(L, [15, 220], [0, 100]))
brightness_percent = max(0, min(100, brightness_percent))
```

This code extracts the thumb and index fingertip coordinates, calculates their distance, and maps the result to a percentage.

## Known Limitations

- This project currently visualizes brightness instead of changing actual screen brightness.
- Direct brightness control depends on the operating system, display type, permissions, and hardware.
- On macOS, external monitors, adapters, docks, or Apple Silicon display paths may block software brightness control.
- Lighting conditions affect hand detection accuracy.
- The webcam must clearly see the hand.
- The distance range `[15, 220]` may need adjustment depending on camera resolution and hand distance from the camera.

## Possible Improvements

- Add real brightness control for supported systems.
- Add support for multiple gestures.
- Add gesture smoothing to reduce flickering.
- Add support for volume control.
- Add a graphical user interface.
- Add left-hand/right-hand detection.
- Add a calibration step for different users and camera distances.
- Add support for all fingers instead of only thumb and index finger.

## Learning Outcomes

This project helped practice:

- Real-time image processing
- Webcam handling with OpenCV
- Hand tracking with MediaPipe
- Landmark-based gesture recognition
- Distance calculation between points
- Mapping sensor-like input to control values
- Handling package compatibility issues
- Working with Python virtual environments
- Debugging macOS camera and display-control limitations

## Author

Moawia Sardar Bagdash

## License

This project is for learning and portfolio demonstration purposes.