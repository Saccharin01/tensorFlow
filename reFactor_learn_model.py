import json
import numpy as np
import tensorflow as tf
from sklearn.model_selection import KFold
from modules.visulaize_history import visulaize_history
from modules.build_model import build_model
from modules.preprocess_image import preprocess_image
from modules.data_generator import data_generator

# JSON 파일 읽기
with open('athletes_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 이미지와 레이블 준비
images = []
labels = []

for entry in data:
    img_path = entry['img']
    img_array = preprocess_image(img_path, (128,256))
    images.append(img_array)
    
    # 레이블: 공격력, 방어력, 정확도
    labels.append([
        1 if entry['species'] == 'person' else 0,
        float(entry['attack']),
        float(entry['defense']),
        float(entry['accuracy'].replace('%', '').strip()),
        float(entry['weight']),
        ])

# NumPy 배열로 변환
X = np.array(images)
y = np.array(labels)

# 데이터 증강 설정
datagen = data_generator()


# 교차 검증 설정
kfold = KFold(n_splits=5, shuffle=True)
fold_no = 1
all_histories = []

for train_index, test_index in kfold.split(X):
    # Train/Test 데이터셋 나누기
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    # 데이터 증강을 통해 학습 데이터 생성
    train_datagen = datagen.flow(X_train, y_train, batch_size=16)

    # 모델 빌드
    athlete_model = build_model()

    # Early Stopping 설정
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    
    # 모델 학습
    history = athlete_model.fit(
        train_datagen,
        steps_per_epoch=len(X_train) // 16,  # 각 에포크에서의 스텝 수
        epochs=10,
        validation_data=(X_test, y_test),  # 검증 데이터는 증강하지 않음
        callbacks=[early_stopping]
    )
    
    # 학습 로그 저장
    all_histories.append(history)
    athlete_model.save(f"M{fold_no}.keras")
    
    fold_no += 1

    # 모델 저장

# 모든 폴드의 학습 기록 시각화
for i, history in enumerate(all_histories):
    visulaize_history(history, title=f"M{i + 1} Learning History")