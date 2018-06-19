# -*- coding: utf-8 -*-

import os
import numpy as np
import shutil
import torch 
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import numpy as np
from torch.autograd import Variable
cuda = torch.cuda.is_available()
import numpy as np

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hyper-parameters
sequence_length = 20
input_size = 5
hidden_size = 128
num_layers = 2
num_classes = 2
batch_size = 10
num_epochs = 5
learning_rate = 0.01

# Recurrent neural network (many-to-one)
class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        # input ==x : tensor of shape (batch_size, seq_length, hidden_size)
        #print(x.shape)
        # Set initial hidden and cell states 
        #output(x.shape)
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device) 
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        #hidden = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        # Forward propagate LSTM
        out,(h0,c0) = self.lstm(x)  # out: tensor of shape (batch_size, seq_length, hidden_size)

        #out, hidden = self.rnn(x, hidden)  # out: tensor of shape (batch_size, seq_length, hidden_size)
        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])#-1をしてseq_lengthを消去
        
        return out

def replace_csv_data():
    #shutil.rmtree("data/rep")
    #os.mkdir("data/rep")
    for name in range(1,10000):
        for year in range(2000,2018):
            if(os.path.exists('data/{0}_{1}.csv'.format(name,year))==True):
                f = open('data/{0}_{1}.csv'.format(name,year),encoding='cp932')#linux only need encoding=cp932?
                lines2 = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
                # lines2: リスト。要素は1行の文字列データ
                
                for line in lines2:
                    fout = open('data/rep/{0}_{1}.csv'.format(name,year), 'a')
                    line = line.replace('\"', '')
                    fout.write(line)
                    fout.close
                fout.close
                f.close
                
def mktrainset():
    hairetu = []
    hairetu = np.array(hairetu)
    labels = []
    labels = np.array(labels)
    for name in range(1,10000):
        for year in range(2000,2019):
            if(os.path.exists('data/{0}_{1}.csv'.format(name,year))==True):
                data = np.genfromtxt("data/rep/{0}_{1}.csv".format(name,year),delimiter=",", skip_header=2, dtype='int')
                data = np.delete(data, 0, 1)
                data = np.delete(data, 5, 1)
                maxcnt = data.shape[0]
                maxcnt = int(maxcnt/21)
                #始値 	高値	安値	終値	出来高
                for i in range(0,maxcnt):
                    #print(data[i*21:i*21+21].shape)
                    hairetu = np.append(hairetu,np.array(data[i*21:i*21+20]))
                    sub = data[i*21+20,3]-data[i*21+19,3]#最終日とその前日の差
                    if(sub>0):#値が上がっていればlabelに1を返す
                        label=1
                    else:
                        label=0
                    labels = np.append(labels,label)
        traindata = np.reshape(hairetu,(-1,20,5))#trainセットを作成
        #print(trainset.shape)#batch,days,features
        #print(labels.shape)
        
    return traindata,labels

  
#replace_csv_data()           
trainset,labels = mktrainset()

trainset = torch.from_numpy(trainset)
labels = torch.from_numpy(labels)
trainset = trainset.type(torch.FloatTensor)
labels = labels.type(torch.LongTensor)

model = RNN(input_size, hidden_size, num_layers, num_classes).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

total_step,_,_ = trainset.shape
roop = int(total_step/batch_size)

for epoch in range(num_epochs):
    for i in range(roop):
        images = trainset[i*batch_size:i*batch_size+batch_size]
        images = images.reshape(-1, sequence_length, input_size).to(device)
        label = labels[i*batch_size:i*batch_size+batch_size]
        label = label.to(device)
        
        # Forward pass
        #(h,c),hidden = model.initHidden()
        outputs = model(images)

        loss = criterion(outputs, label)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (i+1) % batch_size == 0:
            print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
                   .format(epoch+1, num_epochs, i+1, int(total_step/batch_size), loss.item()))
"""
# Test the model
with torch.no_grad():
    correct = 0
    total = 0
    for images, labels in test_loader:
        images = images.reshape(-1, sequence_length, input_size).to(device)
        labels = labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print('Test Accuracy of the model on the 10000 test images: {} %'.format(100 * correct / total)) 

# Save the model checkpoint
torch.save(model.state_dict(), 'model.ckpt')

"""

