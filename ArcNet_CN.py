# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 17:30:14 2019

@author: Koustav
"""

import networkx as nex
import math
import matplotlib.pyplot as plt
import os
from ArcNet import ArtificialNet
import copy
import numpy as np

'''Creates and saves artificial networks where both number of nodes in a given trophic level and the inter-connectance
    is altered'''

class ArtificialNet_C_N(ArtificialNet):
    
    def __init__(self):
        
        self.distr=[20,20,20]
        # Stores the absolute number of vertices stored in each trophic level.
        self.n=sum(self.distr)
        self.config=[]
        for x in self.distr:
            self.config.append(float(x/self.n))
        # self.config stores the vertice distribution ratio among trophic levels.
        
        '''self.connectance_def= {(0, 0): 0.0, (0, 1): 0.11, (1, 1): 0.05, 
                          (1, 2): 0.11, (2, 2): 0.027777777777777776, 
                          (2, 3): 0.11, (2, 1): 0.006122448979591836, 
                          (3, 3): 0.0, (3, 2): 0.0, (3, 1): 0.0}'''
        
        '''Defining the raw template of the connectance which is to be varied.'''
        
        self.connectance_def= {(0, 0): 0.0, (0, 1): 0.24, (1, 1): 0.05, 
                          (1, 2): 0.15, (2, 2): 0.027777777777777776, 
                          (2, 3): 0.0, (2, 1): 0.006122448979591836, 
                          (3, 3): 0.0, (3, 2): 0.0, (3, 1): 0.0}
        
        '''Based on Ythan91 data.'''
        
        self.string='Connectance_NodeNum'
        #To be defined later, check ArcNet.py
        self.m=0
        
        self.connectance= copy.copy(self.connectance_def)
        
        
    def dallas(self):           #What would Houston be without Dallas?
        
        if(os.path.isdir("Machine_Readable_Data\Mult")==False):
            os.mkdir("Machine_Readable_Data\Mult")
        os.chdir("Machine_Readable_Data\Mult")
        
        if(os.path.isdir("Node-Connectance")==False):
            os.mkdir("Node-Connectance")
        os.chdir("Node-Connectance")
        #Changing to node-connectance directory 
        
        if(os.path.isdir("InterConnectance")==False):
            os.mkdir("InterConnectance")
        os.chdir("InterConnectance")
        
        #Creating a file which explains the storage nomenclature
        f=open("nomenclature.txt", 'w')
        f.write("A note on the listing below:\n")
        
        f.write("In [35,20,20]_0.6 the second number denotes the scaling factor of the intra-connectivity,\n")
        f.write("Meanwhile the [35, 20,20] represents the node distribution\n")
        f.flush(); f.close()
        
        if(os.path.isdir("Set III_Yth")==False):
            os.mkdir("Set III_Yth")
        os.chdir("Set III_Yth")
        
        a=np.linspace(0.6,3.8,num=9)
        # The range over which inter-connectivity is scaled over.
        #a=np.append(a,[0.0])
        
        for i in range(5,55,5):
            # Changing the node distribution from 5 to 60
            
            self.distr=[20, 20, i]
            
            self.n=sum(self.distr)
            
            self.config=[]
            for x in self.distr:
                self.config.append(float(x/self.n))
            # self.config stores the vertice distribution ratio among trophic levels.
            
            
            
            for j in a:
                #Iterating over the gamut of inter-connectivity scaling factors.
                
                if(os.path.isdir(str(self.distr)+"_%3.2f" %(j))==False):
                    os.mkdir(str(self.distr)+"_%3.2f" %(j))
                os.chdir(str(self.distr)+"_%3.2f" %(j))
                
                for (x,y) in self.connectance_def.keys():
                    
                    if( x != y):
                        #If the key isn't an intraconnection such as (1,1) or (2,2)
                        self.connectance[(x,y)]= j*self.connectance_def[(x,y)]
                        #Then scale by j.
                        
                '''Following are functions from ArcNet.py that annotate edges (capacity), nodes (node capacities) and saves the resultant
                graph in the graphml format accordingly'''
                
                self.creator()
                
                '''Following are functions from I0.py that annotate edges (capacity), nodes (node capacities) and saves the resultant
                graph in the graphml format accordingly'''
                
                self.edge_annotation()
                self.node_cap()
                
                self.output(i,j)
            
                os.chdir("../")
                #In order to create a new directory
        
        os.chdir("../../../../../")
        #Now back in root directory.
                
    def output(self,i,j):
         
        f=open('log_unabridged.txt','w')
        f.write("Max Trophic level is:\t%d\n" %(self.m))
        nex.write_graphml(self.DirGraph, '%s_Annotated.graphml' %(self.string))
        #Outputting artificially generated graph in graphml format
        
        f.write("Number Of Nodes in Altered Trophic Level:\n")
        f.write("%f\n" %(i))
        
        f.write("Inter-Connectance Scale Factor:\n")
        f.write("%f\n" %(j))
        
        f.write("Intra-Connectance Scale Factor:\n")
        f.write("1\n")
            
        f.flush(), f.close()
        
        nex.draw_kamada_kawai(self.DirGraph, with_labels=True)
        plt.axis('off')
        plt.savefig("Plot_%s.png" %(self.string), dpi=300)
        #plt.show()
        plt.close()
        
        
obj=ArtificialNet_C_N()

if __name__== "__main__":
    obj.dallas()
                        
                        
            
            
        
        
        
            