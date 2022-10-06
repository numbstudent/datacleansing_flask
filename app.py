import re
import pandas as pd

import re

from flask import Flask, jsonify

app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import pandas as pd
import numpy as np

# init dataframe kamus
# df = pd.read_csv("/content/drive/MyDrive/archive/data.csv", encoding='latin-1')
df_kamus = pd.read_csv("archive/new_kamusalay.csv", encoding='latin-1')
df = df_kamus
df = df.reset_index()

def cleanAndReplaceText(input):
  text = input.lower()
  text = re.sub(r"\\n", ' ', text)
  text = re.sub(r"\\\w{3}", '', text)
  text = re.findall(r"[\w]+",text)
  output = ''
  word = ''
  for val in text:
    word = val
    for index, row in df.iterrows():
      if val == row[1]:
        word = row[2]
    output = output +' '+ word
  return output.strip()

def cleanText(input):
  text = input
  text = re.sub(r"\\n", ' ', text)
  text = re.sub(r"\\\w{3}", '', text)
  text = re.findall(r"[\w]+",text)
  output = ' '.join(text)
  return output

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
        'description': "Cleaned Teks",
        'data': [{
            'output1': cleanText(text),
            'output2': cleanAndReplaceText(text) 
        }]
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("file_text_processing.yml", methods=['POST'])
@app.route('/file-text-processing', methods=['POST'])
def file_text_processing():
    file = request.files['text']
    df = pd.read_csv(file, header=None)
    output1 = []
    output2 = []
    for index, row in df.iterrows():
        print("processing "+str(index+1)" of "+str(df.size))
        output1.append(cleanText(row[0]))
        output2.append(cleanAndReplaceText(row[0]))
    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        'data': [{
            'output1': output1,
            'output2': output2 
        }]
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
