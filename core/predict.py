import cv2

def predict(buffer, model):
    image_info = model.detect(buffer)
    return image_info
