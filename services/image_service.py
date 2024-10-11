import face_recognition
import os

from rich import print_json


def get_solicitantes_images(directory):
    images = []
    for file in os.listdir(directory):
        if file.endswith(('jpg', 'jpeg', 'png')):
            images.append(os.path.join(directory, file))
    return images

def load_and_encode_image(image_path):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    return encodings[0] if encodings else None