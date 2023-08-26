import json
import boto3
from flask import Flask, request, jsonify

app = Flask(__name__)
session = boto3.Session(profile_name='default')
client = session.client('rekognition')


def prepare_image(file):
    file_bytes = file.read()
    return file_bytes
    

@app.route('/rekog', methods=['POST'])
def rekognition():
    try:
        file = request.files['file']
        
        file_bytes = prepare_image(file)
        
        response = client.detect_faces(Image={'Bytes': file_bytes}, Attributes=['ALL'])
        for faceDetail in response['FaceDetails']:
          
          print('The detected face is between ' + str(faceDetail['AgeRange']['Low']) + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
          print("Gender: " + str(faceDetail['Gender']))
          print("Smile: " + str(faceDetail['Smile']))
          print("Eyeglasses: " + str(faceDetail['Eyeglasses']))
          print("Emotions: " + str(faceDetail['Emotions'][0]))

          print('Here are the other attributes:')
          print(json.dumps(faceDetail, indent=4, sort_keys=True))
          
        return jsonify(faceDetail)
    except Exception as e:
        return str(e)
  