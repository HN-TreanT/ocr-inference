from PIL import Image
from ocr_api import *
from helper import *
from config.config import CONFIG
import matplotlib.pyplot as plt
import time
# load model
load_model(CONFIG)
print(CONFIG)

# def main(image_paths):
#     for image_path in image_paths:
#         img = Image.open(image_path)
#         start = time.time()
#         text = ocr_processing(img)
#         print(f"Time: {time.time() - start}: OCR:{text}")
#         # plt.imshow(img)
#         # plt.show()        

# if __name__=="__main__":
#     image_paths = get_image_list('./image')
#     main(image_paths)
      

if __name__=="__main__":
    img = Image.open("/Volumes/data/workspace/OCR-And-Spell-Correction-master/ocr-inference/image/image copy 2.png")
    width, height = img.size
   
    text = ocr_processing(img, width, height)
    start = time.time()
    print(f"Time: {time.time() - start}: OCR:{text}")
