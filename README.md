# Finger Bite Screen Off (macOS)

Local computer-vision app that watches for a "finger near mouth" gesture and puts your display to sleep on macOS.

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

## Quick Start (Local)

```bash
cd finger-bite-screen-off
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

- **Push fails with `does not appear to be a git repository`**
  - Your remote is likely wrong (example of wrong: `origin finger_biting`).
  - Set a full GitHub URL:
    - `git remote set-url origin https://github.com/<username>/finger-bite-screen-off.git`
  - Then push again: `git push -u origin main`

- **Camera not opening**
  - Grant camera access in macOS Privacy settings for the app you're running from.