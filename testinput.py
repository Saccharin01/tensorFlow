import tensorflow as tf
import numpy as np
import json

# 1. 학습된 모델 불러오기
model_path = 'M5.keras'  # 모델 파일 경로를 입력하세요
model = tf.keras.models.load_model(model_path)

# 모델의 구조 확인
model.summary()

# JSON 파일 경로
json_file_path = 'athletes_data.json'  # 실제 JSON 파일 경로를 입력하세요

# JSON 파일을 읽어옵니다.
with open(json_file_path, 'r') as f:
    label_data = json.load(f)

# 클래스 이름 리스트 생성
class_names = ["species", "attack", "defense", "accuracy", "weight"]

# 2. 입력 이미지를 불러오고 전처리하기
def preprocess_image(image_path, target_size=(128, 256)):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=target_size)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

# 3. 이미지 파일 경로
image_path = './images/nariman-abbassov.png'  # 입력 이미지 파일 경로
processed_image = preprocess_image(image_path)

# 4. 모델을 통해 예측 수행
predictions = model.predict(processed_image)

# 5. 예측 결과 해석
print("Predictions:", predictions)
predicted_class = np.argmax(predictions, axis=1)
# 6. 클래스 이름을 키로, 예측 확률을 값으로 하는 딕셔너리 생성
predicted_dict = {class_names[i]: predictions[0][i] for i in range(len(class_names))}

print("Predicted class probabilities:", predicted_dict)