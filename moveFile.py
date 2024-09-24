import os
import json
import shutil

image_dir = 'images'
image2_dir = 'image2'

if not os.path.exists(image2_dir):
    os.makedirs(image2_dir)

image_files = os.listdir(image_dir)
with open("athletes_data.json", "r", encoding='utf-8') as data:
    condition = json.load(data)  # JSON 데이터 로드
    # print(condition)
    
    img_list = []
    for element in condition:
        img_path = element["img"]
        img_name = img_path.replace("images\\", "")
        img_list.append(img_name)

# 4. 이미지 파일을 대조하여 일치하는 항목을 image2로 이동
print(img_list)
for img_file in image_files:
    # print(img_file)
    if img_file in img_list:
        shutil.move(os.path.join(image_dir, img_file), os.path.join(image2_dir, img_file))
        print(f"Moved: {img_file} to {image2_dir}")

print("파일 이동 완료.")
