import json
import numpy as np
import tensorflow as tf
from sklearn.model_selection import KFold
from visualize import plot_history

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
    img = img_process.load_img(img_path, target_size=(128, 256))  # 이미지 크기 조정
    img_array = img_process.img_to_array(img) / 255.0  # 정규화
    images.append(img_array)
    
    # 레이블: 공격력, 방어력, 정확도
    labels.append([float(entry['attack']), float(entry['defense']), float(entry['accuracy'].replace('%', '').strip())])

# NumPy 배열로 변환
X = np.array(images)
y = np.array(labels)

# 모델 정의 함수
def build_model():
    model = tf.keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 256, 3)),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),  # Dropout 추가
        layers.Dense(3)  # 공격력, 방어력, 정확도 출력
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    return model

# 교차 검증 설정
kfold = KFold(n_splits=5, shuffle=True)
fold_no = 1
all_histories = []

for train_index, test_index in kfold.split(X):
    # Train/Test 데이터셋 나누기
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    # 모델 빌드
    athlete_model = build_model()

    # Early Stopping 설정
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    
    # 모델 학습
    history = athlete_model.fit(
        X_train, y_train,
        epochs=3,
        batch_size=16,
        validation_data=(X_test, y_test),
        callbacks=[early_stopping]
    )
    
    # 학습 로그 저장
    all_histories.append(history)
    fold_no += 1

    # 모델 저장
    athlete_model.save(f"athlete_model_fold_{fold_no}.keras")

# 마지막 학습 기록 시각화
plot_history(all_histories[-1])
