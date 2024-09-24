import json

test = []

# JSON 파일 열기
with open("athletes_data.json", "r", encoding='utf-8') as data:
    condition = json.load(data)  # JSON 데이터 로드
    for element in condition:  # condition에서 반복
        if "images\\" not in element["img"]:  # 조건 확인
            result = {**element,"img": f'images\\{element["img"]}'}  # 새로운 딕셔너리 생성
            test.append(result)
        else :
          test.append(element)

# 결과를 JSON 파일로 저장
with open("test.json", "w", encoding='utf-8') as output_file:
    json.dump(test, output_file, ensure_ascii=False, indent=4)
