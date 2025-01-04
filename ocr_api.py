import torch
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor


detector = None

def load_model(customcfg):
    global detector
    model_type = customcfg["model_type"]
    print(model_type)
    if model_type == "vggrnn":
        config = Cfg.load_config_from_file("./config/vgg-seq2seq.yml")
        config['weights'] = './weights/seq2seqocr.pth'
    else:    
        config = Cfg.load_config_from_file("./config/vgg-transformer.yml")
        config['weights'] = './weights/transformerocr.pth'
    config['device'] = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    detector = Predictor(config)


# Hàm xử lý OCR
def ocr_processing(preprocessing_img):
    s = detector.predict(preprocessing_img)
    return s
