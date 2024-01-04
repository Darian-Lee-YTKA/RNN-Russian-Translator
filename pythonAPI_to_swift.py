
from flask import Flask, request, jsonify
import json
import re
import spacy
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import numpy as np
from keras.models import load_model

with open('/Users/darianlee/Downloads/rus_tokenizer (1).json', 'r') as file:
    rus_tokenizer = tokenizer_from_json(file.read())

with open('/Users/darianlee/Downloads/eng_tokenizer (1).json', 'r') as file:
    eng_tokenizer = tokenizer_from_json(file.read())


model = load_model('/Users/darianlee/Downloads/best_model_unit_400.h5')

app = Flask(__name__)






@app.route('/SimpleTranslate', methods=['POST'])
def translate():
    data = request.get_json()

    if 'text' not in data:
        return jsonify({'error': 'Missing "text" parameter'}), 400

    text = data['text']
    result = run_translate(text)
    return jsonify({'translation': result})

def preprocess(input):
    input = re.sub(r'л(?=\s|$)', 'л p', input)
    input = re.sub(r'ла(?=\s|$)', 'ла p', input)
    input = re.sub(r'лся(?=\s|$)', 'лся p', input)
    input = re.sub(r'ло(?=\s|$)', 'ло p', input)
    input = re.sub(r'лось(?=\s|$)', 'лось p', input)
    input = re.sub(r'ли(?=\s|$)', 'ли p', input)
    input = re.sub(r'лись(?=\s|$)', 'лись p', input)
    input = re.sub(r'\s+$', '', input, flags=re.MULTILINE)
    russian_lemmas = []
    nlp = spacy.load("ru_core_news_sm")
    doc = nlp(input)
    lemmas = [token.lemma_ if token.text != 'p' else 'p' for token in doc]  # so that the past tense remains tagged
    russian_lemmas.append(lemmas)
    return russian_lemmas


def get_predictions(input):
    lemmas = preprocess(input)
    input_tokens = rus_tokenizer.texts_to_sequences(lemmas)
    while len(input_tokens[0]) < 10:
        input_tokens[0].append(0)
    if len(input_tokens) > 10:
        input_tokens = input_tokens[:9] #only evaluate the first 10 tokens to avoid crash
    trans = model.predict(input_tokens)
    return trans


index_to_word = {index: word for word, index in eng_tokenizer.word_index.items()}


def get_translations(input):
    input = input.lower()
    sentence = get_predictions(input)[0]
    output = ''
    for word in sentence:
        token = np.argmax(word)
        if token == 0:
            continue
        else:
            eng_word = index_to_word[token]
            if eng_word == 'ca':  # in the preprocessing process I accidently replaced can't with ca not
                eng_word = 'can'
            if eng_word == 'wo':  # in the preprocessing process I accidently replaced won't with wo not
                eng_word = 'will'
            if eng_word == 'i':  # fix capitalization of i
                eng_word = 'I'
        output += eng_word + ' '
    return (output)



def run_translate(input_text):
    lemmas = preprocess(input_text)
    input_tokens = rus_tokenizer.texts_to_sequences(lemmas)

    while len(input_tokens[0]) < 10:
        input_tokens[0].append(0)
    translation = get_translations(input_text)

    return translation



if __name__ == '__main__':
    app.run(debug=True)
