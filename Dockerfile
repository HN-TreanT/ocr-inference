FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install gdown
RUN pip install einops
RUN pip install matplotlib

