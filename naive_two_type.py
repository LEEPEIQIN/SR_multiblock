#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from random import randrange
from PIL import Image
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.nn.init as init
import math

def psnr(target, ref):
    # target:目标图像  ref:参考图像 
    # assume RGB image
    diff = ref- target
    diff = diff.reshape(-1)
    rmse = torch.sqrt((diff ** 2.).mean())
    return 20*torch.log10(1.0/rmse)
#test loader:
test_LR = torchvision.datasets.ImageFolder(root='2_LR_test', transform=transforms.ToTensor())
LR_2_test = torch.utils.data.DataLoader(test_LR, batch_size=1, shuffle=False, num_workers=0)
test_HR = torchvision.datasets.ImageFolder(root='2_HR_test', transform=transforms.ToTensor())
HR_2_test = torch.utils.data.DataLoader(test_HR, batch_size=1, shuffle=False, num_workers=0)
## train set generator:
def generator():
    #given:
    HR_URL='2_HR'
    LR_URL='2_LR'
    batch_size=8
    image_size=120
    channel=3
    #genereting:
    HR_set=torchvision.datasets.ImageFolder(root=HR_URL)
    LR_set=torchvision.datasets.ImageFolder(root=LR_URL)
    HR_torch=torch.zeros([batch_size,channel,image_size,image_size])
    LR_torch=torch.zeros([batch_size,channel,image_size,image_size])
    for i in range(batch_size):
        img_number=randrange(len(HR_set))
        HR_img=Image.open(HR_set.imgs[img_number][0])
        LR_img=Image.open(LR_set.imgs[img_number][0])
        y,x=HR_img.size
        X=randrange(0,x-image_size)
        Y=randrange(0,y-image_size)
        HR_img=torchvision.transforms.functional.crop(HR_img, X, Y, image_size, image_size)
        LR_img=torchvision.transforms.functional.crop(LR_img, X, Y, image_size, image_size)
        #whether rotate and whether flipHR_:
        p_f=randrange(2)
        d_r=randrange(4)*90
        HR_img=torchvision.transforms.functional.rotate(HR_img,d_r)
        LR_img=torchvision.transforms.functional.rotate(LR_img,d_r)
        if (p_f==1):
            HR_img=HR_img.transpose(Image.FLIP_LEFT_RIGHT)
            LR_img=LR_img.transpose(Image.FLIP_LEFT_RIGHT)
        ##tensor defined:
        HR_torch[i,:,:,:]=torchvision.transforms.functional.to_tensor(HR_img)
        LR_torch[i,:,:,:]=torchvision.transforms.functional.to_tensor(LR_img)
    ans=[HR_torch,LR_torch]
    return ans
#########################################################
    

#########################################################
class Net_plus(nn.Module):
    def __init__(self):
        super(Net_plus, self).__init__()
        self.pooling=nn.AdaptiveAvgPool2d(1)
        #initial cnn:
        self.int = nn.Conv2d(3, 64, (3, 3), (1, 1), (1, 1))
        #RB_1:
        self.RB_1_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_1_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_1_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_1_1d2 = nn.Conv1d(16,64,1,1)
        #RB_2:
        self.RB_2_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_2_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_2_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_2_1d2 = nn.Conv1d(16,64,1,1)
        #RB_3:
        self.RB_3_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_3_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_3_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_3_1d2 = nn.Conv1d(16,64,1,1)
        #RB_4:
        self.RB_4_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_4_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_4_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_4_1d2 = nn.Conv1d(16,64,1,1)
        #RB_5:
        self.RB_5_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_5_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_5_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_5_1d2 = nn.Conv1d(16,64,1,1)
        #RB_6:
        self.RB_6_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_6_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_6_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_6_1d2 = nn.Conv1d(16,64,1,1)
        #RB_7:
        self.RB_7_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_7_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_7_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_7_1d2 = nn.Conv1d(16,64,1,1)
        #RB_8:
        self.RB_8_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_8_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_8_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_8_1d2 = nn.Conv1d(16,64,1,1)
        #RB_9:
        self.RB_9_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_9_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_9_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_9_1d2 = nn.Conv1d(16,64,1,1)
        #RB_10:
        self.RB_10_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_10_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_10_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_10_1d2 = nn.Conv1d(16,64,1,1)
         #RB_11:
        self.RB_11_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_11_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_11_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_11_1d2 = nn.Conv1d(16,64,1,1)
        #RB_12:
        self.RB_12_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_12_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_12_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_12_1d2 = nn.Conv1d(16,64,1,1)
        #RB_13:
        self.RB_13_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_13_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_13_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_13_1d2 = nn.Conv1d(16,64,1,1)
        #RB_14:
        self.RB_14_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_14_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_14_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_14_1d2 = nn.Conv1d(16,64,1,1)
        #RB_15:
        self.RB_15_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_15_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_15_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_15_1d2 = nn.Conv1d(16,64,1,1)
        #RB_16:
        self.RB_16_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_16_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.RB_16_1d1 = nn.Conv1d(64,16,1,1)
        self.RB_16_1d2 = nn.Conv1d(16,64,1,1)
        #RB_17:
        #self.RB_17_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        #self.RB_17_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        #self.RB_17_1d1 = nn.Conv1d(64,16,1,1)
        #self.RB_17_1d2 = nn.Conv1d(16,64,1,1)
        #RB_18:
        #self.RB_18_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        #self.RB_18_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        #self.RB_18_1d1 = nn.Conv1d(64,16,1,1)
        #self.RB_18_1d2 = nn.Conv1d(16,64,1,1)
        #RB_19:
        #self.RB_19_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        #self.RB_19_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        #self.RB_19_1d1 = nn.Conv1d(64,16,1,1)
        #self.RB_19_1d2 = nn.Conv1d(16,64,1,1)
        #RB_20:
        #self.RB_20_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        #self.RB_20_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        #self.RB_20_1d1 = nn.Conv1d(64,16,1,1)
        #self.RB_20_1d2 = nn.Conv1d(16,64,1,1)
        #end cnn:
        self.end_RB=nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.toR=nn.Conv2d(64, 3, (3, 3), (1, 1), (1, 1))
        self._initialize_weights()

    def forward(self, x):
        LR=x
        x=self.int(x)
        
        #RB_1
        R_1=x
        x=F.relu(self.RB_1_conv1(x))
        x=self.RB_1_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_1_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_1_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_1
        #RB_2
        R_2=x
        x=F.relu(self.RB_2_conv1(x))
        x=self.RB_2_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_2_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_2_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_2
        #RB_3
        R_3=x
        x=F.relu(self.RB_3_conv1(x))
        x=self.RB_3_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_3_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_3_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_3
        #RB_4
        R_4=x
        x=F.relu(self.RB_4_conv1(x))
        x=self.RB_4_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_4_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_4_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_4
        #RB_5
        R_5=x
        x=F.relu(self.RB_5_conv1(x))
        x=self.RB_5_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_5_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_5_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_5
        #RB_6
        R_6=x
        x=F.relu(self.RB_6_conv1(x))
        x=self.RB_6_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_6_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_6_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_6
        #RB_7
        R_7=x
        x=F.relu(self.RB_7_conv1(x))
        x=self.RB_7_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_7_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_7_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_7
        #RB_8
        R_8=x
        x=F.relu(self.RB_8_conv1(x))
        x=self.RB_8_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_8_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_8_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_8
        #RB_9
        R_9=x
        x=F.relu(self.RB_9_conv1(x))
        x=self.RB_9_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_9_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_9_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_9
        #RB_10
        R_10=x
        x=F.relu(self.RB_10_conv1(x))
        x=self.RB_10_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_10_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_10_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_10
        
        #RB_11
        R_11=x
        x=F.relu(self.RB_11_conv1(x))
        x=self.RB_11_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_11_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_11_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_11
        #RB_12
        R_12=x
        x=F.relu(self.RB_12_conv1(x))
        x=self.RB_12_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_12_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_12_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_12
        #RB_13
        R_13=x
        x=F.relu(self.RB_13_conv1(x))
        x=self.RB_13_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_13_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_13_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_13
        #RB_14
        R_14=x
        x=F.relu(self.RB_14_conv1(x))
        x=self.RB_14_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_14_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_14_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_14
        #RB_15
        R_15=x
        x=F.relu(self.RB_15_conv1(x))
        x=self.RB_15_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_15_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_15_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_15
        #RB_16
        R_16=x
        x=F.relu(self.RB_16_conv1(x))
        x=self.RB_16_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.RB_16_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.RB_16_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_16     
        #end:
        x=self.end_RB(x)
        x=self.toR(x)
        x+=LR
        x[x < 0.0] = 0.0
        x[x>1.0]=1.0
        return x
    def _initialize_weights(self):
        init.orthogonal_(self.int.weight)
        
        #RB_1
        init.orthogonal_(self.RB_1_conv1.weight)
        init.orthogonal_(self.RB_1_conv2.weight)
        init.orthogonal_(self.RB_1_1d1.weight)
        init.orthogonal_(self.RB_1_1d2.weight)
        #RB_2
        init.orthogonal_(self.RB_2_conv1.weight)
        init.orthogonal_(self.RB_2_conv2.weight)
        init.orthogonal_(self.RB_2_1d1.weight)
        init.orthogonal_(self.RB_2_1d2.weight)
        #RB_3
        init.orthogonal_(self.RB_3_conv1.weight)
        init.orthogonal_(self.RB_3_conv2.weight)
        init.orthogonal_(self.RB_3_1d1.weight)
        init.orthogonal_(self.RB_3_1d2.weight)
        #RB_4
        init.orthogonal_(self.RB_4_conv1.weight)
        init.orthogonal_(self.RB_4_conv2.weight)
        init.orthogonal_(self.RB_4_1d1.weight)
        init.orthogonal_(self.RB_4_1d2.weight)
        #RB_5
        init.orthogonal_(self.RB_5_conv1.weight)
        init.orthogonal_(self.RB_5_conv2.weight)
        init.orthogonal_(self.RB_5_1d1.weight)
        init.orthogonal_(self.RB_5_1d2.weight)
        #RB_6
        init.orthogonal_(self.RB_6_conv1.weight)
        init.orthogonal_(self.RB_6_conv2.weight)
        init.orthogonal_(self.RB_6_1d1.weight)
        init.orthogonal_(self.RB_6_1d2.weight)
        #RB_7
        init.orthogonal_(self.RB_7_conv1.weight)
        init.orthogonal_(self.RB_7_conv2.weight)
        init.orthogonal_(self.RB_7_1d1.weight)
        init.orthogonal_(self.RB_7_1d2.weight)
        #RB_8
        init.orthogonal_(self.RB_8_conv1.weight)
        init.orthogonal_(self.RB_8_conv2.weight)
        init.orthogonal_(self.RB_8_1d1.weight)
        init.orthogonal_(self.RB_8_1d2.weight)
        #RB_9
        init.orthogonal_(self.RB_9_conv1.weight)
        init.orthogonal_(self.RB_9_conv2.weight)
        init.orthogonal_(self.RB_9_1d1.weight)
        init.orthogonal_(self.RB_9_1d2.weight)
        #RB_10
        init.orthogonal_(self.RB_10_conv1.weight)
        init.orthogonal_(self.RB_10_conv2.weight)
        init.orthogonal_(self.RB_10_1d1.weight)
        init.orthogonal_(self.RB_10_1d2.weight)
        #RB_11
        init.orthogonal_(self.RB_11_conv1.weight)
        init.orthogonal_(self.RB_11_conv2.weight)
        init.orthogonal_(self.RB_11_1d1.weight)
        init.orthogonal_(self.RB_11_1d2.weight)
        #RB_12
        init.orthogonal_(self.RB_12_conv1.weight)
        init.orthogonal_(self.RB_12_conv2.weight)
        init.orthogonal_(self.RB_12_1d1.weight)
        init.orthogonal_(self.RB_12_1d2.weight)
        #RB_13
        init.orthogonal_(self.RB_13_conv1.weight)
        init.orthogonal_(self.RB_13_conv2.weight)
        init.orthogonal_(self.RB_13_1d1.weight)
        init.orthogonal_(self.RB_13_1d2.weight)
        #RB_14
        init.orthogonal_(self.RB_14_conv1.weight)
        init.orthogonal_(self.RB_14_conv2.weight)
        init.orthogonal_(self.RB_14_1d1.weight)
        init.orthogonal_(self.RB_14_1d2.weight)
        #RB_15
        init.orthogonal_(self.RB_15_conv1.weight)
        init.orthogonal_(self.RB_15_conv2.weight)
        init.orthogonal_(self.RB_15_1d1.weight)
        init.orthogonal_(self.RB_15_1d2.weight)
        #RB_16
        init.orthogonal_(self.RB_16_conv1.weight)
        init.orthogonal_(self.RB_16_conv2.weight)
        init.orthogonal_(self.RB_16_1d1.weight)
        init.orthogonal_(self.RB_16_1d2.weight)
        #RB_17
        #init.orthogonal_(self.RB_17_conv1.weight)
        #init.orthogonal_(self.RB_17_conv2.weight)
        #init.orthogonal_(self.RB_17_1d1.weight)
        #init.orthogonal_(self.RB_17_1d2.weight)
        #RB_18
        #init.orthogonal_(self.RB_18_conv1.weight)
        #init.orthogonal_(self.RB_18_conv2.weight)
        #init.orthogonal_(self.RB_18_1d1.weight)
        #init.orthogonal_(self.RB_18_1d2.weight)
        #RB_19
        #init.orthogonal_(self.RB_19_conv1.weight)
        #init.orthogonal_(self.RB_19_conv2.weight)
        #init.orthogonal_(self.RB_19_1d1.weight)
        #init.orthogonal_(self.RB_19_1d2.weight)
        #RB_20
        #init.orthogonal_(self.RB_20_conv1.weight)
        #init.orthogonal_(self.RB_20_conv2.weight)
        #init.orthogonal_(self.RB_20_1d1.weight)
        #init.orthogonal_(self.RB_20_1d2.weight)
        
        init.orthogonal_(self.end_RB.weight)
        init.orthogonal_(self.toR.weight)
    
    

