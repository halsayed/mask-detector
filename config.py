import os
import logging
from redis import Redis


class Config:
    APP_NAME = os.environ.get('APP_NAME', 'Face Mask Detector')
    SHORT_NAME = os.environ.get('SHORT_NAME', 'FMD')
    LOCATION = os.environ.get('LOCATION', 'Mask Detector')
    VERSION = 'v1.7'
    REFRESH_INTERVAL = int(os.environ.get('REFRESH_INTERVAL', 1000))    # msec for page refresh

    MASK_DETECTOR_MODEL = os.environ.get('MASK_DETECTOR_MODEL', 'model/mask_detector')
    FACE_DETECTOR_MODEL = os.environ.get('FACE_DETECTOR_MODEL', 'model/face_detector')
    CONFIDENCE = float(os.environ.get('CONFIDENCE', 0.5))
    SAMPLE_INTERVAL = int(os.environ.get('SAMPLE_INTERVAL', 1))

    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))

    RTSP_URL = os.environ.get('RTSP_URL', 'rtsp://localhost:8554/Stream')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.INFO)


# create logger
log = logging.getLogger()
log.setLevel(Config.LOG_LEVEL)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(Config.LOG_LEVEL)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
log.addHandler(ch)


# redis cache
cache = Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB)


