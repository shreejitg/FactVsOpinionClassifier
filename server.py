# System imports
import json
from flask_httpauth import HTTPBasicAuth
from flask import Flask, Blueprint, g, session, redirect, url_for, escape, request, render_template, jsonify
from flask_cors import CORS, cross_origin

# User imports
import language_models
import neuralnet_classifier

app = Flask(__name__)
CORS(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True
auth = HTTPBasicAuth()

# USER APIs

@app.route('/')
def index():
  return jsonify({'status': 'Success', 'message': 'Hello, from the team at Fact Or Opinion.'})

@app.route('/parse_article', methods=['GET', 'POST'])
def parse_article():
  if not request.data:
    return jsonify(status="Failure", message="No json data received")

  content = json.loads(request.data)
  article_data = content.get('article_data')

  if not article_data:
    return jsonify(status="Failure", message="No data param \'Ariticle Data\' received")

  article_data_tokens = article_data.split('.')
  predictions = []
  classifier = language_models.get_classifer()
  for line in article_data_tokens:
    test_sent_features = language_models.word_feats(line.strip())
    predicted_class = classifier.classify(test_sent_features)
    predictions.append(predicted_class)
  
  # Make call to the language model
  return jsonify(status="Success", predicted_classes=predictions)

@app.route('/tf_parse_article', methods=['GET', 'POST'])
def tf_parse_article():
  print("Function tf_parse_article invoked")
  if not request.data:
    return jsonify(status="Failure", message="No json data received")

  content = json.loads(request.data)
  article_data = content.get('article_data')

  if not article_data:
    return jsonify(status="Failure", message="No data param \'Ariticle Data\' received")

  article_data_tokens = article_data.split('.')
  predictions = neuralnet_classifier.predict(article_data_tokens)
  
  # Make call to the language model
  return jsonify(status="Success", predicted_classes=predictions)

def startServer():
  app.debug=True
  app.run()

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000)