class Net_combine(nn.Module):
    def __init__(self):
        super(Net_combine, self).__init__()
        self.pooling=nn.AdaptiveAvgPool2d(1)
        #initial cnn:
        self.a1_int = nn.Conv2d(3, 64, (3, 3), (1, 1), (1, 1))
        #RB_1:
        self.a1_RB_1_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_1_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_1_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_1_1d2 = nn.Conv1d(16,64,1,1)
        #RB_2:
        self.a1_RB_2_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_2_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_2_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_2_1d2 = nn.Conv1d(16,64,1,1)
        #RB_3:
        self.a1_RB_3_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_3_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_3_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_3_1d2 = nn.Conv1d(16,64,1,1)
        #RB_4:
        self.a1_RB_4_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_4_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_4_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_4_1d2 = nn.Conv1d(16,64,1,1)
        #RB_5:
        self.a1_RB_5_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_5_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_5_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_5_1d2 = nn.Conv1d(16,64,1,1)
        #RB_6:
        self.a1_RB_6_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_6_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_6_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_6_1d2 = nn.Conv1d(16,64,1,1)
        #RB_7:
        self.a1_RB_7_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_7_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_7_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_7_1d2 = nn.Conv1d(16,64,1,1)
        #RB_8:
        self.a1_RB_8_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_8_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_8_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_8_1d2 = nn.Conv1d(16,64,1,1)
        #RB_9:
        self.a1_RB_9_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_9_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_9_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_9_1d2 = nn.Conv1d(16,64,1,1)
        #RB_10:
        self.a1_RB_10_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_10_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_10_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_10_1d2 = nn.Conv1d(16,64,1,1)
         #RB_11:
        self.a1_RB_11_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_11_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_11_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_11_1d2 = nn.Conv1d(16,64,1,1)
        #RB_12:
        self.a1_RB_12_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_12_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_12_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_12_1d2 = nn.Conv1d(16,64,1,1)
        #RB_13:
        self.a1_RB_13_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_13_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_13_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_13_1d2 = nn.Conv1d(16,64,1,1)
        #RB_14:
        self.a1_RB_14_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_14_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_14_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_14_1d2 = nn.Conv1d(16,64,1,1)
        #RB_15:
        self.a1_RB_15_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_15_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_15_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_15_1d2 = nn.Conv1d(16,64,1,1)
        #RB_16:
        self.a1_RB_16_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_16_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_RB_16_1d1 = nn.Conv1d(64,16,1,1)
        self.a1_RB_16_1d2 = nn.Conv1d(16,64,1,1)
        #end cnn:
        self.a1_end_RB=nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a1_toR=nn.Conv2d(64, 3, (3, 3), (1, 1), (1, 1))
       
        
        #initial cnn:
        self.a2_int = nn.Conv2d(3, 64, (3, 3), (1, 1), (1, 1))
        #RB_1:
        self.a2_RB_1_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_1_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_1_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_1_1d2 = nn.Conv1d(16,64,1,1)
        #RB_2:
        self.a2_RB_2_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_2_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_2_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_2_1d2 = nn.Conv1d(16,64,1,1)
        #RB_3:
        self.a2_RB_3_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_3_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_3_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_3_1d2 = nn.Conv1d(16,64,1,1)
        #RB_4:
        self.a2_RB_4_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_4_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_4_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_4_1d2 = nn.Conv1d(16,64,1,1)
        #RB_5:
        self.a2_RB_5_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_5_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_5_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_5_1d2 = nn.Conv1d(16,64,1,1)
        #RB_6:
        self.a2_RB_6_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_6_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_6_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_6_1d2 = nn.Conv1d(16,64,1,1)
        #RB_7:
        self.a2_RB_7_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_7_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_7_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_7_1d2 = nn.Conv1d(16,64,1,1)
        #RB_8:
        self.a2_RB_8_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_8_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_8_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_8_1d2 = nn.Conv1d(16,64,1,1)
        #RB_9:
        self.a2_RB_9_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_9_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_9_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_9_1d2 = nn.Conv1d(16,64,1,1)
        #RB_10:
        self.a2_RB_10_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_10_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_10_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_10_1d2 = nn.Conv1d(16,64,1,1)
         #RB_11:
        self.a2_RB_11_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_11_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_11_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_11_1d2 = nn.Conv1d(16,64,1,1)
        #RB_12:
        self.a2_RB_12_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_12_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_12_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_12_1d2 = nn.Conv1d(16,64,1,1)
        #RB_13:
        self.a2_RB_13_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_13_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_13_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_13_1d2 = nn.Conv1d(16,64,1,1)
        #RB_14:
        self.a2_RB_14_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_14_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_14_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_14_1d2 = nn.Conv1d(16,64,1,1)
        #RB_15:
        self.a2_RB_15_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_15_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_15_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_15_1d2 = nn.Conv1d(16,64,1,1)
        #RB_16:
        self.a2_RB_16_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_16_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_RB_16_1d1 = nn.Conv1d(64,16,1,1)
        self.a2_RB_16_1d2 = nn.Conv1d(16,64,1,1)
        #end cnn:
        self.a2_end_RB=nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a2_toR=nn.Conv2d(64, 3, (3, 3), (1, 1), (1, 1))
        
        #initial cnn:
        self.a3_int = nn.Conv2d(3, 64, (3, 3), (1, 1), (1, 1))
        #RB_1:
        self.a3_RB_1_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_1_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_1_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_1_1d2 = nn.Conv1d(16,64,1,1)
        #RB_2
        self.a3_RB_2_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_2_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_2_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_2_1d2 = nn.Conv1d(16,64,1,1)
        #RB_3:
        self.a3_RB_3_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_3_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_3_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_3_1d2 = nn.Conv1d(16,64,1,1)
        #RB_4:
        self.a3_RB_4_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_4_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_4_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_4_1d2 = nn.Conv1d(16,64,1,1)
        #RB_5:
        self.a3_RB_5_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_5_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_5_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_5_1d2 = nn.Conv1d(16,64,1,1)
        #RB_6:
        self.a3_RB_6_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_6_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_6_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_6_1d2 = nn.Conv1d(16,64,1,1)
        #RB_7:
        self.a3_RB_7_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_7_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_7_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_7_1d2 = nn.Conv1d(16,64,1,1)
        #RB_8:
        self.a3_RB_8_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_8_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_8_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_8_1d2 = nn.Conv1d(16,64,1,1)
        #RB_9:
        self.a3_RB_9_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_9_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_9_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_9_1d2 = nn.Conv1d(16,64,1,1)
        #RB_10:
        self.a3_RB_10_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_10_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_10_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_10_1d2 = nn.Conv1d(16,64,1,1)
         #RB_11:
        self.a3_RB_11_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_11_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_11_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_11_1d2 = nn.Conv1d(16,64,1,1)
        #RB_12:
        self.a3_RB_12_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_12_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_12_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_12_1d2 = nn.Conv1d(16,64,1,1)
        #RB_13:
        self.a3_RB_13_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_13_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_13_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_13_1d2 = nn.Conv1d(16,64,1,1)
        #RB_14:
        self.a3_RB_14_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_14_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_14_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_14_1d2 = nn.Conv1d(16,64,1,1)
        #RB_15:
        self.a3_RB_15_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_15_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_15_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_15_1d2 = nn.Conv1d(16,64,1,1)
        #RB_16:
        self.a3_RB_16_conv1 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_16_conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_RB_16_1d1 = nn.Conv1d(64,16,1,1)
        self.a3_RB_16_1d2 = nn.Conv1d(16,64,1,1)
        #end cnn:
        self.a3_end_RB=nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
        self.a3_toR=nn.Conv2d(64, 3, (3, 3), (1, 1), (1, 1))

    def forward(self, x):
        LR=x
        x=self.a1_int(x)
        #RB_1
        R_1=x
        x=F.relu(self.a1_RB_1_conv1(x))
        x=self.a1_RB_1_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_1_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_1_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_1
        #RB_2
        R_2=x
        x=F.relu(self.a1_RB_2_conv1(x))
        x=self.a1_RB_2_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_2_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_2_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_2
        #RB_3
        R_3=x
        x=F.relu(self.a1_RB_3_conv1(x))
        x=self.a1_RB_3_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_3_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_3_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_3
        #RB_4
        R_4=x
        x=F.relu(self.a1_RB_4_conv1(x))
        x=self.a1_RB_4_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_4_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_4_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_4
        #RB_5
        R_5=x
        x=F.relu(self.a1_RB_5_conv1(x))
        x=self.a1_RB_5_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_5_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_5_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_5
        #RB_6
        R_6=x
        x=F.relu(self.a1_RB_6_conv1(x))
        x=self.a1_RB_6_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_6_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_6_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_6
        #RB_7
        R_7=x
        x=F.relu(self.a1_RB_7_conv1(x))
        x=self.a1_RB_7_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_7_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_7_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_7
        #RB_8
        R_8=x
        x=F.relu(self.a1_RB_8_conv1(x))
        x=self.a1_RB_8_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_8_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_8_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_8
        #RB_9
        R_9=x
        x=F.relu(self.a1_RB_9_conv1(x))
        x=self.a1_RB_9_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_9_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_9_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_9
        #RB_10
        R_10=x
        x=F.relu(self.a1_RB_10_conv1(x))
        x=self.a1_RB_10_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_10_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_10_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_10
        
        #RB_11
        R_11=x
        x=F.relu(self.a1_RB_11_conv1(x))
        x=self.a1_RB_11_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_11_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_11_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_11
        #RB_12
        R_12=x
        x=F.relu(self.a1_RB_12_conv1(x))
        x=self.a1_RB_12_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_12_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_12_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_12
        #RB_13
        R_13=x
        x=F.relu(self.a1_RB_13_conv1(x))
        x=self.a1_RB_13_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_13_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_13_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_13
        #RB_14
        R_14=x
        x=F.relu(self.a1_RB_14_conv1(x))
        x=self.a1_RB_14_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_14_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_14_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_14
        #RB_15
        R_15=x
        x=F.relu(self.a1_RB_15_conv1(x))
        x=self.a1_RB_15_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_15_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_15_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_15
        #RB_16
        R_16=x
        x=F.relu(self.a1_RB_16_conv1(x))
        x=self.a1_RB_16_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a1_RB_16_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a1_RB_16_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_16     
        #end:
        x=self.a1_end_RB(x)
        x=self.a1_toR(x)
        x+=LR
        x[x < 0.0] = 0.0
        x[x>1.0]=1.0
        ###########################################
        LR=x
        x=self.a2_int(x)
        #RB_1
        R_1=x
        x=F.relu(self.a2_RB_1_conv1(x))
        x=self.a2_RB_1_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_1_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_1_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_1
        #RB_2
        R_2=x
        x=F.relu(self.a2_RB_2_conv1(x))
        x=self.a2_RB_2_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_2_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_2_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_2
        #RB_3
        R_3=x
        x=F.relu(self.a2_RB_3_conv1(x))
        x=self.a2_RB_3_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_3_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_3_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_3
        #RB_4
        R_4=x
        x=F.relu(self.a2_RB_4_conv1(x))
        x=self.a2_RB_4_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_4_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_4_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_4
        #RB_5
        R_5=x
        x=F.relu(self.a2_RB_5_conv1(x))
        x=self.a2_RB_5_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_5_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_5_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_5
        #RB_6
        R_6=x
        x=F.relu(self.a2_RB_6_conv1(x))
        x=self.a2_RB_6_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_6_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_6_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_6
        #RB_7
        R_7=x
        x=F.relu(self.a2_RB_7_conv1(x))
        x=self.a2_RB_7_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_7_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_7_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_7
        #RB_8
        R_8=x
        x=F.relu(self.a2_RB_8_conv1(x))
        x=self.a2_RB_8_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_8_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_8_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_8
        #RB_9
        R_9=x
        x=F.relu(self.a2_RB_9_conv1(x))
        x=self.a2_RB_9_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_9_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_9_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_9
        #RB_10
        R_10=x
        x=F.relu(self.a2_RB_10_conv1(x))
        x=self.a2_RB_10_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_10_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_10_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_10
        
        #RB_11
        R_11=x
        x=F.relu(self.a2_RB_11_conv1(x))
        x=self.a2_RB_11_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_11_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_11_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_11
        #RB_12
        R_12=x
        x=F.relu(self.a2_RB_12_conv1(x))
        x=self.a2_RB_12_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_12_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_12_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_12
        #RB_13
        R_13=x
        x=F.relu(self.a2_RB_13_conv1(x))
        x=self.a2_RB_13_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_13_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_13_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_13
        #RB_14
        R_14=x
        x=F.relu(self.a2_RB_14_conv1(x))
        x=self.a2_RB_14_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_14_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_14_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_14
        #RB_15
        R_15=x
        x=F.relu(self.a2_RB_15_conv1(x))
        x=self.a2_RB_15_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_15_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_15_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_15
        #RB_16
        R_16=x
        x=F.relu(self.a2_RB_16_conv1(x))
        x=self.a2_RB_16_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a2_RB_16_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a2_RB_16_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_16     
        #end:
        x=self.a2_end_RB(x)
        x=self.a2_toR(x)
        x+=LR
        x[x < 0.0] = 0.0
        x[x>1.0]=1.0
        #######################################
        LR=x
        x=self.a3_int(x)
        #RB_1
        R_1=x
        x=F.relu(self.a3_RB_1_conv1(x))
        x=self.a3_RB_1_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_1_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_1_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_1
        #RB_2
        R_2=x
        x=F.relu(self.a3_RB_2_conv1(x))
        x=self.a3_RB_2_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_2_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_2_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_2
        #RB_3
        R_3=x
        x=F.relu(self.a3_RB_3_conv1(x))
        x=self.a3_RB_3_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_3_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_3_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_3
        #RB_4
        R_4=x
        x=F.relu(self.a3_RB_4_conv1(x))
        x=self.a3_RB_4_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_4_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_4_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_4
        #RB_5
        R_5=x
        x=F.relu(self.a3_RB_5_conv1(x))
        x=self.a3_RB_5_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_5_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_5_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_5
        #RB_6
        R_6=x
        x=F.relu(self.a3_RB_6_conv1(x))
        x=self.a3_RB_6_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_6_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_6_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_6
        #RB_7
        R_7=x
        x=F.relu(self.a3_RB_7_conv1(x))
        x=self.a3_RB_7_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_7_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_7_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_7
        #RB_8
        R_8=x
        x=F.relu(self.a3_RB_8_conv1(x))
        x=self.a3_RB_8_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_8_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_8_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_8
        #RB_9
        R_9=x
        x=F.relu(self.a3_RB_9_conv1(x))
        x=self.a3_RB_9_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_9_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_9_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_9
        #RB_10
        R_10=x
        x=F.relu(self.a3_RB_10_conv1(x))
        x=self.a3_RB_10_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_10_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_10_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_10
        
        #RB_11
        R_11=x
        x=F.relu(self.a3_RB_11_conv1(x))
        x=self.a3_RB_11_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_11_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_11_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_11
        #RB_12
        R_12=x
        x=F.relu(self.a3_RB_12_conv1(x))
        x=self.a3_RB_12_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_12_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_12_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_12
        #RB_13
        R_13=x
        x=F.relu(self.a3_RB_13_conv1(x))
        x=self.a3_RB_13_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_13_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_13_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_13
        #RB_14
        R_14=x
        x=F.relu(self.a3_RB_14_conv1(x))
        x=self.a3_RB_14_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_14_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_14_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_14
        #RB_15
        R_15=x
        x=F.relu(self.a3_RB_15_conv1(x))
        x=self.a3_RB_15_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_15_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_15_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_15
        #RB_16
        R_16=x
        x=F.relu(self.a3_RB_16_conv1(x))
        x=self.a3_RB_16_conv2(x)
        ca=self.pooling(x)
        ca=F.relu(self.a3_RB_16_1d1(ca.squeeze(2)))
        ca=torch.sigmoid(self.a3_RB_16_1d2(ca))
        x=x*ca.unsqueeze(3)
        x+=R_16     
        #end:
        x=self.a3_end_RB(x)
        x=self.a3_toR(x)
        x+=LR
        x[x < 0.0] = 0.0
        x[x>1.0]=1.0
        return x

