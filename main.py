import flask
from flask import request
# from flask import jsonify
from heartDiseaseRecognizerinator import heartDiseaseRecognize
from heartDiseaseRecognizerinator import heartDiseaseBiggerize


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/check', methods=['GET'])
def check():
    age = request.args.get('age')
    sex = request.args.get('sex')
    cp = request.args.get('cp')
    trestbps = request.args.get('trestbps')
    chol = request.args.get('chol')
    fbs = request.args.get('fbs')
    restecg = request.args.get('restecg')
    thalach = request.args.get('thalach')
    exang = request.args.get('exang')
    oldpeak = request.args.get('oldpeak')
    slope = request.args.get('slope')
    ca = request.args.get('ca')
    thal = request.args.get('thal')

    return heartDiseaseRecognize(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope,
                                       ca, thal)


@app.route('/add', methods=['GET'])
def add():

    age = request.args.get('age')
    sex = request.args.get('sex')
    cp = request.args.get('cp')
    trestbps = request.args.get('trestbps')
    chol = request.args.get('chol')
    fbs = request.args.get('fbs')
    restecg = request.args.get('restecg')
    thalach = request.args.get('thalach')
    exang = request.args.get('exang')
    oldpeak = request.args.get('oldpeak')
    slope = request.args.get('slope')
    ca = request.args.get('ca')
    thal = request.args.get('thal')
    target = request.args.get('target')

    return heartDiseaseBiggerize(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal,
                                target)


app.run()
