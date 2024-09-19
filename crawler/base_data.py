import os
import requests
from bs4 import BeautifulSoup
import json

# 1. 메인 페이지 URL 설정
base_url = 'https://kr.ufc.com'
athletes_list_url = f'{base_url}/athletes/all'

# 2. 저장할 디렉토리 설정
images_dir = 'images'
html_dir = 'htmlStorage'
athlete_data = []

# 3. 디렉토리가 존재하지 않으면 생성
for directory in [images_dir, html_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# 4. 메인 페이지에서 데이터 크롤링
try:
    response = requests.get(athletes_list_url)
    response.raise_for_status()  # 요청이 성공했는지 확인
except requests.exceptions.RequestException as e:
    print(f"메인 페이지 요청 실패: {athletes_list_url}\n{e}")
    exit(1)

soup = BeautifulSoup(response.text, 'html.parser')

# 5. 'c-listing-athlete-flipcard__back' 클래스를 가진 div 요소 찾기
athlete_cards = soup.find_all('div', class_='c-listing-athlete-flipcard__back')

# 6. 각 선수의 이름과 이미지 추출 및 저장
for card in athlete_cards:
    # 6.1. 선수 이름 추출
    name_tag = card.find('span', class_='c-listing-athlete__name')
    if name_tag:
        name = name_tag.get_text().strip().lower().replace(' ', '-')
        kebab_case_name = name

        # 6.2. 선수 이미지 추출 및 저장
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

        # 6.3. 선수 상세 페이지 URL 생성 및 HTML 저장
        athlete_url = f'{base_url}/athlete/{kebab_case_name}'
        try:
            athlete_response = requests.get(athlete_url)
            athlete_response.raise_for_status()

            # HTML 파일 이름 및 경로 설정
            html_name = f"{kebab_case_name}.html"
            html_path = os.path.join(html_dir, html_name)

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

            # HTML 파일 저장
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(athlete_response.text)

            print(f"선수 페이지 저장됨: {html_path}")
        except requests.exceptions.RequestException as e:
            print(f"선수 페이지 요청 중 오류 발생: {athlete_url}\n{e}")

# 7. JSON 파일로 저장
json_file_path = 'athletes_data.json'
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(athlete_data, json_file, ensure_ascii=False, indent=4)

print(f"선수 데이터가 JSON 파일로 저장됨: {json_file_path}")
