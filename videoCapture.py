import cv2
import queue
import threading


class VideoCapture(object):

    def __init__(self, video_stream):
        self.cap = cv2.VideoCapture(video_stream)
        self.q = queue.Queue()
        self.video_stream = video_stream
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.t.start()

    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()

    def isOpened(self):
        return self.cap.isOpened()

    def release(self):
        return self.cap.release()

    def restart(self):
        self.t.killed = True
        self.__init__(self.video_stream)

