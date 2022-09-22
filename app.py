import re
import pandas as pd

import re

from flask import Flask, jsonify

app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'Gold Challenge Data Science Binar Academy '),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk Data Cleansing')
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,config=swagger_config)

@swag_from("text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    text = request.form.get('text')

    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', text)
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("file_text_processing.yml", methods=['POST'])
@app.route('/file-text-processing', methods=['POST'])
def file_text_processing():

    text = request.form.get('text')

    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', text)
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    app.run()