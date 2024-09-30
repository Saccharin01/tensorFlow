import json
import tensorflow as tf

# 이미지 경로
imglocation = "./images/hamdy-abdelwahab.png"

# 이미지 전처리 과정
images_preprocessed = []

img_process = tf.keras.preprocessing.image

# 이미지 로드 및 크기 조정
img = img_process.load_img(imglocation, target_size=(128, 256))  # 이미지 크기 조정
img_array = img_process.img_to_array(img) / 255.0  # 정규화

# 이미지 배열을 리스트로 변환 후 저장
images_preprocessed.append(img_array.tolist())

# 전처리된 데이터를 JSON 형식으로 저장
with open('image.data.preprocess.json', 'w', encoding='utf-8') as outfile:
    json.dump(images_preprocessed, outfile, ensure_ascii=False, indent=4)

print("Preprocessed image data has been saved as 'image.data.preprocess.json'.")
