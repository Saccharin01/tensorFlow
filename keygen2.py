import json

json_path = 'athletes_data.json'

# JSON 파일 읽기 및 역직렬화
with open(json_path, "r") as f:
    jsondata = json.load(f)
    
# 첫 번째 요소의 키 순서 유지
# class_list = list(jsondata[0].keys())

# "img" 키 제거
key_to_remove = "img"
class_list = [key for key in jsondata[0] if key != key_to_remove]

print(class_list)
