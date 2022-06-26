import datetime
import argparse
import uuid
from datetime import timedelta
from flask import *
from processor.AIDetector_pytorch import Detector
from utils.logger import logger
from utils.logger import init as loggerInit

import core.main

UPLOAD_FOLDER = r'./uploads'

ALLOWED_EXTENSIONS = set(['png', 'jpg'])
app = Flask(__name__)
app.secret_key = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

loggerInit()

# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='./index.html'))


@app.route('/detect', methods=['GET', 'POST'])
def detect():
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)
    if file and allowed_file(file.filename):
        fileBuffer = file.read()
        if current_app.save == '1':
            with open("./picture/"+str(uuid.uuid1()) + ".png", 'wb+') as fs:
                fs.write(fileBuffer)
        image_info = core.main.c_main(fileBuffer, current_app.model)
        logger.info("{0}:{1}".format(request.remote_addr,image_info))
        return jsonify({'status': 1, 'image_info': image_info})

    return jsonify({'status': 0})


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=5003, help='port')
    parser.add_argument('--device', default='', help='device')
    parser.add_argument('--save', default='0', help='save')
    parser.add_argument('--model', default='final', help='save')
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    opt = parse_opt()
    # opt.model = 'final_2_0'
    with app.app_context():
        current_app.model = Detector(opt.device, opt.model)
        current_app.save = '0'
    app.run(host='0.0.0.0', port=opt.port)
