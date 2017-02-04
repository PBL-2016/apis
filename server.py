# -*- coding: utf-8 -*-

from flask import (Flask, request)
from flask_uploads import (UploadSet, configure_uploads, IMAGES, UploadNotAllowed)
import json
import os
import datetime

app = Flask(__name__)

uploaded_images = UploadSet('images', default_dest=lambda app: app.instance_path)
configure_uploads(app, uploaded_images)

def dump_response(cluster, skin_color, hair_color, ratio, contour,
                  colors, clothes):
    return json.dumps({'cluster': cluster,
                       'skin_color': skin_color,
                       'hair_color': hair_color,
                       'ratio': ratio,
                       'contour': contour,
                       'colors': colors,
                       'clothes': clothes})

@app.route('/reco/men', methods=['POST'])
def reco_men():
    if request.method == 'POST':
        image = request.files.get('image');
        if not image:
            return "Please upload image"
        else:
            try:
                filename = uploaded_images.save(image)
            except UploadNotAllowed:
                return "Upload was not allowed"
            else:
                print(filename)
                return dump_response(0, '#ffffff', '#ffffff', 2.0, 0, {}, {})
    return "Hoge"

if __name__ == '__main__':
    app.run(debug=True)