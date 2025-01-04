from paddleocr import PaddleOCR
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import os
from config.config import CONFIG
from ocr_api import *
load_model(CONFIG)

img_path = 'test1.jpg'
img = cv2.imread(img_path)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

paddle = PaddleOCR(use_angle_cls=False, lang="vi", use_gpu=False)
result = paddle.ocr(img=img, cls=False, det=True)#, rec=False)
result = result[:][:][0]
print(result)

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

print(boxes)
output_dir = 'cropped_images'
os.makedirs(output_dir, exist_ok=True)
texts = []

previous_bottom = None 

height, width = img.shape[:2] 

def expand_boxes_to_nearest_lines(img, boxes):

    sorted_boxes = sorted(boxes, key=lambda box: box[0][1])
    texts = []
  
    for i, box in enumerate(sorted_boxes):
        y1 = box[0][1]
        y2 = box[1][1]
        x1 = box[0][0]
        x2 = box[1][0]
        
        print( y1, y2, x1, x2)
        
        x1 = max(0, x1 - 50)
        x2 = min(img.shape[1], x2 + 50)
        # Expand to previous line
        if i > 0:
            prev_y2 = sorted_boxes[i-1][1][1]
            y1 = (prev_y2 + y1) // 2
        if i == 0:  
          print("log")
          print(y1)
          y1 = max(0, y1 - 100)  
          print(y1)   
        # Expand to next line
        if i < len(sorted_boxes) - 1:
            next_y1 = sorted_boxes[i+1][0][1]
            y2 = (y2 + next_y1) // 2
        if i == len(sorted_boxes) - 1:
            print("log")
            y2 = min(img.shape[0], y2 + 100) 
            
        cropped_image = img[y1:y2, x1:x2]
        cropped_image_path = os.path.join(output_dir, f'cropped_{i+1}.png')
        print(f'cropped_{i+1}.png: ', y1, y2, x1, x2)
        
        try:
            
         
            gray_img = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
            cropped_image_pil = Image.fromarray(gray_img)
            
            cropped_image_pil.save(cropped_image_path)
            text = ocr_processing(cropped_image_pil)
            print(text)
            texts.append(text)
        except Exception as e:
            print(f"Error processing box {i+1}: {e}")
            continue
            
    return texts
  
text = expand_boxes_to_nearest_lines(img, boxes)
print(text)