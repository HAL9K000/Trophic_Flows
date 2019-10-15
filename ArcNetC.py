# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 14:00:14 2019

@author: Koustav
"""

import networkx as nex
import math
import os
from ArcNet import ArtificialNet
import copy
import matplotlib.pyplot as plt
import numpy as np


'''This script will generate multiple artifical networks with different connectivities in
    Machine_Readable_Data\Mult\Connectance\Set %d\# %d
    wile varying both inter- and intra- connectance.'''
    

class ArtificialNet_C(ArtificialNet):
    
    def __init__(self):
        
        self.distr=[20,20,20]
        self.n=sum(self.distr)
        #Total number of nodes in the artificial network
        self.config=[]   #Stores the node distribution
        for x in self.distr:
            num= float((x/self.n))
            self.config.append(num)
        self.string='Connectance'
        #To be defined later
        self.m=0
        
        self.connectance_def= {(0, 0): 0.0, (0, 1): 0.24, (1, 1): 0.05, 
                          (1, 2): 0.15, (2, 2): 0.027777777777777776, 
                          (2, 3): 0.0, (2, 1): 0.006122448979591836, 
                          (3, 3): 0.0, (3, 2): 0.0, (3, 1): 0.0}
        '''This is the default value of self-connectance, where the inter-trophic connectivity is set to 0.11
            while intra-trophic connectivity is based on the Tuesday Lake dataset'''
        
        self.connectance= copy.copy(self.connectance_def)
        
    def houston(self):          #The launch pad, the nerve centre, for everything that follows suit.
        
        if(os.path.isdir("Machine_Readable_Data\Mult")==False):
            os.mkdir("Machine_Readable_Data\Mult")
        os.chdir("Machine_Readable_Data\Mult")
        
        if(os.path.isdir("Connectance")==False):
            os.mkdir("Connectance")
        os.chdir("Connectance")
        #Changing to connectance directory  
        
        #Creating a file which explains the storage nomenclature
        f=open("nomenclature.txt", 'w')
        f.write("A note on the listing below:\n")
        f.write("In 0.6_3.1 the first number denotes the scaling factor of the inter-connectivity, i.e. 0.6*0.11\n")
        f.write("And 3.1 represents the scaling factor applied to the default intra-connectivity, ie. 3.1*0.05 for (1,1)\n")
        f.flush(); f.close()
        
        if(os.path.isdir("Set II")==False):
            os.mkdir("Set II")
        os.chdir("Set II")
        
        a=np.linspace(0.6,5,num=12)
        b=np.linspace(0.0,2.5,num=6)
        
        for x in a:
            #x runs from 0.2 to 5, acting as the scaling factor for the inter-connectivity
            for y in b:
                #Scaling factor for intra-connectivity.
                
                if(os.path.isdir("%3.2f_%3.2f" %(x,y))==False):
                    os.mkdir("%3.2f_%3.2f" %(x,y))
                os.chdir("%3.2f_%3.2f" %(x,y))
                #Changing to a relevant directory
                
                
                
                for key in self.connectance_def.keys():
                    if key[0]==key[1]:
                        print("Choo!")
                        #Given key represents an intra-connection.
                        self.connectance[key]=self.connectance_def[key]*y
                        #Scaling the intra-connections by y.
                    else:
                        self.connectance[key]=self.connectance_def[key]*x
                        #Scaling the inter-connections by x
                
                '''Following are functions from ArcNet.py that annotate edges (capacity), nodes (node capacities) and saves the resultant
                graph in the graphml format accordingly'''
                
                self.creator()
                
                '''Following are functions from I0.py that annotate edges (capacity), nodes (node capacities) and saves the resultant
                graph in the graphml format accordingly'''
                
                self.edge_annotation()
                self.node_cap()
                
                self.output(x,y)
            
                os.chdir("../")
                #In order to create a new directory
        
    def output(self,x,y):
         
        f=open('log_unabridged.txt','w')
        f.write("Max Trophic level is:\t%d\n" %(self.m))
        nex.write_graphml(self.DirGraph, '%s_Annotated.graphml' %(self.string))
        #Outputting artificially generated graph in graphml format
        
        f.write("Intra-Connectance Scale Factor:\n")
        f.write("%f\n" %(y))
        
        f.write("Inter-Connectance Scale Factor:\n")
        f.write("%f\n" %(x))
            
        f.flush(), f.close()
        
        nex.draw_kamada_kawai(self.DirGraph, with_labels=True)
        plt.axis('off')
        plt.savefig("Plot_%s.png" %(self.string), dpi=300)
        #plt.show()
        plt.close()
                


obj=ArtificialNet_C()
if __name__ == '__main__':
    obj.houston() 
            