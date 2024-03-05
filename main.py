import os
import numpy as np
import face_recognition
from PIL import Image, ImageDraw


def list_image_files(directory):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']  # Ma'lumot uchun rasmlarning keng shaklga ega bo'lgan kengaytmalari
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(root, file))
    return image_files


know_face_encodings = []
for image in list_image_files(r'photos\xijinpin'):
    print(image)
    know_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(image))[0])

unknown_image = face_recognition.load_image_file('photos/allp.jpg')


row = 0
for unknown_encoding in face_recognition.face_encodings(unknown_image):
    results = face_recognition.face_distance(know_face_encodings,
                                             unknown_encoding)

    similarity_percentage = (1 - results[0]) * 100
    # numpy_array = np.array(similarity_percentage)
    # print(np.max(numpy_array))

    if similarity_percentage >= 65:
        pil_image = Image.fromarray(unknown_image)
        draw = ImageDraw.Draw(pil_image)
        loc = face_recognition.face_locations(unknown_image)[row]
        top, right, bottom, left = loc
        face_image = unknown_image[top-50:bottom+25, left-15:right+25]
        pil_image = Image.fromarray(face_image)
        pil_image.save(os.path.join(f"face{row}.jpg"))

    row += 1
