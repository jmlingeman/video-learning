import cv2
import cv2.cv as cv
import os

class Video:
    def __init__(self, filename):
        self.filename = filename
        self.video = cv2.VideoCapture(filename)
        self.frames = []
        self.timestamps = []

    def dump_video_to_frames(self):
        print self.video.isOpened()
        dirname = "".join(filename.split(".")[0:-1])
        os.mkdir(dirname)
        sift = cv2.SIFT()
        while(self.video.isOpened()):
            ret, frame = self.video.read()
            time = self.video.get(cv.CV_CAP_PROP_POS_MSEC)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # cv2.imshow('frame',gray)
            self.frames.append(gray)
            self.timestamps.append(time)
            kp = sift.detect(gray, None)

            img = cv2.drawKeypoints(gray, kp)
            cv2.imwrite(dirname + "/" + time + ".png", img)

            print time
            # if cv2.waitKey(1) & 0xFF == ord('q'):
                # break
        self.video.release()

    def process_frames(frames):
        pass

    def extract_frame(timestamp):
        pass

v = Video("resources/counting2.mp4")
v.dump_video_to_frames()
print len(v.frames)
