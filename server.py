# -*- coding: utf-8 -*-

import falcon
import json
import os
import datetime
from falcon_multipart.middleware import MultipartMiddleware

class RecommendForMen(object):

    def dump_response(self, cluster, skin_color, hair_color, ratio, contour,
                      colors, clothes):
        return json.dumps({'cluster': cluster,
                           'skin_color': skin_color,
                           'hair_color': hair_color,
                           'ratio': ratio,
                           'contour': contour,
                           'colors': colors,
                           'clothes': clothes})

    def on_post(self, req, res):
        print(req.files)
        image = req.get_param('image')
        print(image)
        _, ext = os.path.splitext(image.filename)
        data = image.file.read()
        with open(datetime.now().strftime('%Y%m%d%H%M%S')+'.'+ext, 'wb') as f:
            f.write(data)

        res.body = self.dump_response(0, '#ffffff', '#ffffff', 2.0, 0, {}, {})

app = falcon.API(middleware=[MultipartMiddleware()])
recomen = RecommendForMen()
app.add_route('/reco/men', recomen)

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()