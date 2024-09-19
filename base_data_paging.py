import os
import requests
from bs4 import BeautifulSoup
import json
import time  # 시간 관련 모듈 추가

# 1. 메인 페이지 URL 설정
base_url = 'https://kr.ufc.com'
athletes_list_url = f'{base_url}/athletes/all'

# 2. 저장할 디렉토리 설정
images_dir = 'images'
athlete_data = []

# 3. 디렉토리가 존재하지 않으면 생성
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# 4. 페이지 순회
page_number = 41
pagination_step = 1  # 페이지네이션 단위 설정

while True:
    # 페이지 URL 설정
    current_page_url = f'{athletes_list_url}?page={page_number}'
    
    # 5. 메인 페이지에서 데이터 크롤링
    try:
        response = requests.get(current_page_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"페이지 요청 실패: {current_page_url}\n{e}")
        break

    soup = BeautifulSoup(response.text, 'html.parser')

    # 6. 검색 결과가 없으면 종료
    if soup.find('div', class_='view-empty'):
        print("더 이상 결과가 없습니다. 종료합니다.")
        break

    # 7. 'c-listing-athlete-flipcard__back' 클래스를 가진 div 요소 찾기
    athlete_cards = soup.find_all('div', class_='c-listing-athlete-flipcard__back')

    # 8. 각 선수의 이름과 이미지 추출 및 저장
    for card in athlete_cards:
        # 8.1. 선수 이름 추출
        name_tag = card.find('span', class_='c-listing-athlete__name')
        if name_tag:
            name = name_tag.get_text().strip().lower().replace(' ', '-')
            kebab_case_name = name

            # 8.2. 선수 이미지 추출 및 저장
            img_tag = card.find('img')
            img_path = None  # 기본값 설정
            if img_tag and "standing" in img_tag.get('src', ''):
                img_url = requests.compat.urljoin(base_url, img_tag['src'])

                try:
                    img_response = requests.get(img_url)
                    img_response.raise_for_status()

                    img_name = f"{kebab_case_name}.png"
                    img_path = os.path.join(images_dir, img_name)

                    with open(img_path, 'wb') as f:
                        f.write(img_response.content)

                    print(f"이미지 저장됨: {img_path}")
                except requests.exceptions.RequestException as e:
                    print(f"이미지 다운로드 실패: {img_url}\n{e}")

            # 8.3. 선수 상세 페이지 URL 생성 및 데이터 저장
            athlete_url = f'{base_url}/athlete/{kebab_case_name}'
            try:
                athlete_response = requests.get(athlete_url)
                athlete_response.raise_for_status()

                athlete_soup = BeautifulSoup(athlete_response.text, 'html.parser')
                attack = athlete_soup.select_one('div.c-stat-compare__group.c-stat-compare__group-1 .c-stat-compare__number')
                defense = athlete_soup.select_one('div.c-stat-compare__group.c-stat-compare__group-2 .c-stat-compare__number')
                accuracy = athlete_soup.select_one('.e-chart-circle__percent')

                attack_value = attack.get_text(strip=True) if attack else ""
                defense_value = defense.get_text(strip=True) if defense else ""
                accuracy_value = accuracy.get_text(strip=True) if accuracy else ""

                # 선수 데이터 딕셔너리 생성
                if img_path:  # 이미지가 성공적으로 다운로드되었는지 확인
                    athlete_dict = {
                        "img": img_path,
                        "attack": attack_value,
                        "defense": defense_value,
                        "accuracy": accuracy_value
                    }
                    athlete_data.append(athlete_dict)

            except requests.exceptions.RequestException as e:
                print(f"선수 페이지 요청 중 오류 발생: {athlete_url}\n{e}")

    # 페이지 번호 증가
    page_number += pagination_step  # 페이지 번호 증가 단위 설정

    # 메모리 관리: 사용하지 않는 변수 삭제
    del soup, athlete_cards  # 더 이상 필요 없는 객체 삭제

    # 요청 간 간격 설정 (예: 1초 대기)
    time.sleep(1)

    # 9. 최대 페이지 수 조건 추가
    if page_number >= 300:
        print("최대 페이지 수에 도달했습니다. 종료합니다.")
        break

# 10. 기존 JSON 파일 읽기
json_file_path = 'athletes_data.json'
if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        existing_data = json.load(json_file)
else:
    existing_data = []

# 11. 새 데이터 추가
existing_data.extend(athlete_data)

# 12. JSON 파일로 저장
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

print(f"선수 데이터가 JSON 파일로 저장됨: {json_file_path}")
