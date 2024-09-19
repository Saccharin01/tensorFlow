import json
import os
import numpy as np
import tensorflow as tf
from visualize import plot_history

img_process = tf.keras.preprocessing.image
model = tf.keras.models
layers = tf.keras.layers


# JSON 파일 읽기
with open('athletes_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 이미지와 레이블 준비
images = []
labels = []

for entry in data:
    img_path = entry['img']
    # 이미지 로드 및 전처리
    img = img_process.load_img(img_path, target_size=(128, 128))  # 이미지 크기 조정
    img_array = img_process.img_to_array(img) / 255.0  # 정규화
    images.append(img_array)

    # 레이블: 공격력, 방어력, 정확도
    labels.append([float(entry['attack']), float(entry['defense']), float(entry['accuracy'].replace('%', '').strip())])

# NumPy 배열로 변환
X = np.array(images)
y = np.array(labels)


define_model = model.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(3)  # 공격력, 방어력, 정확도
])

define_model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
# 모델 학습
learn_log = define_model.fit(X, y, epochs=50, batch_size=16, validation_split=0.2)


plot_history(learn_log)