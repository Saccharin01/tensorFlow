import tensorflow as tf
import matplotlib.pyplot as plt

# 모델 로드
model = tf.keras.models
m4_model = model.load_model('m4.keras')

# 모든 레이어의 가중치와 편향 정보 가져오기
weights = m4_model.get_weights()

# 전체 레이어의 가중치와 편향 분포 시각화
num_layers = len(weights) // 2  # 가중치와 편향이 한 쌍씩 있으므로 총 레이어 수는 weights의 절반

plt.figure(figsize=(15, 5 * num_layers))  # 그래프 크기 조정

for layer_num in range(num_layers):
    # 각 레이어의 가중치와 편향을 가져옴
    layer_weights = weights[layer_num * 2]      # 가중치
    layer_bias = weights[layer_num * 2 + 1]     # 편향
    
    # 가중치 분포 시각화
    plt.subplot(num_layers, 2, layer_num * 2 + 1)  # 서브플롯 생성
    plt.hist(layer_weights.flatten(), bins=50)
    plt.title(f'M4 Layer No.{layer_num + 1} Weight Distribution')
    plt.xlabel('Weight Value')
    plt.ylabel('Frequency')
    
    # 편향 분포 시각화
    plt.subplot(num_layers, 2, layer_num * 2 + 2)  # 서브플롯 생성
    plt.hist(layer_bias.flatten(), bins=50)
    plt.title(f'M4 Layer No.{layer_num + 1} Bias Distribution')
    plt.xlabel('Bias Value')
    plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
