#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import csv
import json 
import shutil
import gzip
from numpy import genfromtxt
from datetime import datetime
import pandas as pd
from datetime import timedelta
from collections import defaultdict


data_folder = '' # Define data filepath(s)
target_folder = '' # Define folder to store clean files


absolute_start_time = time.time()

complete_data = defaultdict(list)

filenames = [os.path.join(dp, f) for dp, dn, filenames in os.walk(data_folder) for f in filenames if f == 'ACC.csv']

for i in range(len(filenames)):
    file = filenames[i]
    path = os.path.normpath(file)
    path_comp=path.split(os.sep)
    name = path_comp[-2]
    df=genfromtxt(file,delimiter=',')
 
    print("File " + str(i+1) + " out of " + str(len(filenames)) + ' (' + file + ')') 
    line={}
    samplingrate=0
    for r in range(len(df)):  
        data =df[r]
        if r==0:
            Timestamp = datetime.fromtimestamp(data[0])
        elif r==1:
            samplingrate = data[0]
        else:
            Timestamp = Timestamp + timedelta(milliseconds=1000/samplingrate)
            line["Timestamp"]=Timestamp
            line["X"]=data[0]
            line["Y"]=data[1]
            line["Z"]=data[2]
            complete_data[name].append(line.copy())
    with open(os.path.join(target_folder,'ACC_'+name+'.csv'),'w') as f:
        #print(f)
        writer = csv.DictWriter(f, fieldnames=complete_data[name][0].keys(),lineterminator='\n')
        writer.writeheader()
        writer.writerows(complete_data[name])
        f.close()

sensors=['EDA','BVP','HR','IBI','TEMP']
for key in sensors:    
    absolute_start_time = time.time()
    
    complete_data = defaultdict(list)
    
    filenames = [os.path.join(dp, f) for dp, dn, filenames in os.walk(data_folder) for f in filenames if f == key+'.csv']
    
    for i in range(len(filenames)):
        file = filenames[i]
        path = os.path.normpath(file)
        path_comp=path.split(os.sep)
        name = path_comp[-2]
        df=genfromtxt(file,delimiter=',')
     
        print("File " + str(i+1) + " out of " + str(len(filenames)) + ' (' + file + ')') 
        line={}
        samplingrate=0
        for r in range(len(df)):  
            data =df[r]
            if r==0:
                print(data, ' ' , r)
                if key=='IBI':
                    Timestamp = datetime.fromtimestamp(data[0])
                else:
                    Timestamp = datetime.fromtimestamp(data)
            else: #ignore sampling rate
                if key=='IBI':
                    Timestamp = Timestamp + timedelta(seconds=data[0])
                    line[key]=data[0]
                    line["Timestamp"]=Timestamp
                    complete_data[name].append(line.copy())
                else:
                    if  r==1:
                        samplingrate = data
                    else:
                        Timestamp = Timestamp + timedelta(milliseconds=1000/samplingrate)
                        line[key]=data
                        line["Timestamp"]=Timestamp
                        complete_data[name].append(line.copy())
                
        with open(os.path.join(target_folder,key+'_'+name+'.csv'),'w') as f:
            #print(f)
            if len(complete_data[name])>0:
                writer = csv.DictWriter(f, fieldnames=complete_data[name][0].keys(),lineterminator='\n')
                writer.writeheader()
                writer.writerows(complete_data[name])
                f.close()

