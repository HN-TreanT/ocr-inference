
from PIL import Image
import os
from ocr_api import *

output_dir = 'cropped_images'
os.makedirs(output_dir, exist_ok=True)
def expand_boxes_to_nearest_lines(img, boxes):

    sorted_boxes = sorted(boxes, key=lambda box: box[0][1])
    texts = []
    
    for i, box in enumerate(sorted_boxes):
        print("check")
        y1 = box[0][1]
        y2 = box[1][1]
        x1 = box[0][0]
        x2 = box[1][0]
        
        print("check 1")
        print(img.shape)
        x1 = max(0, x1 - 50)
        x2 = min(img.shape[1], x2 + 50)
  
        if i > 0:
            prev_y2 = sorted_boxes[i-1][1][1]
            y1 = (prev_y2 + y1) // 2
        if i == 0:  
          y1 = max(0, y1 - 100)    
        if i < len(sorted_boxes) - 1:
            next_y1 = sorted_boxes[i+1][0][1]
            y2 = (y2 + next_y1) // 2
            
        if i == len(sorted_boxes) - 1:
            y2 = min(img.shape[0], y2 + 100) 
            
        cropped_image = img[y1:y2, x1:x2]
        cropped_image_path = os.path.join(output_dir, f'cropped_{i+1}.png')
        print(f'cropped_{i+1}.png: ', y1, y2, x1, x2)
        
        try:
            cropped_image_pil = Image.fromarray(cropped_image)
            cropped_image_pil.save(cropped_image_path)
            text = ocr_processing(cropped_image_pil)
            print(text)
            texts.append(text)   
        except Exception as e:
            print(f"Error processing box {i+1}: {e}")
            continue
            
    return texts
  