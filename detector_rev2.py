import re
import numpy as np
import cv2


# step 1 - load the model

net = cv2.dnn.readNet('last.onnx')

# step 2 - feed a 640x640 image to get predictions


def format_yolov5(frame):

    row, col, _ = frame.shape
    _max = max(col, row)
    result = np.zeros((_max, _max, 3), np.uint8)
    result[0:row, 0:col] = frame
    return result


def detect_number(image_path):
    image = cv2.imread(image_path)
    input_image = format_yolov5(image)  # making the image square
    blob = cv2.dnn.blobFromImage(input_image, 1/255.0, (640, 640), swapRB=True)
    net.setInput(blob)
    predictions = net.forward()

    # step 3 - unwrap the predictions to get the object detections

    class_ids = []
    confidences = []
    boxes = []

    output_data = predictions[0]

    image_width, image_height, _ = input_image.shape
    x_factor = image_width / 640
    y_factor = image_height / 640

    for r in range(25200):
        row = output_data[r]
        confidence = row[4]
        if confidence >= 0.4:

            classes_scores = row[5:]
            _, _, _, max_indx = cv2.minMaxLoc(classes_scores)
            class_id = max_indx[1]
            if (classes_scores[class_id] > .25):

                confidences.append(confidence)

                class_ids.append(class_id)

                x, y, w, h = row[0].item(), row[1].item(
                ), row[2].item(), row[3].item()
                left = int((x - 0.5 * w) * x_factor)
                top = int((y - 0.5 * h) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                boxes.append(box)

    class_list = []
    with open("classes.txt", "r") as f:
        class_list = [cname.strip() for cname in f.readlines()]

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45)
    print('index',indexes)
    result_class_ids = []
    result_confidences = []
    result_boxes = []

    for i in indexes:
        result_confidences.append(confidences[i])
        result_class_ids.append(class_ids[i])
        result_boxes.append(boxes[i])
    # print(result_confidences)
    # print(class_ids)
    # print(result_boxes)
    for i in range(len(result_class_ids)):
        bo=[]
        box = result_boxes[i]
        class_id = result_class_ids[i]

        cv2.rectangle(image, box, (0, 255, 255), 2)
        cv2.rectangle(image, (box[0], box[1]),
                      (box[0] + box[2], box[1]), (0, 255, 255), -1)
        cv2.putText(image, class_list[class_id], (box[0], box[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 220, 0))
        classd = [class_list[cl] for cl in class_ids]
        scorel = [score for score in result_confidences]
        text2 = '%s' % (classd[0])
        box_list = []
        x1 = int(box[0])
        y1 = int(box[1])
        x2 = int(box[0] + box[2])
        y2 = int(box[1] + box[3])
        box_list.append(x1)
        box_list.append(y1)
        box_list.append(x2)
        box_list.append(y2)
        bo.append(box_list)
        # print(x1, y1, x2, y2)
        cropped = image[y1:y2, x1:x2]

    # cv2.imwrite("out_detection.png",cropped)
    # cv2.imwrite("out_detection.png",image)
    # cv2.imshow('image',image)
    # plt.imshow(image)
    # plt.imshow(image)
    # plt.show()
    # cv2.waitKey(0)
    return image, text2,scorel,bo
# image,score,text,box=detect_number('D:\\Sanket Kulkarni_data\\API\\flask_web\\container_8.png')
# print('score',score)
# print('tex', text)
# print('box',box)
# cv2.imshow('image',image)
# cv2.waitKey(0)
