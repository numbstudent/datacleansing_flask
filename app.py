import re
import pandas as pd

import re

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


from flask import Flask, jsonify

app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import sqlite3


# init dataframe kamus
# df = pd.read_csv("/content/drive/MyDrive/archive/data.csv", encoding='latin-1')
df_kamus = pd.read_csv("archive/new_kamusalay.csv", encoding='latin-1')
df = df_kamus
df = df.reset_index()


# create database kamus ke sqlite, replace jika sudah ada
conn = sqlite3.connect("kamus.db")
df.to_sql("kamus", conn, if_exists='replace', index=False)
conn.close()

# create stop words
def stopwordRemove(text):
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    output = stopword.remove(text)
    return output 

def textStem(text):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    output   = stemmer.stem(text)
    return output


# berhubung looping dictionary belum bisa cepat jadi mending pakai query saja via sqlite
def checkDict(word):
    conn = None
    try:
        conn = sqlite3.connect("kamus.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute("SELECT `anak jakarta asyik asyik` FROM kamus where anakjakartaasikasik = '"+word+"' ")
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        return None


# hapus emoticon, symbols, dan ubah ke kata-kata non alay
def cleanAndReplaceText(input):
  text = input.lower()
  text = re.sub(r'http\S+', '', text) #URL removal
  text = re.sub(r"url{3}", ' ', text) # 'url' string removal
  text = re.sub(r"rt{2}", ' ', text) # retweet removal
  text = re.sub(r"user{4}", ' ', text) # USER removal
  text = re.sub(r"\\n", ' ', text) # newline removal
  text = re.sub(r"\\\w{3}", '', text) # emoticon removal
  text = re.findall(r"[\w]+",text) # symbols removal
  output = ''
  word = ''
  for val in text:
    word = val
    
    translate = checkDict(word) # replace word to non alay
    if translate:
        word = translate
    output = output +' '+ word
  return output.strip()

app.json_encoder = LazyJSONEncoder

description = '''
Dokumentasi API untuk Data Cleansing

- File hasil generate untuk text processing: archive/test_data.csv
- File original untuk generate: archive/data.csv
- File kamus untuk translate alay -> non alay: archive/new_kamusalay.csv

Terdapat 3 API Endpoint:
1. <a href="../file-generate" target="blank">File-generate</a>: membuat text file yang sesuai format untuk uji coba di file-text-processing
2. <a href="../file-text-processing" target="blank">File-text-processing</a>: melakukan cleansing terhadap text dengan inputan file berformat csv; Hasil generate dari point 1 dapat digunakan di sini
3. <a href="../text-processing" target="blank">Text-processing</a>: melakukan cleansing terhadap text dengan inputan text field
'''

swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'Gold Challenge Data Science Binar Academy '),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: description)
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
    originaltext = request.form.get('text')
    data = []
    text = originaltext
    cleanedtext = cleanAndReplaceText(text)
    cleanedtext = stopwordRemove(cleanedtext)
    cleanedtext = textStem(cleanedtext)
    val = {'original': text, 'cleaned': cleanedtext}
    data.append(val)

    json_response = {
        'status_code': 200,
        'description': "Original vs Cleaned",
        'data': data
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("file_text_processing.yml", methods=['POST'])
@app.route('/file-text-processing', methods=['POST'])
def file_text_processing():
    file = request.files['file']
    df = pd.read_csv(file, header=None)
    data = []
    for index, row in df.iterrows():
        print("processing "+str(index+1)+" of "+str(df.size))
        text = row[0]
        cleanedtext = cleanAndReplaceText(text)
        cleanedtext = stopwordRemove(cleanedtext)
        cleanedtext = textStem(cleanedtext)
        val = {'original':text, 'cleaned':cleanedtext}
        data.append(val)
    json_response = {
        'status_code': 200,
        'description': "Original vs Cleaned",
        'data': data
    }

    response_data = jsonify(json_response)
    return response_data
    
@swag_from("file_generate.yml", methods=['POST'])
@app.route('/file-generate', methods=['POST'])
def file_generate():
    amount = request.form.get('amount')
    wordincluded = request.form.get('wordincluded')

    from textgen import generate_text
    data = generate_text(amount, wordincluded)
    
    json_response = {
        'status_code': 200,
        'description': "Random text file generation. File in archive/test_data.csv",
        'data': data
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
