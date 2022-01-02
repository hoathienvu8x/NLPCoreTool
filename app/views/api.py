# -*- coding: utf-8 -*-

from app import engine, DATA_FOLDER
from flask import request, jsonify
from pyvi import ViTokenizer, ViPosTagger
import unicodedata, re, os

def is_unicode(text):
    return type(text) == str

def vn_text(text):
    if not is_unicode(text):
        text = text.decode('utf-8')
    text = unicodedata.normalize('NFC', text)
    return text

def tokenize(text, raw=False):
    text = vn_text(text)
    text = text.replace("…"," ... ")
    text = text.replace("“"," \" ")
    text = text.replace("”"," \" ")
    tokens = ViTokenizer.tokenize(text)
    if raw:
        return ["%s" % token.replace('_',' ') for token in tokens.split(' ')]
    return tokens

def nlpcore_get_data(req):
    if req.content_type and "application/json" in req.content_type:
        return req.get_json()
    return req.form

@engine.route('/api/tokenize', methods=['POST'])
def nlpcore_tokenizer():
    data = nlpcore_get_data(request)
    text = data.get('text','').strip()
    if not text:
        return jsonify({
            'error':'Invalid params'
        })
    raw = data.get('raw','').strip()
    if raw:
        tokens = tokenize(text,True)
        return jsonify(tokens)
    raw = tokenize(text,False)
    raw = re.sub(r'\s+,?[\s+$]',', ',raw)
    raw = re.sub(r'\s+\.?[\s+$]','. ',raw)
    if raw[-2:] == ' .':
        raw = raw[:-2] + '.'
    if raw[-2:] == ' ,':
        raw = raw[:-2] + ','
    return jsonify([raw])

@engine.route('/api/tagger', methods=['POST'])
def nlpcore_tagger():
    data = nlpcore_get_data(request)
    text = data.get('text','').strip()
    if not text:
        return jsonify({
            'error':'Invalid params'
        })
    raw = data.get('raw','').strip()
    taggers = ViPosTagger.postagging(ViTokenizer.tokenize(text))
    if raw:
        data = []
        for i, word in enumerate(taggers[0]):
            data.append([
                word.replace('_',' '),
                taggers[1][i] if i < len(taggers[1]) else 'X'
            ])
        return jsonify(data)
    data = []
    for i, word in enumerate(taggers[0]):
        data.append('%s/%s' % (word.replace('_',' '), taggers[1][i] if i < len(taggers[1]) else 'X'))
    return jsonify(" ".join(data))

@engine.route('/api/ner', methods=['POST'])
def nlpcore_ner():
    return jsonify([])

@engine.route("/api/train", methods=['POST'])
def nlpcore_train():
    data = nlpcore_get_data(request)
    text = data.get('text','').strip()
    if not text:
        return jsonify({
            'error':'Invalid params'
        })
    try:
        with open(os.path.join(DATA_FOLDER, 'train.txt'),'a') as f:
            f.write(text + "\n")
    except Exception as e:
        return jsonify({
            'error':str(e)
        })
    return jsonify({
        'status':'ok'
    })
