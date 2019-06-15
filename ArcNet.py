# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 15:16:32 2019

@author: Koustav
"""

import networkx as nex
import os
import random as ran
from .I0 import I_O


class ArtificialNet(I_O):
    
    def __init__(self):
        
        self.n=24   #Total number of nodes
        
        self.configuration() #Determines trophic distribution of nodes
        
        self.connectance={(0, 0): 0.0, (0, 1): 0.29523809523809524, (1, 1): 0.050347222222222224, 
                          (1, 2): 0.44642857142857145, (2, 2): 0.4489795918367347, 
                          (2, 1): 0.017857142857142856}
        # Using connectance data from Tuesday Lake
        
        
    def houston(self):      #Control deck
        self.creator()
        
        
    def creator(self):      #Creates the graph from specified data, one node at a time
        
        self.DirGraph=nex.DiGraph()
        #Empty directed graph.
        
        s=self.distr.sum() #Total nodes in node distribution
        
        #Creating nodes and labelling them according to trophic level
        
        trp=0 #Stores current trohic level
        p=0
        for n in range(0,s):
            p+=1
            
        
        
                
    def configuration(self): #Determines trophic distribution of nodes
        
        self.conf= input("Input a configuration of your choice using same keywords: 'Rect', 'Inv Tr', 'Tr', 'Dia', 'Chal', 'Inv Chal'\n") 
        #Determing patterning of nodes
        self.config=[]
        if (self.conf=="Rect"):
            print("The given %s configuration is 1:1:1" %(self.conf))
            self.config=[1,1,1]
        elif (self.conf=="Inv Tr"):
            print("The given %s configuration is 1:2:3" %(self.conf))
            self.config=[1,2,3]
        elif (self.conf=="Tr"):
            print("The given %s configuration is 3:2:1" %(self.conf))
            self.config=[3,2,1]
        elif (self.conf=="Dia"):
            print("The given %s configuration is 1:2:1" %(self.conf))
            self.config=[1,2,1]
        elif (self.conf=="Chal"):
            print("The given %s configuration is 1:2:2" %(self.conf))
            self.config=[1,2,2]
        elif (self.conf=="Inv Chal"):
            print("The given %s configuration is 2:2:1" %(self.conf))
            self.config=[2,2,1]
        else:
            print("Enter config of your own, one trophic level at a time, press 0 to finish")
            i=0
            inp= int(input("Enter ratio of nodes for %d Trophic level\n" %(i)))
            while(inp != 0):                
                self.config.append(inp)
                i+=1
                inp= int(input("Enter ratio of nodes for %d Trophic level\n" %(i)))
                
        
        s=self.config.sum()         #Sum of ratios
        self.distr=[]   #Stores the node distribution
        for x in self.config:
            num= int((x*self.n)/s)
            self.distr.append(num)

            