import torch
import numpy as np
from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_boxes, xyxy2xywh
from utils.augmentations import letterbox
from utils.torch_utils import select_device
from utils.datasets import LoadImages
from random import randint
import cv2


class Detector(object):

    def __init__(self, device, model, conf_thres=0.25):
        self.imgsz = 640
        self.max_frame = 160
        self.conf_thres = conf_thres  # confidence threshold
        self.iou_thres = 0.45  # NMS IOU threshold
        self.init_model(device, model)

    def init_model(self, device, model):

        self.weights = 'weights/'+model+'.pt'
        self.device = select_device(device)
        model = attempt_load(self.weights, device=self.device)
        # torch.save(model, 'test.pt')
        self.model = model
        self.names = model.module.names if hasattr(
            model, 'module') else model.names
        self.colors = [
            (randint(0, 255), randint(0, 255), randint(0, 255)) for _ in self.names
        ]
        self.stride = int(model.stride.max())  # model stride

    def detect(self, imageBuffer):
        # Dataloader
        lines = []

        img0s = cv2.imdecode(np.frombuffer(
            imageBuffer, np.uint8), cv2.IMREAD_COLOR)  # BGR
        # Padded resize
        img = letterbox(img0s, self.imgsz, stride=self.stride)[0]
        # Convert
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim

        # Inference

        pred = self.model(img)[0]
        # NMS
        pred = non_max_suppression(
            pred, self.conf_thres, self.iou_thres)
        # Process predictions
        for det in pred:  # detections per image
            im0 = img0s.copy()
            # normalization gain whwh
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(
                    img.shape[2:], det[:, :4], im0.shape).round()

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    clsn = self.names[int(cls)]
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)
                                      ) / gn).view(-1).tolist()  # normalized xywh
                    # line = (clsn, cls, *xywh)  # label format
                    line = (clsn, xywh[0])
                    print(line)
                    lines.append(line)
        lines.sort(key=lambda l: l[1])
        info = []
        for line in lines:
            info.append(line[0])
        # print(info)
        return info
