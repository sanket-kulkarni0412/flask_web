
from flask import Flask, redirect, render_template, request, jsonify
import os
import cv2
from detector_rev2 import detect_number
import base64
app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = '/'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        image = request.files['image']
        image.save(os.path.join(app.config["IMAGE_UPLOADS"], 'demo.jpg'))
        # img=cv2.imread('static\demo.jpg')
        #npimg = np.fromstring(img, np.uint8)
        #img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
        img, text, scores, boxes = detect_number('/demo.jpg')
        #img = Image.fromarray(img.astype("uint8"))
        #rawBytes = io.BytesIO()
        #img.save(rawBytes, "JPEG")
        # rawBytes.seek(0)heroku git:remote -a object-det-api

        #img_base64 = base64.b64encode(rawBytes.read())

        # im_arr: image in Numpy one-dim array format.
        _, im_arr = cv2.imencode('.jpg', img)
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes).decode()

        return jsonify({'status': im_b64, 'class': str(text), 'score': str(scores), 'boxes': str(boxes)})
    else:
        return 'notwroking'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5019)
