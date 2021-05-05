import time
from videoCapture import VideoCapture
from config import Config, log, cache
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np

capture_device = VideoCapture(Config.RTSP_URL)
log.info('initialized capture device in background service')


def detect_and_predict_mask(frame, faceNet, maskNet, confidence=0.5):
    # grab the dimensions of the frame and then construct a blob
    # from it
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()

    # initialize our list of faces, their corresponding locations,
    # and the list of predictions from our face mask network
    faces = []
    locs = []
    preds = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        frame_confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if frame_confidence > confidence:
            # compute the (x, y)-coordinates of the bounding box for
            # the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # ensure the bounding boxes fall within the dimensions of
            # the frame
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # extract the face ROI, convert it from BGR to RGB channel
            # ordering, resize it to 224x224, and preprocess it
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            # add the face and bounding boxes to their respective
            # lists
            faces.append(face)
            locs.append((startX, startY, endX, endY))

    # only make a predictions if at least one face was detected
    if len(faces) > 0:
        # for faster inference we'll make batch predictions on *all*
        # faces at the same time rather than one-by-one predictions
        # in the above `for` loop
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)

    # return a 2-tuple of the face locations and their corresponding
    # locations
    return (locs, preds)


def detect_no_mask():
    prototext_path = f'{Config.FACE_DETECTOR_MODEL}.prototxt'
    weights_path = f'{Config.FACE_DETECTOR_MODEL}.caffemodel'
    model_path = f'{Config.MASK_DETECTOR_MODEL}.model'
    confidence = Config.CONFIDENCE
    sample_interval = Config.SAMPLE_INTERVAL

    net = cv2.dnn.readNet(prototext_path, weights_path)
    model = load_model(model_path)
    log.info('loaded face mask detector model ...')

    # Main detector loop
    while True:
        start_time = time.time()
        faces_without_mask = 0
        faces_with_mask = 0

        if capture_device.isOpened():
            image = capture_device.read()
            (locs, preds) = detect_and_predict_mask(image, net, model)

            # loop over the detected face locations and their corresponding
            # locations
            for (box, pred) in zip(locs, preds):
                # unpack the bounding box and predictions
                (startX, startY, endX, endY) = box
                (mask, withoutMask) = pred

                # determine the class label and color we'll use to draw
                # the bounding box and text
                if mask > withoutMask:
                    label = f'Mask: {mask:.2f}'
                    faces_with_mask += 1
                    color = (0, 255, 0)
                else:
                    label = f'No Mask: {withoutMask:.2f}'
                    faces_without_mask += 1
                    color = (0, 0, 255)

                # display the label and bounding box rectangle on the output
                # frame
                cv2.putText(image, label, (startX, startY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)

        cache.set(f'{Config.CAMERA_NAME}-image', cv2.imencode('.jpg', image)[1].tobytes())
        cache.set(f'{Config.CAMERA_NAME}-mask_count', faces_with_mask)
        cache.set(f'{Config.CAMERA_NAME}-nomask_count', faces_without_mask)
        log.info(f'{Config.CAMERA_NAME} - found without mask:{faces_without_mask}, with mask:{faces_with_mask}')

        time_to_wait = sample_interval - time.time() - start_time
        if time_to_wait > 0:
            time.sleep(time_to_wait)
        else:
            time.sleep(0.5)


if __name__ == '__main__':
    detect_no_mask()
