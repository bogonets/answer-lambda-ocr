import easyocr

# pip install easyocr


def init_recognizer(lang_list):
    return easyocr.Reader(lang_list)


def recognize(reader, image):
    return reader.readtext(image)


def draw_text(image, text_info):
    img = image.clone()
    image_h, image_w, _ = img.shape
    for item in text_info:
        bbox = item[0]
        c1 = (int(bbox[0][0]), int(bbox[0][1]))
        c2 = (int(bbox[2][0]), int(bbox[2][1]))
        bbox_color = (0, 255, 0)
        fontScale = 0.5
        bbox_thick = int(0.6 * (image_h + image_w) / 600)
        bbox_mess = '%s: %.2f' % (item[1], item[2] * 100)

        cv2.rectangle(img, c1, c2, bbox_color, bbox_thick)

        t_size = cv2.getTextSize(bbox_mess, 0, fontScale, thickness=bbox_thick // 2)[0]
        c3 = (c1[0] + t_size[0], c1[1] - t_size[1] - 3)
        cv2.rectangle(img, c1, (np.float32(c3[0]), np.float32(c3[1])), bbox_color, -1) #filled

        cv2.putText(img, bbox_mess, (c1[0], np.float32(c1[1] - 2)), cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale, (0, 0, 0), bbox_thick // 2, lineType=cv2.LINE_AA)

    return img

