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
        
        self.n=70   #Total number of nodes
        
        self.configuration() #Determines trophic distribution of nodes
        
        '''self.connectance={(0, 0): 0.0, (0, 1): 0.24, (1, 1): 0.053877551020408164, 
                          (1, 2): 0.15374149659863945, (2, 2): 0.027777777777777776, 
                          (2, 3): 0.07142857142857142, (2, 1): 0.006122448979591836, 
                          (3, 3): 0.0, (3, 2): 0.0, (3, 1): 0.0}'''
        #Based on Ythan91
        
        '''self.connectance={(0, 0): 0.0, (0, 1): 0.29523809523809524, (1, 1): 0.050347222222222224, 
                          (1, 2): 0.44642857142857145, (2, 2): 0.4489795918367347, 
                          (2, 1): 0.017857142857142856}'''
        # Using connectance data from Tuesday Lake
        
        self.connectance={(0, 0): 0.0, (0, 1): 0.11, (1, 1): 0.05, 
                          (1, 2): 0.11, (2, 2): 0.027777777777777776, 
                          (2, 3): 0.11, (2, 1): 0.006122448979591836, 
                          (3, 3): 0.0, (3, 2): 0.0, (3, 1): 0.0}
        
        self.string="fw_ArtNet_"+self.conf
        #Used for the saving the graphml file.
        
        
        
    def houston(self):      #Control deck
        
        if(os.path.isdir("Machine_Readable_Data\%s" %(self.string))==False):
            os.mkdir("Machine_Readable_Data\%s" %(self.string))
        os.chdir("Machine_Readable_Data\%s" %(self.string))
        
        self.creator()      #Creates graph (nodes + edges) and assigns trophic levels
        
        
        
        '''Following are functions from I0.py that annotate edges (capacity), nodes (node capacities) and saves the resultant
           graph in the graphml format accordingly'''
        
        self.edge_annotation()
        self.node_cap()
        self.output()
        
        
        
    def creator(self):      #Creates graph (nodes + edges) and assigns trophic levels to nodes accordingly.
        
        self.DirGraph=nex.DiGraph()
        #Empty directed graph.
        
        
        
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
            if (self.trophiclvl[n]==1):
                a.append(n)
            elif (self.trophiclvl[n]==3):
                b.append(n)
        
        print("Nodes in trophic level 1 are:\t"+str(a))
        print("Nodes in trophic level 3 are:\t"+str(b))
                
        
        for (x,y) in self.connectance.keys():
            l1=[]; l2=[]
            #Stores list of nodes in different trophic levels            
            for n in self.DirGraph.nodes():
                if (self.trophiclvl[n]==x):
                    l1.append(n)
                if(self.trophiclvl[n]==y):
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
        flag=0
        i=0
        while(i<p):
            
            #Choosing random nodes from the two trophic levels to be linked up.
            v1=ran.choice(l1)
            v2=ran.choice(l2)
            if(x[0] == (x[1]-1)):
                #If the two levels are in trophic succession such as (1,2) or (2,3)
                flag=1
                if(len(b)!=0):
                    #All members of a given trophic level must connect to a member of the preceding tropic level.
                    v2=ran.choice(b)
                    b.remove(v2)
                else:
                    #All members are linked up.
                    v2=ran.choice(l2)
                    flag=0
                    
            if((v1,v2) in a):
                #If randomly chosen edge already present in graph then skip to next iteration and pick again
                print("Boko")
                print(str(v1)+" , "+str(v2))
                continue
            else:
                self.DirGraph.add_edge(v1,v2)
                a.append((v1,v2))
                i=i+1
                
        if(flag==1):
            #For sparse connecrtions, all the members of a trophic level must connect to the previous trophic level.
            while(len(b)>0):
                v1=ran.choice(l1)
                v2=ran.choice(b)
                b.remove(v2)
                self.DirGraph.add_edge(v1,v2)
                a.append((v1,v2))
                
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


