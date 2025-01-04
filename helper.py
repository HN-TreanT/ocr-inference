import os
import numpy as np
import json
import pathlib


IMAGE_EXT = [".jpg", ".jpeg", ".webp", ".bmp", ".png"]

# Load data folder (các ảnh linetext cần OCR và file json lưu script text tương ứng)
def load_data(data_dir):
    TRAIN_JSON = os.path.join(data_dir, "labels.json")
    with open(TRAIN_JSON, 'r', encoding='utf8') as f:
        train_labels = json.load(f)

    dict_filepath_label = {}
    raw_data_path = pathlib.Path(os.path.join(data_dir))
    for item in raw_data_path.glob('**/*.*'):
        file_name = str(os.path.basename(item))
        if file_name != "labels.json":
            label = train_labels[file_name]
            dict_filepath_label[str(item)] = label

    image_paths = list(dict_filepath_label.keys())
    return image_paths


# Load data folder (các ảnh linetext cần OCR và file txt lưu script text tương ứng)
def load_data_from_txt(data_dir, annotation_name):
    annotation_path = os.path.join(data_dir, annotation_name)
    img_paths = []
    with open(annotation_path, 'r') as ann_file:
        lines = ann_file.readlines()
        np.random.shuffle(lines)
        for l in lines:
            img_path, lex = l.strip().split('\t')
            img_path = os.path.join(data_dir, img_path)
            img_paths.append(img_path)
    return img_paths


# Tạo file output (định dạng .txt) tương ứng với model name
def create_out_file(out_folder, model_name):
    folder_name = os.path.dirname(out_folder)
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)
    # out_file = out_folder + '/' + model_name + '.txt'
    out_file = os.path.join(out_folder, model_name + '.txt')
    file_name = os.path.dirname(out_file)
    if not os.path.isdir(file_name):
        os.makedirs(file_name)
    return out_file


# Lấy list image paths từ inference data folder
def get_image_list(path):
    image_names = []
    for maindir, subdir, file_name_list in os.walk(path):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            ext = os.path.splitext(apath)[1]
            if ext in IMAGE_EXT:
                image_names.append(apath)
    return image_names