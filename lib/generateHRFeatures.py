#!/usr/bin/python
'''
Created on Jun 13, 2014

@author: jacoba100

usage: ./activityparser.py -i ../resources/Move_2014_06_11_05_25_15_Cycling.tcx | cut -f 1,4,6,7,8 | ./generateHRFeatures.py 
'''
import sys
import dateutil
import dateutil.parser
from collections import deque

class FeatureProcessor:
    def __init__(self):
        self.last60Alts = deque()
        self.last60Speeds = deque()
        self.last60Hrs = deque()
        
    def process(self,str):
        last10AltsAvg = 0
        last10HrsAvg = 0
        last10SpeedsAvg = 0
        last30AltsAvg = 0
        last30HrsAvg = 0
        last30SpeedsAvg = 0
        last60AltsAvg = 0
        last60HrsAvg= 0
        last60SpeedsAvg = 0
        
        # TODO: process timestamp,alt,hr,speed,type and tx to delta alt, hr, speed,type
        
        features = str.split('\t')
        
            
        alt = float(features[1])
        hr = int(features[2])
        speed = float(features[3])
        extype = int(features[4])
        
        if alt == 0.0 and speed == 0.0:
            return
        
        self.last60Alts.appendleft(alt)
        self.last60Hrs.appendleft(hr)
        self.last60Speeds.appendleft(speed)
        
        altsLen = len(self.last60Alts)
        
        if altsLen > 10: # since we add to all of them, we can operate on all of them. 
            last10Alts = []
            last10Hrs = []
            last10Speeds = []
            for i in range(0,10):
                last10Alts.append(self.last60Alts[i])
                last10Hrs.append(self.last60Hrs[i])
                last10Speeds.append(self.last60Speeds[i])
                
            last10AltsAvg = float(sum(last10Alts))/len(last10Alts)
            last10HrsAvg = float(sum(last10Hrs))/len(last10Hrs)
            last10SpeedsAvg = float(sum(last10Speeds))/len(last10Speeds)
            
        
        if altsLen > 30:  
            last30Alts = []
            last30Hrs = []
            last30Speeds = []
            for i in range(0,30):
                last30Alts.append(self.last60Alts[i])
                last30Hrs.append(self.last60Hrs[i])
                last30Speeds.append(self.last60Speeds[i])
                
            last30AltsAvg = float(sum(last30Alts))/len(last30Alts)
            last30HrsAvg = float(sum(last30Hrs))/len(last30Hrs)
            last30SpeedsAvg = float(sum(last30Speeds))/len(last30Speeds)
            
        
        if altsLen > 60:
            
            # pop it down, bro
            
            self.last60Alts.pop()
            self.last60Hrs.pop()
            self.last60Speeds.pop()
                
            last60AltsAvg = float(sum(self.last60Alts))/len(self.last60Alts)
            last60HrsAvg = float(sum(self.last60Hrs))/len(self.last60Hrs)
            last60SpeedsAvg = float(sum(self.last60Speeds))/len(self.last60Speeds)
            
            
        # holy feature matrix, batman! 
        
        # alt,hr,speed,extypetype,last10AltsAvg,last10HrsAvg,last10SpeedsAvg,last30AltsAvg,last30HrsAvg,last30SpeedsAvg,last60AltsAvg,last60HrsAvg,last60SpeedsAvg
        
        print("%0.9f,%d,%0.9f,%d,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f"%(alt,hr,speed,extype,last10AltsAvg,last10HrsAvg,last10SpeedsAvg,last30AltsAvg,last30HrsAvg,last30SpeedsAvg,last60AltsAvg,last60HrsAvg,last60SpeedsAvg))
        
if __name__ == '__main__':
    
    
    processor =  FeatureProcessor()
    
    while(True):
        str = sys.stdin.readline()
        if str == '':
            break
        
        
        processor.process(str)
                
        
        
        