class ArtificialNet_Mult_Node(ArtificialNet):
    # To create multiple graphs at once varying some parameter (node distribution)
    
    def houston(self):
        
        if(os.path.isdir("Machine_Readable_Data\Mult")==False):
            os.mkdir("Machine_Readable_Data\Mult")
        os.chdir("Machine_Readable_Data\Mult")
        
        if(os.path.isdir("Node Distribution")==False):
            os.mkdir("Node Distribution")
        os.chdir("Node Distribution")
        #Changing node distribution.
        
        if(os.path.isdir("Set I")==False):
            os.mkdir("Set I")
        os.chdir("Set I")
        
        i=0.25
        while(i<=3):
            self.config=[i,1,1]
            self.string=str(self.config)
            
            if(os.path.isdir("%s" %(self.string))==False):
                os.mkdir("%s" %(self.string))
            os.chdir("%s" %(self.string))
                
            s=sum(self.config)         #Sum of ratios
            self.distr=[]   #Stores the node distribution
            for x in self.config:
                num= int((x*self.n)/s)
                self.distr.append(num)
        
            self.creator()      #Creates graph (nodes + edges) and assigns trophic levels
        
        
            '''Following are functions from I0.py that annotate edges (capacity), nodes (node capacities) and saves the resultant
                graph in the graphml format accordingly'''
        
            self.edge_annotation()
            self.node_cap()
            self.output()
            
            os.chdir("../")
            #In order to create a new directory
            
            i+=0.25
        
    def output(self):
         
        f=open('log_unabridged.txt','w')
        f.write("Max Trophic level is:\t%d\n" %(self.m))
        nex.write_graphml(self.DirGraph, '%s_Annotated.graphml' %(self.string))
        #Outputting min vertex cut graph in graphml format
        f.write("Node Distribution:\n")
        for x in self.config:
            f.write("%f\n" %(x))
            
        f.flush(), f.close()
        
        nex.draw_kamada_kawai(self.DirGraph, with_labels=True)
        plt.axis('off')
        plt.savefig("Plot_%s.png" %(self.string), dpi=300)
        plt.show()
        plt.close()
        

class ArtificialNet_Mult_NodeNum(ArtificialNet):
    # To create multiple graphs at once varying some parameter (node number)
    
    def houston(self):
        
        if(os.path.isdir("Machine_Readable_Data\Mult")==False):
            os.mkdir("Machine_Readable_Data\Mult")
        os.chdir("Machine_Readable_Data\Mult")
        
        if(os.path.isdir("Node Number")==False):
            os.mkdir("Node Number")
        os.chdir("Node Number")
        #Changing node distribution.
        
        if(os.path.isdir("Set IV")==False):
            os.mkdir("Set IV")
        os.chdir("Set IV")
        
        i=0.25
        p=5
        while(i<=3):
            
            self.distr=[20,20,p]
            self.string=str(self.distr)
            
            if(os.path.isdir("%s" %(self.string))==False):
                os.mkdir("%s" %(self.string))
            os.chdir("%s" %(self.string))
                
            self.n=sum(self.distr)         #Sum of distribution
            self.config=[]   #Stores the node distribution
            for x in self.distr:
                num= float((x/self.n))
                self.config.append(num)
        
            self.creator()      #Creates graph (nodes + edges) and assigns trophic levels
        
        
            '''Following are functions from I0.py that annotate edges (capacity), nodes (node capacities) and saves the resultant
                graph in the graphml format accordingly'''
        
            self.edge_annotation()
            self.node_cap()
            self.output()
            
            os.chdir("../")
            #In order to create a new directory
            
            i+=0.25
            p+=5
        
    def output(self):
         
        f=open('log_unabridged.txt','w')
        f.write("Max Trophic level is:\t%d\n" %(self.m))
        nex.write_graphml(self.DirGraph, '%s_Annotated.graphml' %(self.string))
        #Outputting min vertex cut graph in graphml format
        f.write("Node Distribution (Numbers):\n")
        for x in self.distr:
            f.write("%f\n" %(x))
            
        f.flush(), f.close()
        
        nex.draw_kamada_kawai(self.DirGraph, with_labels=True)
        plt.axis('off')
        plt.savefig("Plot_%s.png" %(self.string), dpi=300)
        plt.show()
        plt.close()
        
    

obj=ArtificialNet_Mult_NodeNum()
if __name__ == '__main__':
    obj.houston()           