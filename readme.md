<p align="center">
  <img src="../docs/vinorsoft_logo.png" width="150">
  <br />
  <br />
  <a href="http://www.vinorsoft.com/"><img alt="Auth Vinorsoft" src="https://img.shields.io/badge/Auth-Vinorsoft-FFD500?style=flat&labelColor=005BBB" /></a>
  <a href="https://github.com/pytorch/fairseq/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
  <a href="https://github.com/optimuskonboi"><img alt="Instructor DanPV" src="https://img.shields.io/badge/Instructor-DanPV-FFD500?style=flat&labelColor=005BBB" /></a>
  <a href="https://github.com/giangnv125"><img alt="Deployer GiangNV" src="https://img.shields.io/badge/Deployer-GiangNV-FFD500?style=flat&labelColor=005BBB" /></a>
</p>

--------------------------------------------------------------------------------
## Vinorsoft Vietnamese Handwritten Recognition
### Overview
- This Vietnamese OCR inference based on this link https://github.com/pbcquoc/vietocr/tree/master

### Our dataset
- Link: https://drive.google.com/drive/folders/199bK9vfX89s1muT2mWSNULuh9Y_xaIj5?usp=drive_link


### Pretrained models on our custom dataset
Download below pretrained models and place into `weights` folder:

| Model           | Link                                                                                                                                |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------|
| vgg_transformer | Link: https://drive.google.com/file/d/1vYJsuJq2d2Mk3FNO26l0_lrJlS0E8JDq/view?usp=drive_link                                           |
|vgg_seq2seq      | Link: https://drive.google.com/file/d/1RQ7uarWBNe9ntL1YFx0Cts0gOohq5nmv/view?usp=drive_link                                                        |
### Installation docker
- Moving to Dockerfile directory and build Docker image
```shell
docker build -t <<image-name>> .
```
- Run Docker Container on GPU
```shell
xhost +
docker run --network=host --gpus all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -it -v <<source-directory>>:/home -w /home --name cmraiocr <<image-name>>
```
### Run
- Place inference data to `./demo`
- Choose model inference (vgg_seq2seq or vgg_transformer): `model_type` parameter  in `config/config.py` file
```
    "model_type": "vggrnn",
    # "model_type": "transformer",
```
- Run file `python3 main.py` on docker container
```
    Input: images folder
    Output: list text OCR from images
```