net_combine=Net_combine()
    
net_plus=Net_plus()
#net_plus.load_state_dict(torch.load('real_net1_plus.pt'))
#net_plus.eval()

net_combine.a1_int.weight.data=net_plus.int.weight.data
net_combine.a1_int.bias.data=net_plus.int.bias.data
#RB1
net_combine.a1_RB_1_conv1.weight.data=net_plus.RB_1_conv1.weight.data
net_combine.a1_RB_1_conv1.bias.data=net_plus.RB_1_conv1.bias.data
net_combine.a1_RB_1_conv2.weight.data=net_plus.RB_1_conv2.weight.data
net_combine.a1_RB_1_conv2.bias.data=net_plus.RB_1_conv2.bias.data
net_combine.a1_RB_1_1d1.weight.data=net_plus.RB_1_1d1.weight.data
net_combine.a1_RB_1_1d1.bias.data=net_plus.RB_1_1d1.bias.data
net_combine.a1_RB_1_1d2.weight.data=net_plus.RB_1_1d2.weight.data
net_combine.a1_RB_1_1d2.bias.data=net_plus.RB_1_1d2.bias.data
#RB2
net_combine.a1_RB_2_conv1.weight.data=net_plus.RB_2_conv1.weight.data
net_combine.a1_RB_2_conv1.bias.data=net_plus.RB_2_conv1.bias.data
net_combine.a1_RB_2_conv2.weight.data=net_plus.RB_2_conv2.weight.data
net_combine.a1_RB_2_conv2.bias.data=net_plus.RB_2_conv2.bias.data
net_combine.a1_RB_2_1d1.weight.data=net_plus.RB_2_1d1.weight.data
net_combine.a1_RB_2_1d1.bias.data=net_plus.RB_2_1d1.bias.data
net_combine.a1_RB_2_1d2.weight.data=net_plus.RB_2_1d2.weight.data
net_combine.a1_RB_2_1d2.bias.data=net_plus.RB_2_1d2.bias.data
#RB3
net_combine.a1_RB_3_conv1.weight.data=net_plus.RB_3_conv1.weight.data
net_combine.a1_RB_3_conv1.bias.data=net_plus.RB_3_conv1.bias.data
net_combine.a1_RB_3_conv2.weight.data=net_plus.RB_3_conv2.weight.data
net_combine.a1_RB_3_conv2.bias.data=net_plus.RB_3_conv2.bias.data
net_combine.a1_RB_3_1d1.weight.data=net_plus.RB_3_1d1.weight.data
net_combine.a1_RB_3_1d1.bias.data=net_plus.RB_3_1d1.bias.data
net_combine.a1_RB_3_1d2.weight.data=net_plus.RB_3_1d2.weight.data
net_combine.a1_RB_3_1d2.bias.data=net_plus.RB_3_1d2.bias.data
#RB4
net_combine.a1_RB_4_conv1.weight.data=net_plus.RB_4_conv1.weight.data
net_combine.a1_RB_4_conv1.bias.data=net_plus.RB_4_conv1.bias.data
net_combine.a1_RB_4_conv2.weight.data=net_plus.RB_4_conv2.weight.data
net_combine.a1_RB_4_conv2.bias.data=net_plus.RB_4_conv2.bias.data
net_combine.a1_RB_4_1d1.weight.data=net_plus.RB_4_1d1.weight.data
net_combine.a1_RB_4_1d1.bias.data=net_plus.RB_4_1d1.bias.data
net_combine.a1_RB_4_1d2.weight.data=net_plus.RB_4_1d2.weight.data
net_combine.a1_RB_4_1d2.bias.data=net_plus.RB_4_1d2.bias.data
#RB5
net_combine.a1_RB_5_conv1.weight.data=net_plus.RB_5_conv1.weight.data
net_combine.a1_RB_5_conv1.bias.data=net_plus.RB_5_conv1.bias.data
net_combine.a1_RB_5_conv2.weight.data=net_plus.RB_5_conv2.weight.data
net_combine.a1_RB_5_conv2.bias.data=net_plus.RB_5_conv2.bias.data
net_combine.a1_RB_5_1d1.weight.data=net_plus.RB_5_1d1.weight.data
net_combine.a1_RB_5_1d1.bias.data=net_plus.RB_5_1d1.bias.data
net_combine.a1_RB_5_1d2.weight.data=net_plus.RB_5_1d2.weight.data
net_combine.a1_RB_5_1d2.bias.data=net_plus.RB_5_1d2.bias.data
#RB6
net_combine.a1_RB_6_conv1.weight.data=net_plus.RB_6_conv1.weight.data
net_combine.a1_RB_6_conv1.bias.data=net_plus.RB_6_conv1.bias.data
net_combine.a1_RB_6_conv2.weight.data=net_plus.RB_6_conv2.weight.data
net_combine.a1_RB_6_conv2.bias.data=net_plus.RB_6_conv2.bias.data
net_combine.a1_RB_6_1d1.weight.data=net_plus.RB_6_1d1.weight.data
net_combine.a1_RB_6_1d1.bias.data=net_plus.RB_6_1d1.bias.data
net_combine.a1_RB_6_1d2.weight.data=net_plus.RB_6_1d2.weight.data
net_combine.a1_RB_6_1d2.bias.data=net_plus.RB_6_1d2.bias.data
#RB7
net_combine.a1_RB_7_conv1.weight.data=net_plus.RB_7_conv1.weight.data
net_combine.a1_RB_7_conv1.bias.data=net_plus.RB_7_conv1.bias.data
net_combine.a1_RB_7_conv2.weight.data=net_plus.RB_7_conv2.weight.data
net_combine.a1_RB_7_conv2.bias.data=net_plus.RB_7_conv2.bias.data
net_combine.a1_RB_7_1d1.weight.data=net_plus.RB_7_1d1.weight.data
net_combine.a1_RB_7_1d1.bias.data=net_plus.RB_7_1d1.bias.data
net_combine.a1_RB_7_1d2.weight.data=net_plus.RB_7_1d2.weight.data
net_combine.a1_RB_7_1d2.bias.data=net_plus.RB_7_1d2.bias.data
#RB8
net_combine.a1_RB_8_conv1.weight.data=net_plus.RB_8_conv1.weight.data
net_combine.a1_RB_8_conv1.bias.data=net_plus.RB_8_conv1.bias.data
net_combine.a1_RB_8_conv2.weight.data=net_plus.RB_8_conv2.weight.data
net_combine.a1_RB_8_conv2.bias.data=net_plus.RB_8_conv2.bias.data
net_combine.a1_RB_8_1d1.weight.data=net_plus.RB_8_1d1.weight.data
net_combine.a1_RB_8_1d1.bias.data=net_plus.RB_8_1d1.bias.data
net_combine.a1_RB_8_1d2.weight.data=net_plus.RB_8_1d2.weight.data
net_combine.a1_RB_8_1d2.bias.data=net_plus.RB_8_1d2.bias.data
#RB9
net_combine.a1_RB_9_conv1.weight.data=net_plus.RB_9_conv1.weight.data
net_combine.a1_RB_9_conv1.bias.data=net_plus.RB_9_conv1.bias.data
net_combine.a1_RB_9_conv2.weight.data=net_plus.RB_9_conv2.weight.data
net_combine.a1_RB_9_conv2.bias.data=net_plus.RB_9_conv2.bias.data
net_combine.a1_RB_9_1d1.weight.data=net_plus.RB_9_1d1.weight.data
net_combine.a1_RB_9_1d1.bias.data=net_plus.RB_9_1d1.bias.data
net_combine.a1_RB_9_1d2.weight.data=net_plus.RB_9_1d2.weight.data
net_combine.a1_RB_9_1d2.bias.data=net_plus.RB_9_1d2.bias.data
#RB10
net_combine.a1_RB_10_conv1.weight.data=net_plus.RB_10_conv1.weight.data
net_combine.a1_RB_10_conv1.bias.data=net_plus.RB_10_conv1.bias.data
net_combine.a1_RB_10_conv2.weight.data=net_plus.RB_10_conv2.weight.data
net_combine.a1_RB_10_conv2.bias.data=net_plus.RB_10_conv2.bias.data
net_combine.a1_RB_10_1d1.weight.data=net_plus.RB_10_1d1.weight.data
net_combine.a1_RB_10_1d1.bias.data=net_plus.RB_10_1d1.bias.data
net_combine.a1_RB_10_1d2.weight.data=net_plus.RB_10_1d2.weight.data
net_combine.a1_RB_10_1d2.bias.data=net_plus.RB_10_1d2.bias.data
#RB11
net_combine.a1_RB_11_conv1.weight.data=net_plus.RB_11_conv1.weight.data
net_combine.a1_RB_11_conv1.bias.data=net_plus.RB_11_conv1.bias.data
net_combine.a1_RB_11_conv2.weight.data=net_plus.RB_11_conv2.weight.data
net_combine.a1_RB_11_conv2.bias.data=net_plus.RB_11_conv2.bias.data
net_combine.a1_RB_11_1d1.weight.data=net_plus.RB_11_1d1.weight.data
net_combine.a1_RB_11_1d1.bias.data=net_plus.RB_11_1d1.bias.data
net_combine.a1_RB_11_1d2.weight.data=net_plus.RB_11_1d2.weight.data
net_combine.a1_RB_11_1d2.bias.data=net_plus.RB_11_1d2.bias.data
#RB12
net_combine.a1_RB_12_conv1.weight.data=net_plus.RB_12_conv1.weight.data
net_combine.a1_RB_12_conv1.bias.data=net_plus.RB_12_conv1.bias.data
net_combine.a1_RB_12_conv2.weight.data=net_plus.RB_12_conv2.weight.data
net_combine.a1_RB_12_conv2.bias.data=net_plus.RB_12_conv2.bias.data
net_combine.a1_RB_12_1d1.weight.data=net_plus.RB_12_1d1.weight.data
net_combine.a1_RB_12_1d1.bias.data=net_plus.RB_12_1d1.bias.data
net_combine.a1_RB_12_1d2.weight.data=net_plus.RB_12_1d2.weight.data
net_combine.a1_RB_12_1d2.bias.data=net_plus.RB_12_1d2.bias.data
#RB13
net_combine.a1_RB_13_conv1.weight.data=net_plus.RB_13_conv1.weight.data
net_combine.a1_RB_13_conv1.bias.data=net_plus.RB_13_conv1.bias.data
net_combine.a1_RB_13_conv2.weight.data=net_plus.RB_13_conv2.weight.data
net_combine.a1_RB_13_conv2.bias.data=net_plus.RB_13_conv2.bias.data
net_combine.a1_RB_13_1d1.weight.data=net_plus.RB_13_1d1.weight.data
net_combine.a1_RB_13_1d1.bias.data=net_plus.RB_13_1d1.bias.data
net_combine.a1_RB_13_1d2.weight.data=net_plus.RB_13_1d2.weight.data
net_combine.a1_RB_13_1d2.bias.data=net_plus.RB_13_1d2.bias.data
#RB14
net_combine.a1_RB_14_conv1.weight.data=net_plus.RB_14_conv1.weight.data
net_combine.a1_RB_14_conv1.bias.data=net_plus.RB_14_conv1.bias.data
net_combine.a1_RB_14_conv2.weight.data=net_plus.RB_14_conv2.weight.data
net_combine.a1_RB_14_conv2.bias.data=net_plus.RB_14_conv2.bias.data
net_combine.a1_RB_14_1d1.weight.data=net_plus.RB_14_1d1.weight.data
net_combine.a1_RB_14_1d1.bias.data=net_plus.RB_14_1d1.bias.data
net_combine.a1_RB_14_1d2.weight.data=net_plus.RB_14_1d2.weight.data
net_combine.a1_RB_14_1d2.bias.data=net_plus.RB_14_1d2.bias.data
#RB15
net_combine.a1_RB_15_conv1.weight.data=net_plus.RB_15_conv1.weight.data
net_combine.a1_RB_15_conv1.bias.data=net_plus.RB_15_conv1.bias.data
net_combine.a1_RB_15_conv2.weight.data=net_plus.RB_15_conv2.weight.data
net_combine.a1_RB_15_conv2.bias.data=net_plus.RB_15_conv2.bias.data
net_combine.a1_RB_15_1d1.weight.data=net_plus.RB_15_1d1.weight.data
net_combine.a1_RB_15_1d1.bias.data=net_plus.RB_15_1d1.bias.data
net_combine.a1_RB_15_1d2.weight.data=net_plus.RB_15_1d2.weight.data
net_combine.a1_RB_15_1d2.bias.data=net_plus.RB_15_1d2.bias.data
#RB16
net_combine.a1_RB_16_conv1.weight.data=net_plus.RB_16_conv1.weight.data
net_combine.a1_RB_16_conv1.bias.data=net_plus.RB_16_conv1.bias.data
net_combine.a1_RB_16_conv2.weight.data=net_plus.RB_16_conv2.weight.data
net_combine.a1_RB_16_conv2.bias.data=net_plus.RB_16_conv2.bias.data
net_combine.a1_RB_16_1d1.weight.data=net_plus.RB_16_1d1.weight.data
net_combine.a1_RB_16_1d1.bias.data=net_plus.RB_16_1d1.bias.data
net_combine.a1_RB_16_1d2.weight.data=net_plus.RB_16_1d2.weight.data
net_combine.a1_RB_16_1d2.bias.data=net_plus.RB_16_1d2.bias.data



