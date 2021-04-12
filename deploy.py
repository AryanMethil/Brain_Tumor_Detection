import cv2
import numpy as np
import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator
import keras
from tensorflow.keras.models import load_model
import streamlit as st
from PIL import Image

tf.keras.backend.clear_session()


model =load_model(r"C:\Users\ASUS\PycharmProjects\College\DS2_ResNet_3_Tensorflow_2point2_Histo_Erode_Dilate.h5",compile=False)


def predict_func(img):
    print(img.shape)
    IMG_SIZE = 150
    img_path = r"C:\Users\ASUS\PycharmProjects\College\Test\yes\yes1.jpeg"
    kernel = np.ones((4,4), np.uint8)

    norm = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th1 = cv2.equalizeHist(norm)
    eroded = cv2.erode(th1, kernel)
    dilate = cv2.dilate(eroded, kernel)
    cv2.imwrite(img_path, dilate)

    VAL_DIR = r"C:\\Users\\ASUS\\PycharmProjects\\College\\Test\\"
    val_datagen = ImageDataGenerator(rescale=1 / 255)
    val_generator = val_datagen.flow_from_directory(VAL_DIR, target_size=(IMG_SIZE, IMG_SIZE), class_mode='binary',
                                                    shuffle=False)

    Y_pred = model.predict_classes(val_generator)
    per_list = model.predict(val_generator)

    for i in per_list:
        percentage = i

    for i in Y_pred:
        if i == 1:
            image = cv2.putText(img, 'Tumor', (30, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (255, 0, 0), 2, cv2.LINE_AA)
        else:
            image = cv2.putText(img, 'Normal', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (255, 0, 0), 2, cv2.LINE_AA)

    return image, percentage

def main():
    """Brain Tumor Detection App"""

    html_temp = r'''
        <body style="background-color:red;">
        <div style="background-color:red ;padding:10px">
        <h2 style="color:white;text-align:center;">Brain Tumor Detection WebApp</h2>
        </div>
        </body>
    '''
    st.markdown(html_temp, unsafe_allow_html=True)

    image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    if image_file is not None:
        print(image_file)
        image = Image.open(image_file)
        st.text("Original Image")
        st.image(image)

    if st.button("Recognise"):
        image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        result_img , percent = predict_func(image)
        st.image(result_img)
        st.text(percent)


if __name__ == '__main__':
    main()