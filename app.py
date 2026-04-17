import math
import subprocess
import time
from dataclasses import dataclass

import cv2
import mediapipe as mp


@dataclass
class Config:
    # Distance threshold in normalized image coordinates.
    bite_distance_threshold: float = 0.08
    # Number of consecutive frames that must match before action.
    confirm_frames: int = 6
    # Minimum seconds between screen-off events.
    cooldown_seconds: float = 4.0
    # Show preview window.
    show_preview: bool = True


MOUTH_LANDMARKS = [13, 14, 78, 308]  # upper/lower lip + corners
INDEX_TIP = 8


def euclidean(a, b) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def mouth_center(face_landmarks):
    xs = [face_landmarks.landmark[i].x for i in MOUTH_LANDMARKS]
    ys = [face_landmarks.landmark[i].y for i in MOUTH_LANDMARKS]
    return sum(xs) / len(xs), sum(ys) / len(ys)


def sleep_display_now():
    # macOS display sleep command.
    subprocess.run(["pmset", "displaysleepnow"], check=False)


def run(config: Config):
    if not hasattr(mp, "solutions"):
        raise RuntimeError(
            "Your installed mediapipe package does not include `solutions`. "
            "Use `pip install -r requirements.txt` to install the compatible version."
        )

    mp_hands = mp.solutions.hands
    mp_face_mesh = mp.solutions.face_mesh
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    bite_frame_streak = 0
    last_trigger = 0.0

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.5,
    ) as hands, mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.5,
    ) as face_mesh:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            hand_result = hands.process(rgb)
            face_result = face_mesh.process(rgb)

            bite_detected = False
            draw_distance = None

            if (
                hand_result.multi_hand_landmarks
                and face_result.multi_face_landmarks
            ):
                face = face_result.multi_face_landmarks[0]
                m_center = mouth_center(face)

                # Check every detected hand.
                for hand_landmarks in hand_result.multi_hand_landmarks:
                    tip = hand_landmarks.landmark[INDEX_TIP]
                    d = euclidean((tip.x, tip.y), m_center)
                    draw_distance = d if draw_distance is None else min(draw_distance, d)
                    if d < config.bite_distance_threshold:
                        bite_detected = True

                    if config.show_preview:
                        mp_draw.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                        )

                if config.show_preview:
                    ih, iw, _ = frame.shape
                    mx, my = int(m_center[0] * iw), int(m_center[1] * ih)
                    cv2.circle(frame, (mx, my), 6, (0, 200, 255), -1)

            bite_frame_streak = bite_frame_streak + 1 if bite_detected else 0

            now = time.time()
            if (
                bite_frame_streak >= config.confirm_frames
                and now - last_trigger > config.cooldown_seconds
            ):
                sleep_display_now()
                last_trigger = now
                bite_frame_streak = 0

            if config.show_preview:
                text = f"bite={bite_detected} streak={bite_frame_streak}"
                if draw_distance is not None:
                    text += f" dist={draw_distance:.3f}"
                cv2.putText(
                    frame,
                    text,
                    (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (0, 255, 0) if bite_detected else (0, 165, 255),
                    2,
                )
                cv2.putText(
                    frame,
                    "Press q to quit",
                    (15, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (255, 255, 255),
                    2,
                )
                cv2.imshow("Finger Bite Detector", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run(Config())
