from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import numpy as np
from paddleocr import PaddleOCR
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import os
from config.config import CONFIG
from ocr_api import *
from paddle_service import expand_boxes_to_nearest_lines
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
load_model(CONFIG)
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.post("/ocr")
async def ocr(file: UploadFile=File(...)) :
  try:
      file_image = await file.read()
      np_img = np.frombuffer(file_image, np.uint8)
      img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
      
      # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
      # _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
      
      paddle = PaddleOCR(use_angle_cls=False, lang="vi", use_gpu=True)
      result = paddle.ocr(img=img, cls=False, det=True)
      result = result[:][:][0]
      print(result)
      boxes = []
      if result :
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
      text = expand_boxes_to_nearest_lines(img, boxes=boxes)
      return text
  except Exception as e: 
      print(f"Error: {e}")
      return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)