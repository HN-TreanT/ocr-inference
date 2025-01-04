from paddleocr import PaddleOCR
import cv2
import matplotlib.pyplot as plt
from PIL import Image

img_path = '/Volumes/data/workspace/OCR-And-Spell-Correction-master/ocr-inference/image/devan2.jpg'
img = cv2.imread(img_path)

def display_image_in_actual_size(im_data, dpi=600):
    height, width, depth = im_data.shape
    figsize = width / float(dpi), height / float(dpi)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.imshow(im_data, cmap='gray')
    plt.show()

paddle = PaddleOCR(use_angle_cls=False, lang="vi", use_gpu=True)
result = paddle.ocr(img_path, cls=False, det=True)#, rec=False)
result = result[:][:][0]

print("check result")

boxes = []
for line in result:
  line = line[0]
  boxes.append([[int(line[0][0]), int(line[0][1])], [int(line[2][0]), int(line[2][1])]])

boxes = boxes[::-1]

EXPEND = 5
for box in boxes:
  box[0][0] = box[0][0] - EXPEND
  box[0][1] = box[0][1] - EXPEND
  box[1][0] = box[1][0] + EXPEND
  box[1][1] = box[1][1] + EXPEND


texts = []
for box in boxes:
  cropped_image = img[box[0][1]:box[1][1], box[0][0]:box[1][0]]

  try:
    cropped_image = Image.fromarray(cropped_image)
  except:
    continue

  #rec_result = Paddle.ocr(cropped_image, cls=True, det=False, rec=True)
#   rec_result = detector.predict(cropped_image)

#   text = rec_result#[0]

#   texts.append(text)
#   print(text)

display_image_in_actual_size(img, 100)