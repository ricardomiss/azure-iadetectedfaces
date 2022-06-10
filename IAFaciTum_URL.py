# lIBRERIAS DE PYTHON
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from PIL import ImageFont
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person


#PUNTOS DE CONEXION Y CONTRASEÑA (EDITAR SI NO DA CONEXION JSJSJ)
KEY = "83c6c014b5444f7b98fdef0bcf85a01a"
ENDPOINT = "https://iade.cognitiveservices.azure.com/"

#Autenticar al cliente 
#Esta clase representa la autorización para usar el servicio Face, se necesita para que Face funcione correctamente.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


#VISUALIZACION DE CARAS Y ANALISIS DE CARAS
# Detect a face in an image that contains a single face
single_face_image_url = input("Ingresa una URL de una IMAGEN: \n")
single_image_name = os.path.basename(single_face_image_url)
#attributes = ['age','gender']
detected_faces = face_client.face.detect_with_url(url=single_face_image_url, detection_model='detection_01', recognition_model='recognition_04', return_face_attributes = ['age','gender','emotion'], include_id = True, face_landmarks = True)
#detected_faces = face_client.face.detect_with_url(url=single_face_image_url, detection_model='detection_03', attributes = ["age","gender"], include_id = True, include_landmarks = True)
if not detected_faces:
    raise Exception('Ninguna cara se detecto {}'.format(single_image_name))

# Display the detected face ID in the first single-face image.
print('Detected face ID from', single_image_name, '')
for face in detected_faces: print (face.face_id)
print()
for face in detected_faces:
    age = face.face_attributes.age
    gender = face.face_attributes.gender
    emotion = face.face_attributes.emotion


    print("La edad es: ", str(int(age)))
    if gender == "female":
        print("El genero es: Mujer\n")
    else:
        print("El genero es: Hombre\n")
    emotion_procesado = [(emotion.neutral*100),(emotion.happiness*100),(emotion.anger*100),(emotion.sadness*100),(emotion.contempt*100),(emotion.disgust*100),(emotion.fear*100),(emotion.surprise*100)]
    print("Neutral",emotion_procesado[0],"%")
    print("Felicidad",emotion_procesado[1],"%")
    print("Enojo",emotion_procesado[2],"%")
    print("Tristeza",emotion_procesado[3],"%")
    print("Odio",emotion_procesado[4],"%")
    print("disgusto",emotion_procesado[5],"%")
    print("Miedo",emotion_procesado[6],"%")
    print("Sorprendido",emotion_procesado[7],"%")
print()
# Save this ID for use in Find Similar
first_image_face_ID = detected_faces[0].face_id


#Funcion que encierra las caras en un rectangulo
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    
    return ((left, top), (right, bottom))

#DESCARGAR Y MOSTRAR LA IMAGEN DONDE DETECTA LA CARA
def drawFaceRectangles():
#Descarga la imagen desde la URL (de manera temporal)
    response = requests.get(single_face_image_url)
    img = Image.open(BytesIO(response.content))
    print('Generando imagen, espere un momento')
#Por cada cara detectada devuelve un cuadrado rojo
    draw = ImageDraw.Draw(img)
    for face in detected_faces:
        draw.rectangle(getRectangle(face), outline='red')
#Display the image in the default image browser.
    img.show()

drawFaceRectangles()
input()