del net_plus






net_plus=Net_plus()
#net_plus.load_state_dict(torch.load('real_net2_plus.pt'))
#net_plus.eval()

net_combine.a2_int.weight.data=net_plus.int.weight.data
net_combine.a2_int.bias.data=net_plus.int.bias.data
#RB1
net_combine.a2_RB_1_conv1.weight.data=net_plus.RB_1_conv1.weight.data
net_combine.a2_RB_1_conv1.bias.data=net_plus.RB_1_conv1.bias.data
net_combine.a2_RB_1_conv2.weight.data=net_plus.RB_1_conv2.weight.data
net_combine.a2_RB_1_conv2.bias.data=net_plus.RB_1_conv2.bias.data
net_combine.a2_RB_1_1d1.weight.data=net_plus.RB_1_1d1.weight.data
net_combine.a2_RB_1_1d1.bias.data=net_plus.RB_1_1d1.bias.data
net_combine.a2_RB_1_1d2.weight.data=net_plus.RB_1_1d2.weight.data
net_combine.a2_RB_1_1d2.bias.data=net_plus.RB_1_1d2.bias.data
#RB2
net_combine.a2_RB_2_conv1.weight.data=net_plus.RB_2_conv1.weight.data
net_combine.a2_RB_2_conv1.bias.data=net_plus.RB_2_conv1.bias.data
net_combine.a2_RB_2_conv2.weight.data=net_plus.RB_2_conv2.weight.data
net_combine.a2_RB_2_conv2.bias.data=net_plus.RB_2_conv2.bias.data
net_combine.a2_RB_2_1d1.weight.data=net_plus.RB_2_1d1.weight.data
net_combine.a2_RB_2_1d1.bias.data=net_plus.RB_2_1d1.bias.data
net_combine.a2_RB_2_1d2.weight.data=net_plus.RB_2_1d2.weight.data
net_combine.a2_RB_2_1d2.bias.data=net_plus.RB_2_1d2.bias.data
#RB3
net_combine.a2_RB_3_conv1.weight.data=net_plus.RB_3_conv1.weight.data
net_combine.a2_RB_3_conv1.bias.data=net_plus.RB_3_conv1.bias.data
net_combine.a2_RB_3_conv2.weight.data=net_plus.RB_3_conv2.weight.data
net_combine.a2_RB_3_conv2.bias.data=net_plus.RB_3_conv2.bias.data
net_combine.a2_RB_3_1d1.weight.data=net_plus.RB_3_1d1.weight.data
net_combine.a2_RB_3_1d1.bias.data=net_plus.RB_3_1d1.bias.data
net_combine.a2_RB_3_1d2.weight.data=net_plus.RB_3_1d2.weight.data
net_combine.a2_RB_3_1d2.bias.data=net_plus.RB_3_1d2.bias.data
#RB4
net_combine.a2_RB_4_conv1.weight.data=net_plus.RB_4_conv1.weight.data
net_combine.a2_RB_4_conv1.bias.data=net_plus.RB_4_conv1.bias.data
net_combine.a2_RB_4_conv2.weight.data=net_plus.RB_4_conv2.weight.data
net_combine.a2_RB_4_conv2.bias.data=net_plus.RB_4_conv2.bias.data
net_combine.a2_RB_4_1d1.weight.data=net_plus.RB_4_1d1.weight.data
net_combine.a2_RB_4_1d1.bias.data=net_plus.RB_4_1d1.bias.data
net_combine.a2_RB_4_1d2.weight.data=net_plus.RB_4_1d2.weight.data
net_combine.a2_RB_4_1d2.bias.data=net_plus.RB_4_1d2.bias.data
#RB5
net_combine.a2_RB_5_conv1.weight.data=net_plus.RB_5_conv1.weight.data
net_combine.a2_RB_5_conv1.bias.data=net_plus.RB_5_conv1.bias.data
net_combine.a2_RB_5_conv2.weight.data=net_plus.RB_5_conv2.weight.data
net_combine.a2_RB_5_conv2.bias.data=net_plus.RB_5_conv2.bias.data
net_combine.a2_RB_5_1d1.weight.data=net_plus.RB_5_1d1.weight.data
net_combine.a2_RB_5_1d1.bias.data=net_plus.RB_5_1d1.bias.data
net_combine.a2_RB_5_1d2.weight.data=net_plus.RB_5_1d2.weight.data
net_combine.a2_RB_5_1d2.bias.data=net_plus.RB_5_1d2.bias.data
#RB6
net_combine.a2_RB_6_conv1.weight.data=net_plus.RB_6_conv1.weight.data
net_combine.a2_RB_6_conv1.bias.data=net_plus.RB_6_conv1.bias.data
net_combine.a2_RB_6_conv2.weight.data=net_plus.RB_6_conv2.weight.data
net_combine.a2_RB_6_conv2.bias.data=net_plus.RB_6_conv2.bias.data
net_combine.a2_RB_6_1d1.weight.data=net_plus.RB_6_1d1.weight.data
net_combine.a2_RB_6_1d1.bias.data=net_plus.RB_6_1d1.bias.data
net_combine.a2_RB_6_1d2.weight.data=net_plus.RB_6_1d2.weight.data
net_combine.a2_RB_6_1d2.bias.data=net_plus.RB_6_1d2.bias.data
#RB7
net_combine.a2_RB_7_conv1.weight.data=net_plus.RB_7_conv1.weight.data
net_combine.a2_RB_7_conv1.bias.data=net_plus.RB_7_conv1.bias.data
net_combine.a2_RB_7_conv2.weight.data=net_plus.RB_7_conv2.weight.data
net_combine.a2_RB_7_conv2.bias.data=net_plus.RB_7_conv2.bias.data
net_combine.a2_RB_7_1d1.weight.data=net_plus.RB_7_1d1.weight.data
net_combine.a2_RB_7_1d1.bias.data=net_plus.RB_7_1d1.bias.data
net_combine.a2_RB_7_1d2.weight.data=net_plus.RB_7_1d2.weight.data
net_combine.a2_RB_7_1d2.bias.data=net_plus.RB_7_1d2.bias.data
#RB8
net_combine.a2_RB_8_conv1.weight.data=net_plus.RB_8_conv1.weight.data
net_combine.a2_RB_8_conv1.bias.data=net_plus.RB_8_conv1.bias.data
net_combine.a2_RB_8_conv2.weight.data=net_plus.RB_8_conv2.weight.data
net_combine.a2_RB_8_conv2.bias.data=net_plus.RB_8_conv2.bias.data
net_combine.a2_RB_8_1d1.weight.data=net_plus.RB_8_1d1.weight.data
net_combine.a2_RB_8_1d1.bias.data=net_plus.RB_8_1d1.bias.data
net_combine.a2_RB_8_1d2.weight.data=net_plus.RB_8_1d2.weight.data
net_combine.a2_RB_8_1d2.bias.data=net_plus.RB_8_1d2.bias.data
#RB9
net_combine.a2_RB_9_conv1.weight.data=net_plus.RB_9_conv1.weight.data
net_combine.a2_RB_9_conv1.bias.data=net_plus.RB_9_conv1.bias.data
net_combine.a2_RB_9_conv2.weight.data=net_plus.RB_9_conv2.weight.data
net_combine.a2_RB_9_conv2.bias.data=net_plus.RB_9_conv2.bias.data
net_combine.a2_RB_9_1d1.weight.data=net_plus.RB_9_1d1.weight.data
net_combine.a2_RB_9_1d1.bias.data=net_plus.RB_9_1d1.bias.data
net_combine.a2_RB_9_1d2.weight.data=net_plus.RB_9_1d2.weight.data
net_combine.a2_RB_9_1d2.bias.data=net_plus.RB_9_1d2.bias.data
#RB10
net_combine.a2_RB_10_conv1.weight.data=net_plus.RB_10_conv1.weight.data
net_combine.a2_RB_10_conv1.bias.data=net_plus.RB_10_conv1.bias.data
net_combine.a2_RB_10_conv2.weight.data=net_plus.RB_10_conv2.weight.data
net_combine.a2_RB_10_conv2.bias.data=net_plus.RB_10_conv2.bias.data
net_combine.a2_RB_10_1d1.weight.data=net_plus.RB_10_1d1.weight.data
net_combine.a2_RB_10_1d1.bias.data=net_plus.RB_10_1d1.bias.data
net_combine.a2_RB_10_1d2.weight.data=net_plus.RB_10_1d2.weight.data
net_combine.a2_RB_10_1d2.bias.data=net_plus.RB_10_1d2.bias.data
#RB11
net_combine.a2_RB_11_conv1.weight.data=net_plus.RB_11_conv1.weight.data
net_combine.a2_RB_11_conv1.bias.data=net_plus.RB_11_conv1.bias.data
net_combine.a2_RB_11_conv2.weight.data=net_plus.RB_11_conv2.weight.data
net_combine.a2_RB_11_conv2.bias.data=net_plus.RB_11_conv2.bias.data
net_combine.a2_RB_11_1d1.weight.data=net_plus.RB_11_1d1.weight.data
net_combine.a2_RB_11_1d1.bias.data=net_plus.RB_11_1d1.bias.data
net_combine.a2_RB_11_1d2.weight.data=net_plus.RB_11_1d2.weight.data
net_combine.a2_RB_11_1d2.bias.data=net_plus.RB_11_1d2.bias.data
#RB12
net_combine.a2_RB_12_conv1.weight.data=net_plus.RB_12_conv1.weight.data
net_combine.a2_RB_12_conv1.bias.data=net_plus.RB_12_conv1.bias.data
net_combine.a2_RB_12_conv2.weight.data=net_plus.RB_12_conv2.weight.data
net_combine.a2_RB_12_conv2.bias.data=net_plus.RB_12_conv2.bias.data
net_combine.a2_RB_12_1d1.weight.data=net_plus.RB_12_1d1.weight.data
net_combine.a2_RB_12_1d1.bias.data=net_plus.RB_12_1d1.bias.data
net_combine.a2_RB_12_1d2.weight.data=net_plus.RB_12_1d2.weight.data
net_combine.a2_RB_12_1d2.bias.data=net_plus.RB_12_1d2.bias.data
#RB13
net_combine.a2_RB_13_conv1.weight.data=net_plus.RB_13_conv1.weight.data
net_combine.a2_RB_13_conv1.bias.data=net_plus.RB_13_conv1.bias.data
net_combine.a2_RB_13_conv2.weight.data=net_plus.RB_13_conv2.weight.data
net_combine.a2_RB_13_conv2.bias.data=net_plus.RB_13_conv2.bias.data
net_combine.a2_RB_13_1d1.weight.data=net_plus.RB_13_1d1.weight.data
net_combine.a2_RB_13_1d1.bias.data=net_plus.RB_13_1d1.bias.data
net_combine.a2_RB_13_1d2.weight.data=net_plus.RB_13_1d2.weight.data
net_combine.a2_RB_13_1d2.bias.data=net_plus.RB_13_1d2.bias.data
#RB14
net_combine.a2_RB_14_conv1.weight.data=net_plus.RB_14_conv1.weight.data
net_combine.a2_RB_14_conv1.bias.data=net_plus.RB_14_conv1.bias.data
net_combine.a2_RB_14_conv2.weight.data=net_plus.RB_14_conv2.weight.data
net_combine.a2_RB_14_conv2.bias.data=net_plus.RB_14_conv2.bias.data
net_combine.a2_RB_14_1d1.weight.data=net_plus.RB_14_1d1.weight.data
net_combine.a2_RB_14_1d1.bias.data=net_plus.RB_14_1d1.bias.data
net_combine.a2_RB_14_1d2.weight.data=net_plus.RB_14_1d2.weight.data
net_combine.a2_RB_14_1d2.bias.data=net_plus.RB_14_1d2.bias.data
#RB15
net_combine.a2_RB_15_conv1.weight.data=net_plus.RB_15_conv1.weight.data
net_combine.a2_RB_15_conv1.bias.data=net_plus.RB_15_conv1.bias.data
net_combine.a2_RB_15_conv2.weight.data=net_plus.RB_15_conv2.weight.data
net_combine.a2_RB_15_conv2.bias.data=net_plus.RB_15_conv2.bias.data
net_combine.a2_RB_15_1d1.weight.data=net_plus.RB_15_1d1.weight.data
net_combine.a2_RB_15_1d1.bias.data=net_plus.RB_15_1d1.bias.data
net_combine.a2_RB_15_1d2.weight.data=net_plus.RB_15_1d2.weight.data
net_combine.a2_RB_15_1d2.bias.data=net_plus.RB_15_1d2.bias.data
#RB16
net_combine.a2_RB_16_conv1.weight.data=net_plus.RB_16_conv1.weight.data
net_combine.a2_RB_16_conv1.bias.data=net_plus.RB_16_conv1.bias.data
net_combine.a2_RB_16_conv2.weight.data=net_plus.RB_16_conv2.weight.data
net_combine.a2_RB_16_conv2.bias.data=net_plus.RB_16_conv2.bias.data
net_combine.a2_RB_16_1d1.weight.data=net_plus.RB_16_1d1.weight.data
net_combine.a2_RB_16_1d1.bias.data=net_plus.RB_16_1d1.bias.data
net_combine.a2_RB_16_1d2.weight.data=net_plus.RB_16_1d2.weight.data
net_combine.a2_RB_16_1d2.bias.data=net_plus.RB_16_1d2.bias.data



