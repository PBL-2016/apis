# -*- coding: utf-8 -*-

from flask import (Flask, request, render_template)
from flask_uploads import (UploadSet, configure_uploads, IMAGES, UploadNotAllowed)
from predict import (prediction_init, analysis, P_SUCCESS, P_NOTFOUND, P_UNDETECTED)
from cluster import get_cluster_images
import json
import os
import datetime

app = Flask(__name__)

uploaded_images = UploadSet('images', default_dest=lambda app: app.instance_path)
configure_uploads(app, uploaded_images)

def dump_response(cluster, sample_images, skin_color, hair_color, ratio,
                  contour, colors, clothes):
    return json.dumps({'cluster': cluster,
                       'sample_images': sample_images,
                       'skin_color': skin_color,
                       'hair_color': hair_color,
                       'ratio': ratio,
                       'contour': contour,
                       'colors': colors,
                       'clothes': clothes})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/reco/men', methods=['POST'])
def reco_men():
    if request.method == 'POST':
        image = request.files.get('camera');
        if not image:
            return "Please upload image"
        else:
            try:
                filename = uploaded_images.save(image)
                filename = app.instance_path + '/' + filename
            except UploadNotAllowed:
                return "Upload was not allowed"
            else:
                result, code = analysis(filename)
                if code == P_SUCCESS:
                    hair_color = '#%02X%02X%02X' % (result['hairR'],
                                                    result['hairG'],
                                                    result['hairB'])
                    skin_color = '#%02X%02X%02X' % (result['skinR'],
                                                    result['skinG'],
                                                    result['skinB'])
                    sample_images = get_cluster_images(result['cluster'])
                    tmp = {}
                    tmp['sample_images'] = sample_images
                    tmp['skin_color'] = skin_color
                    tmp['hair_color'] = hair_color
                    tmp['ratio'] = float(result['ratio'])
                    tmp['contour'] = int(result['contour'])
                    return render_template('result.html', res=tmp)
#                    return dump_response(int(result['cluster']),
#                                         sample_images,
#                                         skin_color, hair_color,
#                                         float(result['ratio']),
#                                         int(result['contour']),
#                                         {}, {})
                elif code == P_NOTFOUND:
#                    return json.dumps({'error': 'File not found'})
                    return render_template('error.html', error="File not found")
                elif code == P_UNDETECTED:
#                    result['error'] = 'Undetected'
#                    return json.dumps(result)
                    return render_template('error.html', error="Undetected your face or bust")
    return "Unexpected"

if __name__ == '__main__':
    prediction_init()
    app.run(debug=True)
