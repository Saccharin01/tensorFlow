import tensorflow as tf

def build_model(dropout_rate: float = 0.5, layer_out_put: int = 5) -> tf.keras.Model:
    layers = tf.keras
    """
    CNN 모델을 생성하는 함수입니다.

    * Args:
        dropout_rate (float, optional): 드롭아웃 레이어의 비율. 기본값은 0.5입니다.
        layer_out_put (int, optional): 출력 레이어의 노드 수. 기본값은 5입니다.

    * Returns:
        tf.keras.Model: 구성된 Keras 모델
    """
    
    model = tf.keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 256, 3)),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(dropout_rate), 
        layers.Dense(layer_out_put)
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    return model