del net_plus

net_plus=Net_plus()
#net_plus.load_state_dict(torch.load('real_net3_plus.pt'))
#net_plus.eval()

net_combine.a3_int.weight.data=net_plus.int.weight.data
net_combine.a3_int.bias.data=net_plus.int.bias.data
#RB1
net_combine.a3_RB_1_conv1.weight.data=net_plus.RB_1_conv1.weight.data
net_combine.a3_RB_1_conv1.bias.data=net_plus.RB_1_conv1.bias.data
net_combine.a3_RB_1_conv2.weight.data=net_plus.RB_1_conv2.weight.data
net_combine.a3_RB_1_conv2.bias.data=net_plus.RB_1_conv2.bias.data
net_combine.a3_RB_1_1d1.weight.data=net_plus.RB_1_1d1.weight.data
net_combine.a3_RB_1_1d1.bias.data=net_plus.RB_1_1d1.bias.data
net_combine.a3_RB_1_1d2.weight.data=net_plus.RB_1_1d2.weight.data
net_combine.a3_RB_1_1d2.bias.data=net_plus.RB_1_1d2.bias.data
#RB2
net_combine.a3_RB_2_conv1.weight.data=net_plus.RB_2_conv1.weight.data
net_combine.a3_RB_2_conv1.bias.data=net_plus.RB_2_conv1.bias.data
net_combine.a3_RB_2_conv2.weight.data=net_plus.RB_2_conv2.weight.data
net_combine.a3_RB_2_conv2.bias.data=net_plus.RB_2_conv2.bias.data
net_combine.a3_RB_2_1d1.weight.data=net_plus.RB_2_1d1.weight.data
net_combine.a3_RB_2_1d1.bias.data=net_plus.RB_2_1d1.bias.data
net_combine.a3_RB_2_1d2.weight.data=net_plus.RB_2_1d2.weight.data
net_combine.a3_RB_2_1d2.bias.data=net_plus.RB_2_1d2.bias.data
#RB3
net_combine.a3_RB_3_conv1.weight.data=net_plus.RB_3_conv1.weight.data
net_combine.a3_RB_3_conv1.bias.data=net_plus.RB_3_conv1.bias.data
net_combine.a3_RB_3_conv2.weight.data=net_plus.RB_3_conv2.weight.data
net_combine.a3_RB_3_conv2.bias.data=net_plus.RB_3_conv2.bias.data
net_combine.a3_RB_3_1d1.weight.data=net_plus.RB_3_1d1.weight.data
net_combine.a3_RB_3_1d1.bias.data=net_plus.RB_3_1d1.bias.data
net_combine.a3_RB_3_1d2.weight.data=net_plus.RB_3_1d2.weight.data
net_combine.a3_RB_3_1d2.bias.data=net_plus.RB_3_1d2.bias.data
#RB4
net_combine.a3_RB_4_conv1.weight.data=net_plus.RB_4_conv1.weight.data
net_combine.a3_RB_4_conv1.bias.data=net_plus.RB_4_conv1.bias.data
net_combine.a3_RB_4_conv2.weight.data=net_plus.RB_4_conv2.weight.data
net_combine.a3_RB_4_conv2.bias.data=net_plus.RB_4_conv2.bias.data
net_combine.a3_RB_4_1d1.weight.data=net_plus.RB_4_1d1.weight.data
net_combine.a3_RB_4_1d1.bias.data=net_plus.RB_4_1d1.bias.data
net_combine.a3_RB_4_1d2.weight.data=net_plus.RB_4_1d2.weight.data
net_combine.a3_RB_4_1d2.bias.data=net_plus.RB_4_1d2.bias.data
#RB5
net_combine.a3_RB_5_conv1.weight.data=net_plus.RB_5_conv1.weight.data
net_combine.a3_RB_5_conv1.bias.data=net_plus.RB_5_conv1.bias.data
net_combine.a3_RB_5_conv2.weight.data=net_plus.RB_5_conv2.weight.data
net_combine.a3_RB_5_conv2.bias.data=net_plus.RB_5_conv2.bias.data
net_combine.a3_RB_5_1d1.weight.data=net_plus.RB_5_1d1.weight.data
net_combine.a3_RB_5_1d1.bias.data=net_plus.RB_5_1d1.bias.data
net_combine.a3_RB_5_1d2.weight.data=net_plus.RB_5_1d2.weight.data
net_combine.a3_RB_5_1d2.bias.data=net_plus.RB_5_1d2.bias.data
#RB6
net_combine.a3_RB_6_conv1.weight.data=net_plus.RB_6_conv1.weight.data
net_combine.a3_RB_6_conv1.bias.data=net_plus.RB_6_conv1.bias.data
net_combine.a3_RB_6_conv2.weight.data=net_plus.RB_6_conv2.weight.data
net_combine.a3_RB_6_conv2.bias.data=net_plus.RB_6_conv2.bias.data
net_combine.a3_RB_6_1d1.weight.data=net_plus.RB_6_1d1.weight.data
net_combine.a3_RB_6_1d1.bias.data=net_plus.RB_6_1d1.bias.data
net_combine.a3_RB_6_1d2.weight.data=net_plus.RB_6_1d2.weight.data
net_combine.a3_RB_6_1d2.bias.data=net_plus.RB_6_1d2.bias.data
#RB7
net_combine.a3_RB_7_conv1.weight.data=net_plus.RB_7_conv1.weight.data
net_combine.a3_RB_7_conv1.bias.data=net_plus.RB_7_conv1.bias.data
net_combine.a3_RB_7_conv2.weight.data=net_plus.RB_7_conv2.weight.data
net_combine.a3_RB_7_conv2.bias.data=net_plus.RB_7_conv2.bias.data
net_combine.a3_RB_7_1d1.weight.data=net_plus.RB_7_1d1.weight.data
net_combine.a3_RB_7_1d1.bias.data=net_plus.RB_7_1d1.bias.data
net_combine.a3_RB_7_1d2.weight.data=net_plus.RB_7_1d2.weight.data
net_combine.a3_RB_7_1d2.bias.data=net_plus.RB_7_1d2.bias.data
#RB8
net_combine.a3_RB_8_conv1.weight.data=net_plus.RB_8_conv1.weight.data
net_combine.a3_RB_8_conv1.bias.data=net_plus.RB_8_conv1.bias.data
net_combine.a3_RB_8_conv2.weight.data=net_plus.RB_8_conv2.weight.data
net_combine.a3_RB_8_conv2.bias.data=net_plus.RB_8_conv2.bias.data
net_combine.a3_RB_8_1d1.weight.data=net_plus.RB_8_1d1.weight.data
net_combine.a3_RB_8_1d1.bias.data=net_plus.RB_8_1d1.bias.data
net_combine.a3_RB_8_1d2.weight.data=net_plus.RB_8_1d2.weight.data
net_combine.a3_RB_8_1d2.bias.data=net_plus.RB_8_1d2.bias.data
#RB9
net_combine.a3_RB_9_conv1.weight.data=net_plus.RB_9_conv1.weight.data
net_combine.a3_RB_9_conv1.bias.data=net_plus.RB_9_conv1.bias.data
net_combine.a3_RB_9_conv2.weight.data=net_plus.RB_9_conv2.weight.data
net_combine.a3_RB_9_conv2.bias.data=net_plus.RB_9_conv2.bias.data
net_combine.a3_RB_9_1d1.weight.data=net_plus.RB_9_1d1.weight.data
net_combine.a3_RB_9_1d1.bias.data=net_plus.RB_9_1d1.bias.data
net_combine.a3_RB_9_1d2.weight.data=net_plus.RB_9_1d2.weight.data
net_combine.a3_RB_9_1d2.bias.data=net_plus.RB_9_1d2.bias.data
#RB10
net_combine.a3_RB_10_conv1.weight.data=net_plus.RB_10_conv1.weight.data
net_combine.a3_RB_10_conv1.bias.data=net_plus.RB_10_conv1.bias.data
net_combine.a3_RB_10_conv2.weight.data=net_plus.RB_10_conv2.weight.data
net_combine.a3_RB_10_conv2.bias.data=net_plus.RB_10_conv2.bias.data
net_combine.a3_RB_10_1d1.weight.data=net_plus.RB_10_1d1.weight.data
net_combine.a3_RB_10_1d1.bias.data=net_plus.RB_10_1d1.bias.data
net_combine.a3_RB_10_1d2.weight.data=net_plus.RB_10_1d2.weight.data
net_combine.a3_RB_10_1d2.bias.data=net_plus.RB_10_1d2.bias.data
#RB11
net_combine.a3_RB_11_conv1.weight.data=net_plus.RB_11_conv1.weight.data
net_combine.a3_RB_11_conv1.bias.data=net_plus.RB_11_conv1.bias.data
net_combine.a3_RB_11_conv2.weight.data=net_plus.RB_11_conv2.weight.data
net_combine.a3_RB_11_conv2.bias.data=net_plus.RB_11_conv2.bias.data
net_combine.a3_RB_11_1d1.weight.data=net_plus.RB_11_1d1.weight.data
net_combine.a3_RB_11_1d1.bias.data=net_plus.RB_11_1d1.bias.data
net_combine.a3_RB_11_1d2.weight.data=net_plus.RB_11_1d2.weight.data
net_combine.a3_RB_11_1d2.bias.data=net_plus.RB_11_1d2.bias.data
#RB12
net_combine.a3_RB_12_conv1.weight.data=net_plus.RB_12_conv1.weight.data
net_combine.a3_RB_12_conv1.bias.data=net_plus.RB_12_conv1.bias.data
net_combine.a3_RB_12_conv2.weight.data=net_plus.RB_12_conv2.weight.data
net_combine.a3_RB_12_conv2.bias.data=net_plus.RB_12_conv2.bias.data
net_combine.a3_RB_12_1d1.weight.data=net_plus.RB_12_1d1.weight.data
net_combine.a3_RB_12_1d1.bias.data=net_plus.RB_12_1d1.bias.data
net_combine.a3_RB_12_1d2.weight.data=net_plus.RB_12_1d2.weight.data
net_combine.a3_RB_12_1d2.bias.data=net_plus.RB_12_1d2.bias.data
#RB13
net_combine.a3_RB_13_conv1.weight.data=net_plus.RB_13_conv1.weight.data
net_combine.a3_RB_13_conv1.bias.data=net_plus.RB_13_conv1.bias.data
net_combine.a3_RB_13_conv2.weight.data=net_plus.RB_13_conv2.weight.data
net_combine.a3_RB_13_conv2.bias.data=net_plus.RB_13_conv2.bias.data
net_combine.a3_RB_13_1d1.weight.data=net_plus.RB_13_1d1.weight.data
net_combine.a3_RB_13_1d1.bias.data=net_plus.RB_13_1d1.bias.data
net_combine.a3_RB_13_1d2.weight.data=net_plus.RB_13_1d2.weight.data
net_combine.a3_RB_13_1d2.bias.data=net_plus.RB_13_1d2.bias.data
#RB14
net_combine.a3_RB_14_conv1.weight.data=net_plus.RB_14_conv1.weight.data
net_combine.a3_RB_14_conv1.bias.data=net_plus.RB_14_conv1.bias.data
net_combine.a3_RB_14_conv2.weight.data=net_plus.RB_14_conv2.weight.data
net_combine.a3_RB_14_conv2.bias.data=net_plus.RB_14_conv2.bias.data
net_combine.a3_RB_14_1d1.weight.data=net_plus.RB_14_1d1.weight.data
net_combine.a3_RB_14_1d1.bias.data=net_plus.RB_14_1d1.bias.data
net_combine.a3_RB_14_1d2.weight.data=net_plus.RB_14_1d2.weight.data
net_combine.a3_RB_14_1d2.bias.data=net_plus.RB_14_1d2.bias.data
#RB15
net_combine.a3_RB_15_conv1.weight.data=net_plus.RB_15_conv1.weight.data
net_combine.a3_RB_15_conv1.bias.data=net_plus.RB_15_conv1.bias.data
net_combine.a3_RB_15_conv2.weight.data=net_plus.RB_15_conv2.weight.data
net_combine.a3_RB_15_conv2.bias.data=net_plus.RB_15_conv2.bias.data
net_combine.a3_RB_15_1d1.weight.data=net_plus.RB_15_1d1.weight.data
net_combine.a3_RB_15_1d1.bias.data=net_plus.RB_15_1d1.bias.data
net_combine.a3_RB_15_1d2.weight.data=net_plus.RB_15_1d2.weight.data
net_combine.a3_RB_15_1d2.bias.data=net_plus.RB_15_1d2.bias.data
#RB16
net_combine.a3_RB_16_conv1.weight.data=net_plus.RB_16_conv1.weight.data
net_combine.a3_RB_16_conv1.bias.data=net_plus.RB_16_conv1.bias.data
net_combine.a3_RB_16_conv2.weight.data=net_plus.RB_16_conv2.weight.data
net_combine.a3_RB_16_conv2.bias.data=net_plus.RB_16_conv2.bias.data
net_combine.a3_RB_16_1d1.weight.data=net_plus.RB_16_1d1.weight.data
net_combine.a3_RB_16_1d1.bias.data=net_plus.RB_16_1d1.bias.data
net_combine.a3_RB_16_1d2.weight.data=net_plus.RB_16_1d2.weight.data
net_combine.a3_RB_16_1d2.bias.data=net_plus.RB_16_1d2.bias.data

