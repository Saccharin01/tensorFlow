import json
import numpy as np
import tensorflow as tf
from sklearn.model_selection import KFold
from modules.visulaize_history import plot_history

model = tf.keras.models
layers = tf.keras.layers

# JSON 파일 읽기
with open('athletes_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 이미지와 레이블 준비
images = []
labels = []

img_process = tf.keras.preprocessing.image
for entry in data:
    img_path = entry['img']
    img = img_process.load_img(img_path, target_size=(64, 128))  # 이미지 크기 조정
    img_array = img_process.img_to_array(img) / 255.0  # 정규화
    images.append(img_array)
    
    # 레이블: 공격력, 방어력, 정확도
    labels.append([
        float(entry['attack']),
        float(entry['defense']),
        float(entry['accuracy'].replace('%', '').strip()),
        # float(entry['weight'])  # 필요한 경우 추가
    ])

# NumPy 배열로 변환
X = np.array(images)
y = np.array(labels)

# X를 리스트로 변환하여 JSON으로 저장
X_list = X.tolist()  # NumPy 배열을 리스트로 변환

with open("test.json", 'w', encoding='utf-8') as json_file:
    json.dump(X_list, json_file, ensure_ascii=False, indent=4)
print("Images and labels have been saved to test.json and labels.json.")
