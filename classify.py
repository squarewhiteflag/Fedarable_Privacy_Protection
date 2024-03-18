import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#matplotlib inline
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import cv2


import tensorflow as tf
#from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras_preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import InputLayer, Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications.efficientnet import EfficientNetB3
from tensorflow.keras.optimizers import Adam

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

# 设置数据路径
data_path = os.path.join('D:\Python Project\COVID')#变换设备的时候需更改
train_data_path = os.path.join(data_path, 'train')
test_data_path = os.path.join(data_path,'test')

# 从txt文件中读取训练和测试数据集的DataFrame
train_df = pd.read_csv(os.path.join(data_path, 'train.txt'), sep=" ", index_col=None, header=None)
test_df = pd.read_csv(os.path.join(data_path, 'test.txt'), sep=" ", index_col=None, header=None)

train_df.head()
#print(train_df.columns)
#print(test_df.columns)

# 删除训练和测试数据集DataFrame中指定的列
train_df.drop(columns = [0,3], axis=1, inplace=True)
test_df.drop(columns = [0,3], axis=1, inplace=True)
#train_df.drop(columns=['image_name', 'diagnosis'], inplace=True)
#test_df.drop(columns=['image_name', 'diagnosis'], inplace=True)







# 给列命名
train_df.columns = ['image_name', 'diagnosis']
test_df.columns = ['image_name', 'diagnosis']
train_df.head()
# 统计训练和测试数据集中不同类别的样本数量
train_df.diagnosis.value_counts()

test_df.diagnosis.value_counts()

# 获取测试数据集中不同类别的标签
clas = np.unique(test_df.diagnosis)

rand_indx = np.random.randint(0,len(train_df),1)[0]
img = cv2.imread(os.path.join(train_data_path, train_df.image_name[rand_indx]))
plt.imshow(img/255)
plt.title(train_df.diagnosis[rand_indx])
plt.show()
img.shape

# 设置批量大小、训练验证数据集划分的种子和目标图像大小（模型开整）
batch_size = 32
#batch_size = 12
train_vla_sesd = 40
target_size = (256, 256)

# 创建训练验证数据集和测试数据集的图像生成器
train_val_Gen = ImageDataGenerator( rescale = 1.0/255,
                                    validation_split=0.1)
test_Gen = ImageDataGenerator( rescale = 1.0/255)

# 生成训练数据集
'''train_data = train_val_Gen.flow_from_dataframe(train_df,
                                               train_data_path,
                                               x_col='image_name',
                                               y_col='diagnosis',
                                               target_size=target_size,
                                               class_mode='binary',
                                               batch_size=batch_size,
                                               seed=train_vla_sesd,
                                              subset='training'
                                              )'''
train_data = train_val_Gen.flow_from_dataframe(train_df,
                                               train_data_path,
                                               x_col='image_name',
                                               y_col='diagnosis',
                                               target_size=target_size,
                                               class_mode='binary',
                                               batch_size=batch_size,
                                               seed=train_vla_sesd,
                                               subset='training'

                                               )
#这条修补版加的
#train_data_repeated = [data for data in train_data] * 40


#train_data = train_data.repeat()

# 生成验证数据集
val_data = train_val_Gen.flow_from_dataframe(train_df,
                                               train_data_path,
                                               x_col='image_name',
                                               y_col='diagnosis',
                                               target_size=target_size,
                                               class_mode='binary',
                                               batch_size=batch_size,
                                               seed=train_vla_sesd,
                                               subset='validation'
                                              )

# 生成测试数据集
test_data = test_Gen.flow_from_dataframe(test_df,
                                       test_data_path,
                                       x_col='image_name',
                                       y_col='diagnosis',
                                       target_size=target_size,
                                       class_mode='binary',
                                       batch_size=batch_size
                                      )

#后加的#这一坨好像没卵用了
print(len(train_data))
#the same  image with incoded labels and scaled 1/255

plt.imshow(train_data[int(rand_indx/32)][0][(rand_indx%32)-1])
plt.title(train_data[int(rand_indx/32)][1][(rand_indx%32)-1])

