import tensorflow as tf

# 이미지 데이터를 폴더에서 불러오기
datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

train_generator = datagen.flow_from_directory(
    'train/',  # 학습 이미지가 저장된 폴더
    target_size=(32, 32),  # 모든 이미지를 32x32 크기로 변경
    batch_size=32,
    class_mode='binary'  # 클래스가 2개라면 'binary', 3개 이상이면 'categorical'
)

# 모델 학습
history = tf.keras.model.fit(train_generator, epochs=10)
