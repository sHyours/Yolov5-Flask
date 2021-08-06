from core import predict


def c_main(buffer, model):
    image_info = predict.predict(buffer, model)
    return image_info


if __name__ == '__main__':
    pass