#plt.imshow(train_data[int(rand_indx/12)][0][(rand_indx%12)-1])
#plt.title(train_data[int(rand_indx/12)][1][(rand_indx%12)-1])
plt.show()

ef_model = EfficientNetB3(include_top=False)

model = Sequential()

#model.add(InputLayer(input_shape=(256,256,3)))
model.add(InputLayer(shape=(256,256,3)))
model.add(ef_model)

for layer in ef_model.layers:
    layer.trainable = False

model.add(GlobalAveragePooling2D())

model.add(Dense(256, activation='relu'))
#model.add(Dense(512, activation='tanh'))
model.add(Dense(128, activation='relu'))

model.add(Dropout(0.5))

model.add(Dense(1, activation='sigmoid'))

model.summary()

#这里在神奇的mac上正确率会下降，但显示我内存爆了，不太确定是程序还是电脑的问题
lR = 1e-2
loss='binary_crossentropy'
metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]

model.compile(optimizer=Adam(learning_rate=lR),
              loss= loss,
              metrics=metrics)

epochs = 40
for epoch in range(epochs):
    # 在每个训练周期结束后清理 TensorFlow 会话
    tf.keras.backend.clear_session()

    # 进行模型训练
    results = model.fit(train_data,
                        epochs=1,  # 每次只训练一个周期
                        validation_data=val_data,
                        steps_per_epoch=len(train_data),
                        validation_steps=len(val_data))

    # 打印训练过程中的指标等信息
    #print(f"Epoch {epoch + 1}/{epochs}:")
    #print(f"Training Loss: {results.history['loss']}")
    #print(f"Validation Loss: {results.history['val_loss']}")


# 训练结束后清理一次 TensorFlow 会话
tf.keras.backend.clear_session()

'''results = model.fit(train_data,
                     epochs=40,
                     validation_data=val_data,
                     steps_per_epoch=len(train_data),
                    validation_steps=len(val_data))'''

#model.evaluate(test_data)
model.evaluate(test_data)
#yPred = model.predict(test_data)
yPred = model.predict(test_data)
yPred = np.where(yPred >= 0.5, 1, 0)
confusion_matrix(test_data.labels, yPred)
# 得到过程矩阵
loss = results.history['loss']
val_loss = results.history['val_loss']
acc = results.history['accuracy']
val_acc = results.history['val_accuracy']
precision = results.history['precision']
val_precision = results.history['val_precision']
recall = results.history['recall']
val_recall = results.history['val_recall']

# 画图部分
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

#绘图和形成文件都gpt抄的，问题不大，能跑
# Plot binary cross-entropy
axs[0, 0].plot(loss, label='training')
axs[0, 0].plot(val_loss, label='validation')
axs[0, 0].set_title('Binary Cross-Entropy')
axs[0, 0].legend()

# Plot accuracy
axs[0, 1].plot(acc, label='training')
axs[0, 1].plot(val_acc, label='validation')
axs[0, 1].set_title('Accuracy')
axs[0, 1].legend()

# Plot precision
axs[1, 0].plot(precision, label='training')
axs[1, 0].plot(val_precision, label='validation')
axs[1, 0].set_title('Precision')
axs[1, 0].legend()

# Plot recall
axs[1, 1].plot(recall, label='training')
axs[1, 1].plot(val_recall, label='validation')
axs[1, 1].set_title('Recall')
axs[1, 1].legend()

# Show the plot
plt.show()
rand_bachs = np.random.randint(0, len(test_data), 4)
rand_images = np.random.randint(0, 32, 4)

fig, axs = plt.subplots(4, 4, figsize=(20, 20))
for i, bach in enumerate(rand_bachs):
    for j, image in enumerate(rand_images):
        axs[i, j].imshow(test_data[bach][0][image])
        title = f'True: {test_data[bach][1][image]} Predicted: {yPred[(bach * 32) + image - 1]}'
        axs[i, j].set_title(title)

plt.show()
model.save('Covid-19_X-rai_diagnosis.h5')
