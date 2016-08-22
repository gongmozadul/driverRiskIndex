# -*- coding: utf-8 -*-


def driveui():

    import cv2
    from datetime import datetime
    import serial
    import MainUI

    cap = cv2.VideoCapture(0)

    # Get Webcam Properties
    width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

    # Graph and Text List
    dri = []
    text = []

    # Graph and Text Location
    x = width - 200
    y = height - 20

    # Graph x_axis
    x_axis = 100

    # Text Log Size
    text_Size = 20

    ser = serial.Serial("COM4", 9600)

    while(1):

        if cv2.waitKey(1) & 0xFF == ord('e'):
            break

        ret, frames = cap.read()
        serialText = ser.readline()
        dr2 = serialText.split('-')

        try:
            dr = int(round(float(dr2[0])))
        except:
            continue

        # Draw Standard Line
        cv2.line(frames, (0, 410), (400, 410), (128, 128, 128), 1)

        # Show Graph At Bottom
        if len(dri) > x_axis:
            dri.pop(0)

        # Set Graph Color
        if dr < 33:
            color = (0, 0, 255)
        elif dr < 66:
            color = (0, 255, 255)
        else:
            color = (0, 255, 0)

        dri.append(y - dr)

        # Draw Line With 4 Pixel Gap
        for i in range(len(dri)-1):
            cv2.line(frames, (i * 4, dri[i]), ((i+1) * 4, dri[i+1]), color)

        # Show Data At Right Side
        if len(text) > text_Size:
            text.pop(0)
        time = datetime.now().strftime('%S.%f')[:-3]
        text.append(time + "  " + dr2[1])

        # Draw Log
        for i in range(len(text)):
            cv2.putText(frames, text[i], (x, y - (20 * i)), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255))

        cv2.imshow('cam test', frames)

    ser.close()
    return
