# Finger Bite Screen Off (macOS)

A small local computer-vision app that watches for a "finger near mouth" gesture and puts your display to sleep on macOS.

## Features

- Real-time webcam detection with OpenCV + MediaPipe.
- Requires multiple matching frames to reduce accidental triggers.
- Cooldown between triggers.
- Local processing only (no cloud calls in this script).

## How It Works

The app tracks:

- your index fingertip position (from hand landmarks), and
- an approximate mouth center (from face landmarks).

If the fingertip stays close to the mouth for several consecutive frames, it runs:

```bash
pmset displaysleepnow
```

## Requirements

- macOS
- Python 3.9+
- Webcam access permission for your terminal app (Terminal/Cursor)

## Quick Start

```bash
cd /Users/james/Desktop/ECE495/finger-bite-screen-off
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Press `q` to quit.

## Configuration

Tune behavior in `Config` in `app.py`:

- `bite_distance_threshold`: lower = stricter gesture distance.
- `confirm_frames`: higher = fewer false positives.
- `cooldown_seconds`: minimum time between screen-off triggers.
- `show_preview`: `True` to display webcam overlay, `False` for no preview window.

## Troubleshooting

- **`ModuleNotFoundError: mediapipe`**
  - Make sure the virtualenv is active: `source .venv/bin/activate`
  - Reinstall deps: `pip install -r requirements.txt`

- **`module 'mediapipe' has no attribute 'solutions'`**
  - Install the pinned compatible version in `requirements.txt`.

- **Camera not opening**
  - Grant camera access in macOS Privacy settings for the app you're running from.

## Share It With Friends (GitHub)

From the project folder:

```bash
git init
git add .
git commit -m "Initial commit: finger bite screen off app"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

Then share the GitHub link. Your friend can clone and run using the Quick Start section above.

## License

MIT
