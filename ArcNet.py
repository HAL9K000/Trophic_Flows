# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 15:16:32 2019

@author: Koustav
"""

import networkx as nex
import os
import random as ran
from I0 import I_O
import matplotlib.pyplot as plt
import copy


#Using connectance data from Tuesday Lake

class ArtificialNet(I_O):
    
    def __init__(self):
        
        self.n=24   #Total number of nodes
        
        self.configuration() #Determines trophic distribution of nodes
        
        self.connectance={(0, 0): 0.0, (0, 1): 0.29523809523809524, (1, 1): 0.050347222222222224, 
                          (1, 2): 0.44642857142857145, (2, 2): 0.4489795918367347, 
                          (2, 1): 0.017857142857142856}
        # Using connectance data from Tuesday Lake
        self.string="fw_ArtNet_"+self.conf
        #Used for the saving the graphml file.
        
        
        
    def houston(self):      #Control deck
        self.creator()      #Creates graph (nodes + edges) and assigns trophic levels
        
        nex.draw_kamada_kawai(self.DirGraph, with_labels=True)
        plt.axis('off')
        plt.show()
        plt.close()
        
        '''Following are functions from I0.py that annotate edges (capacity), nodes (node capacities) and saves the resultant
           graph in the graphml format accordingly'''
        
        self.edge_annotation()
        self.node_cap()
        self.output()
        
        
        
    def creator(self):      #Creates graph (nodes + edges) and assigns trophic levels to nodes accordingly.
        
        self.DirGraph=nex.DiGraph()
        #Empty directed graph.
        
        if(os.path.isdir("Machine_Readable_Data\%s" %(self.string))==False):
            os.mkdir("Machine_Readable_Data\%s" %(self.string))
        os.chdir("Machine_Readable_Data\%s" %(self.string))
        
        s=sum(self.distr) #Total nodes in node distribution
        print("Total nodes being considered:\t%d" %(s))
        #Creating nodes and labelling them according to trophic level
        
        self.m=0 #Stores current trophic level
        p=0     #Numbering the nodes
        
        for n in self.distr:          
            for i in range(0,n):
                k=str(p)
                self.DirGraph.add_node(k, trophic=self.m)
                p+=1
            self.m+=1       
        #Nodes are created, next to create edges using connectance data
        
        self.m-=1 #Maximum trophic level stored here.
        
        print("The trophic level of the system is:\t%d" %(self.m))
        
        self.trophiclvl=nex.get_node_attributes(self.DirGraph, 'trophic')
        print(self.trophiclvl)
        a=[]; b=[]
        for n in self.DirGraph.nodes():
            if (self.trophiclvl[n]==0):
                a.append(n)
            elif (self.trophiclvl[n]==1):
                b.append(n)
        
        print("Nodes in trophic level 0 are:\t"+str(a))
        print("Nodes in trophic level 1 are:\t"+str(b))
                
        
        for (x,y) in self.connectance.keys():
            l1=[]; l2=[]
            #Stores list of nodes in different trophic levels            
            for n in self.DirGraph.nodes():
                if (self.trophiclvl[n]==x):
                    l1.append(n)
                elif(self.trophiclvl[n]==y):
                    l2.append(n)
            self.edgeconnector(l1,l2, (x,y))
            
            
        
        self.DirGraph.add_node('s', trophic=-1)
        #Adding the super node, the ultimate source of all energy.
        
        a=[]
        for x in self.DirGraph.nodes():
            if (self.DirGraph.in_degree(x)==0):
                if(x != 's'):
                    #s has no in-degree too. We wish to prevent self-loops.
                    self.DirGraph.add_edge('s',x)
                    a.append(x)
        
        print("Nodes in trophic level 0 are:\t"+str(a))
            
            

            
    def edgeconnector(self, l1, l2, x): #Adds edges as per connectance data
        
        p= int(len(l1)*len(l2)*self.connectance[x]) 
        #Gives the realised edges that need to be formed b/w two trophic levels
        print("For "+str(x)+"trophic level, we have:\t%d edges" %(p))
        print("Total combinations possible:\t%d" %(len(l1)*len(l2)))
        a=[] #Stores list of chosen edges
        b=copy.copy(l2)
        i=0
        while(i<p):
            
            #Choosing random nodes from the two trophic levels to be linked up.
            v1=ran.choice(l1)
            v2=ran.choice(l2)
            if(x[0] == (x[1]-1)):
                #If the two levels are in trophic succession such as (1,2) or (2,3)
                if(len(b)!=0):
                    #All members of a given trophic level must connect to a member of the preceding tropic level.
                    v2=ran.choice(b)
                    b.remove(v2)
                else:
                    #All members are linked up.
                    v2=ran.choice(l2)
                    
            if((v1,v2) in a):
                #If randomly chosen edge already present in graph then skip to next iteration and pick again
                print("Boko")
                print(str(v1)+" , "+str(v2))
                continue
            else:
                self.DirGraph.add_edge(v1,v2)
                a.append((v1,v2))
                i=i+1
                
        print("In "+str(x)+"trophic level, realised number of edges:\t%d\n" %(len(a)))
        
        
        
                
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
                
        
        s=sum(self.config)         #Sum of ratios
        self.distr=[]   #Stores the node distribution
        for x in self.config:
            num= int((x*self.n)/s)
            self.distr.append(num)

obj=ArtificialNet()
if __name__ == '__main__':
    obj.houston()           