del net_plus

net_combine.load_state_dict(torch.load('net_combine1_test.pt'))
net_combine.eval()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
net_combine.to(device)


p=[]
best=0.0
criterion = nn.L1Loss()
optimizer=torch.optim.Adam(net_combine.parameters(), lr=0.00001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0, amsgrad=False)
for epoch in range(40):
    #running_loss=0.0
    for i in range(500):
        HR,LR=generator()
        HR=HR.to(device)
        LR=LR.to(device)
        optimizer.zero_grad()
        outputs=net_combine(LR)
        Loss=criterion(outputs,HR)
        Loss.backward()
        optimizer.step()
        #running_loss+=Loss.item()
        
        #print('[%d, %5d] loss: %.3f' %
        #     (epoch + 1, i + 1, running_loss))
        #running_loss = 0.0
        del HR,LR,outputs
    n_test=15
    PSNR=0.0
    temp_HR_2=iter(HR_2_test)
    temp_LR_2=iter(LR_2_test)
    with torch.no_grad():
        for t in range(n_test):
            HR_test=temp_HR_2.next()[0].squeeze()
            _,x,y=HR_test.size()
            LR_test=temp_LR_2.next()[0]
            if x>1500:
                x=1500
            if y>1500:
                y=1500
            HR_test=HR_test[:,0:(x-1),0:(y-1)].to(device)
            LR_test=LR_test[:,:,0:(x-1),0:(y-1)].to(device)
            outputs=net_combine(LR_test).data.squeeze()
            PSNR+=psnr(outputs,HR_test)
            del HR_test,LR_test,outputs
    PSNR=PSNR/n_test
    p.append(PSNR)
    print(PSNR)
    if PSNR>best:
        best=PSNR
    print(best)
    del PSNR,n_test,temp_HR_2,temp_LR_2
    torch.save(net_combine.state_dict(), 'net_combine1_test.pt')
print('Finished Training phase1')



