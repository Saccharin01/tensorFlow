import tensorflow as tf
import numpy as np
image = tf.keras.preprocessing.image
# 1. 학습된 모델 불러오기 (모델 파일 경로를 지정합니다.)
model_path = 'model.keras'  # 모델 파일 경로를 입력하세요
model = tf.keras.models.load_model(model_path)

# 2. 입력 이미지를 불러오고 전처리하기
def preprocess_image(image_path, target_size=(128, 256)):
    img = image.load_img(image_path, target_size=target_size)
    img_array = image.img_to_array(img)  # 이미지를 numpy 배열로 변환
    img_array = np.expand_dims(img_array, axis=0)  # 배치 차원을 추가하여 (1, height, width, channels) 형태로 만듭니다.
    img_array = img_array / 255.0  # 이미지 정규화
    return img_array

# 3. 이미지 파일 경로
image_path = './images/aalon-cruz.png'  # 입력 이미지 파일 경로를 입력하세요
processed_image = preprocess_image(image_path)

# 4. 모델을 통해 예측 수행
predictions = model.predict(processed_image)

resultObj = {
  "attack": predictions[0][0],
  "defense" : predictions[0][1],
  "accuarcy" : predictions[0][2]
}


# 5. 예측 결과 출력
print("예측 결과:", resultObj["attack"])
