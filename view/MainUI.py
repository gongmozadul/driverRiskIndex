#-*- coding: utf-8 -*-
import cv2
import overlay

def mainui(cap):

    # Get Webcam Properties
    width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

    # Graph and Text List
    dri = []
    text = ['pypypypypypy', 'yyyiidididididididi', 'dfkaosjlkadfj939048209384']

    # Graph x_axis
    x_axis = 100

    dr = 0

    # Show Graph At Bottom
    while(1):
        if len(dri) == x_axis:
            break
        dri.append(dr)
        dr += 1

    while(1):

        if cv2.waitKey(1) & 0xFF == ord('s'):
            overlay.driveui()
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ret, frames = cap.read()

        # Draw Background
        image = frames.copy()
        cv2.rectangle(image, (0, 0), (width, height), (255, 255, 255), -1)
        cv2.addWeighted(image, 0.7, frames, 0.3, 0, frames)

        # Draw Picture
        img = cv2.imread('main.png', -1)
        pic_height, pic_width, chn = img.shape
        pic_x = (width - pic_width)/2
        pic_y = 0
        for i in range(0, 3):
            frames[pic_y:pic_y + pic_height, pic_x:pic_x + pic_width, i] = \
                img[:, :, i] * (img[:, :, 3]/255.0) + frames[pic_y:pic_y + pic_height, pic_x:pic_x + pic_width, i] * (1.0 - img[:, :, 3]/255.0)

        # Draw Graph
        drawgraph(frames, dri, height, width, (255, 255, 255), thickness=2)

        # Draw Log
        for i in range(len(text)):
            textsize = cv2.getTextSize(text[i], cv2.FONT_HERSHEY_TRIPLEX, 0.7, 1)[0]
            text_x = (width - textsize[0]) / 2
            text_y = (height - textsize[1]) / 2 + 20
            cv2.putText(frames, text[i], (text_x, text_y + (textsize[1] * i * 2)), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 0))

        cv2.imshow('cam test', frames)

    cap.release()
    cv2.destroyAllWindows()


def drawgraph(frames, dri, height, width, color, x_gap=0.1, y_gap=0.05, thickness=1):

    # Graph Position
    x = int(round(width * x_gap))
    y = int(round(height - (height * y_gap)))

    # Graph Gap
    gap = (width - x * 2) / 100

    # Draw Standard Line
    cv2.line(frames, (x, y - 50), (x + (gap * 100), y - 50), (128, 128, 128), thickness)

    for i in range(len(dri) - 1):
        cv2.line(frames, (x + (i * gap), y - dri[i]), (x + ((i + 1) * gap), y - dri[i + 1]), color, thickness)

if __name__ == "__main__":
    mainui(cv2.VideoCapture(0))
