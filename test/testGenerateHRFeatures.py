'''
Created on Jun 14, 2014

@author: jacoba100
'''
import unittest
from generateHRFeatures import FeatureProcessor

class Test(unittest.TestCase):


    def testProcess(self):
        
        processor = FeatureProcessor()
        try:
            with open('../resources/rawFeatures.txt', 'r') as rawFeatures:
                allData = rawFeatures.readlines()
                
                for line in allData:
                    processor.process(line)
        except Exception as inst:
            print type(inst)
            print inst
            
        
        


if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testProcess']
    unittest.main()