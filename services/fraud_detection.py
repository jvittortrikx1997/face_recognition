import os
import face_recognition

from .image_service import load_and_encode_image

def compare_images(solicitante_image, blacklist_images, base_dir):
    solicitante_encoding = load_and_encode_image(solicitante_image)

    if solicitante_encoding is None or len(solicitante_encoding) == 0:
        return None, None

    for pesid, fraud_image_name in blacklist_images:
        fraud_image_path = os.path.join(base_dir, fraud_image_name)
        fraud_encoding = load_and_encode_image(fraud_image_path)

        if fraud_encoding is not None and len(fraud_encoding) > 0 and any(face_recognition.compare_faces([fraud_encoding], solicitante_encoding)):
            return pesid, fraud_image_path

    return None, None
