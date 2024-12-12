import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.optimizers import Adam
from matplotlib.dates import DateFormatter, YearLocator

# 下载苹果公司的数据
apple_data = yf.download('AAPL', start='2020-01-01', end='2024-11-28')

# 提取调整后的收盘价数据
data = apple_data[['Adj Close']].reset_index()

# 将日期设置为索引
data.set_index('Date', inplace=True)

# 将数据框转换为numpy数组
dataset = data.values.reshape(-1, 1)

# 缩放数据
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

# 创建训练数据集
training_data_len = int(len(scaled_data) * 0.95)
train_data = scaled_data[0:training_data_len, :]

# 将数据拆分为x_train和y_train数据集
x_train = []
y_train = []

for i in range(60, len(train_data)):
    x_train.append(train_data[i - 60:i, 0])
    y_train.append(train_data[i, 0])

# 将x_train和y_train转换为numpy数组
x_train, y_train = np.array(x_train), np.array(y_train)

# 调整数据形状
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# 构建LSTM模型
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(64, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(25))
model.add(Dense(1))

# 编译模型
model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

# 训练模型
model.fit(x_train, y_train, batch_size=1, epochs=20)

# 创建测试数据集
test_data = scaled_data[training_data_len - 60:, :]
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
    x_test.append(test_data[i - 60:i, 0])

# 将测试数据转换为numpy数组
x_test = np.array(x_test)

# 调整数据形状
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# 获取模型的预测值
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions).flatten()

# 计算均方根误差 (RMSE)
rmse = np.sqrt(np.mean(((predictions - y_test.flatten()) ** 2)))
print(f"RMSE: {rmse}")

# 绘制实际值和预测值
train = data.iloc[:training_data_len]
valid = data.iloc[training_data_len:]
valid = valid.copy()  # 避免SettingWithCopyWarning
valid['Predictions'] = predictions

plt.figure(figsize=(14, 8))
plt.plot(train['Adj Close'], label='Train')
plt.plot(valid['Adj Close'], label='Val')
plt.plot(valid['Predictions'], label='Predictions')
plt.title('Apple Stock Prediction')
plt.xlabel('Date')
plt.ylabel('Close Price USD ($)')
plt.legend()
plt.gca().xaxis.set_major_formatter(DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(YearLocator())
plt.show()


