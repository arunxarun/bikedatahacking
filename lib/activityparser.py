#!/usr/bin/python
'''
Created on Feb 16, 2013

@author: jacoba100

usage: ./activityparser.py -i ../resources/Move_2014_06_11_05_25_15_Cycling.tcx | cut -f 1,4,6,7,8 | ./generateHRFeatures.py 
'''
import sys
import xml.etree.ElementTree as ET
from optparse import OptionParser
import dateutil.parser
import logging

import json
import logging

ACTVITIES = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Activities'
ACTIVITY = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Activity'
LAP = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Lap'
TRACK = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Track'
TIME = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Time'
POSITION = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Position'
LAT = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LatitudeDegrees'
LONG = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LongitudeDegrees'
ALT = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AltitudeMeters'
DIST = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters'
HRBPM = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}HeartRateBpm'
HRVAL = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Value'

TOTALTIME ='{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}TotalTimeSeconds' 
CALORIES = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Calories'
AVGHR = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AverageHeartRateBpm'
INTENSITY = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Intensity'
VALUE  = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Value'
ID = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Id'
EXT = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Extensions'
TPX = '{http://www.garmin.com/xmlschemas/ActivityExtension/v2}TPX'
SPEED = '{http://www.garmin.com/xmlschemas/ActivityExtension/v2}Speed'

'''
{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters
{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}MaximumSpeed


{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}MaximumHeartRateBpm

{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}TriggerMethod

'''



        
    
class ActivityParser(object):
    '''
    parses actvities into a set of objects
    '''


    def __init__(self,logger,isMetric = False):
        '''
        Constructor
        '''
        self.parsedLaps= []
        self.summary = None
        self.logger = logger
        self.isMetric = isMetric
    
    def parse(self,inFileName,outFileName,type):
        
        activities = []
        aggregatedTrackPoints = []
        tree = ET.parse(inFileName)
        
        if outFileName != None:
            outFile =  open(outFileName,"w")
        
        root = tree.getroot()
        
        activitiesTag = root.find(ACTVITIES)
        
        for activityTag in activitiesTag:
            
            laps = []  
            lapTags = activityTag.findall(LAP)
            act_type  = activityTag.attrib['Sport']
            idTag = activityTag.find(ID)
            act_id = idTag.text
            
            
            
            for lapTag in lapTags:
                tracks = []
                tt = 0
                td = 0
                cc = 0
                hr = 0
                isResting = False
                
                totaltime = lapTag.find(TOTALTIME)
                if(totaltime != None):
                    tt = float(totaltime.text)
                
                totalDistTag = lapTag.find(DIST)
                if(totalDistTag != None):
                    td = float(totalDistTag.text)
                                         
                cals = lapTag.find(CALORIES)
                if(cals != None):
                    cc = float(cals.text)
                
                avgHrTag = lapTag.find(AVGHR)
                if(avgHrTag != None):
                    val = avgHrTag.find(VALUE)
                    avgHr = float(val.text)
                    
                intensity = lapTag.find(INTENSITY)
                if(intensity != None):
                    if(intensity.text == 'Resting'):
                        isResting = True
                    else:
                        isResting = False
                    
                
                
                # TODO: group trackpoints with laps but also group them into buckets of groupBy count. 
                # return these separately. 
                
                trackTags = lapTag.findall(TRACK)
                
                for trackTag in trackTags:
                    
                    trackPoints = []
                    for trackpointTag in trackTag:
                        
                        realtime = ''
                        lat = ''
                        lng = ''
                        alt = ''
                        dist = ''
                        hr = ''
                        
                        ts = 0
                        latDegrees = 0.0
                        lngDegrees = 0.0
                        altMeters = 0.0
                        distMeters = 0.0
                        hrBpm = 0
                        speedMeters = 0.0
                        
                        timesec = trackpointTag.find(TIME)
                        if timesec != None:
                            realtime = timesec.text
                            d2 = dateutil.parser.parse(realtime)
                            ts = d2.astimezone(dateutil.tz.tzutc())
                        else:
                            ts = None
                            
                        pos = trackpointTag.find(POSITION)
                        if pos != None:
                            lat = pos.find(LAT)
                            latDegrees = float(lat.text)
                            lng = pos.find(LONG)
                            lngDegrees = float(lng.text)
                        else:
                            latDegrees = lngDegrees = 0
                        
                        alt = trackpointTag.find(ALT)
                        if alt != None:
                            altMeters = float(alt.text)
                        else:
                            alt = 0
                            
                        
                        dist = trackpointTag.find(DIST)
                        if dist != None:
                            distMeters = float(dist.text)
                        else:
                            distMeters = 0
                            
                        hrb = trackpointTag.find(HRBPM)
                        
                        if hrb != None:
                            hr = hrb.find(HRVAL)
                            hrBpm = int(hr.text)
                        else:
                            hrBpm = 0
                        
                        ext = trackpointTag.find(EXT)
                        if ext != None:
                            tpx = ext.find(TPX)
                            if tpx != None:
                                speed = tpx.find(SPEED)
                                if speed != None:
                                    speedMeters = float(speed.text)
                
                
#                        ts = 0
#                        latDegrees = 0.0
#                        lngDegrees = 0.0
#                        altMeters = 0.0
#                        distMeters = 0.0
#                        hrBpm = 0
#                        speedMeters = 0.0
                        str = "%s\t%0.9f\t%0.9f\t%0.9f\t%0.9f\t%d\t%0.9f\t%d"%(ts,latDegrees,lngDegrees,altMeters,distMeters,hrBpm,speedMeters,type)
                        if outFileName != None:
                            outFile.write(str+"\n")
                        else:
                            print str
                
                
if __name__ == "__main__":
    
    parser = OptionParser()
    parser.add_option("-i", "--inFile", dest="inFileName",
                          help="parse FILE", metavar="FILE")
    parser.add_option("-o", "--outFile", dest="outFileName",
                          help="output FILE", metavar="FILE")
    
    parser.add_option("-t", "--type", dest="type",
                          help="exercise type", metavar="type")
    
    (options, args) = parser.parse_args()
        
    inFileName = options.inFileName
    outFileName = options.outFileName
    type = options.type
    if inFileName == None:
        print 'usage: python activityparser.py -i [inFileName] -o [outFileName]'
        sys.exit()

    if type == None:
        type = 1 # road biking = 1, mtb =2, running = 3
    
    logger = logging.getLogger('activityparser')
    hdlr = logging.FileHandler('./testoutput/activityparser.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)   
    
    ap = ActivityParser(logger)
    ap.parse(inFileName,outFileName,type)
    
    
        
    # persist these to Cassandra? 
        