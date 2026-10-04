import threading
from collections import deque
import requests



# Parameters
STREAM_URL = "http://192.168.1.200:3102/stream.mjpg"

STREAM_DECODE_SIZE = (320, 180)         # Video size to process for motion
STREAM_FRAMERATE = 30                   # Stream FPS to match

MOTION_THRESHOLD_PCT = 0.025            # % diff of pixels between frames threshold to activate recording
MOTION_LOOKBACK_SECONDS = 0.25          # Seconds for pixel diff ratios to be stored in diff_buffer

RECORD_PREROLL_SECONDS = 5              # Seconds before reading for motion

VIDEO_MAX_LEN_SECONDS = 120             # Max Video duration

BUFFER_READ_CURSOR = RECORD_PREROLL_SECONDS * STREAM_FRAMERATE  # Index cursor to current frame
BUFFER_READ_SIZE = (                    # Max Buffer read size (generous size)
        BUFFER_READ_CURSOR +
        VIDEO_MAX_LEN_SECONDS * 3 * STREAM_FRAMERATE
)
BUFFER_THRESHOLD_SIZE = MOTION_LOOKBACK_SECONDS * STREAM_FRAMERATE # Max Buffer thershold size



# Buffers
buffer_lock = threading.Lock()
read_buffer = deque(maxlen=BUFFER_READ_SIZE)
rec_buffer = deque()
proc_buffer = deque(maxlen=5)



# Helper Functions



# Thread Functions
def reader_thread():
    global buffer_lock, read_buffer
    # Get stream
    print("Connecting to MJPG stream")
    r = requests.get(STREAM_URL, stream=True, timeout=30)
    r.raise_for_status()

    # Read chunks
    jpeg_b = b""
    for chunk in r.iter_content(chunk_size=1024):
        # No more data to read, print info, loop broken early
        if not chunk:
            print("Connection closed")
            break

        # JPEG end bytes in jpeg_b, append to read_buffer
        if jpeg_b.find(b"\xff\xd9"):
            with buffer_lock:
                read_buffer.append(jpeg_b)
            jpeg_b = b""
        # No JPEG end bytes in jpeg_b, add chunk
        else:
            jpeg_b += chunk

def motion_processing_thread():
    raise NotImplementedError

def clip_processing_thread():
    raise NotImplementedError