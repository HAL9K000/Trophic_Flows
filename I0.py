# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:38:37 2019

@author: Koustav
"""

import os
import networkx as nex
import numpy as np

''' This is a script that takes a CSV file and coverts it to machine readable format and tags it with
     perceived trophic level data'''
class I_O:
    
    def __init__(self):
        os.chdir("CSV Data")
        self.string = "fw_ythan91"
        self.foodweb= np.genfromtxt("%s.csv" %(self.string), delimiter=',')
        print(len(self.foodweb))
        os.chdir("../")
        
    def control_panel(self):
        self.creator()
        self.node_anotation()
        self.edge_annotation()
        self.node_cap()
        self.output()
        
        
        
    def creator(self):      #Creating an Adjaceny Matrix From Given CSV
        print("AdjacenyList\%s" %(self.string))
        if(os.path.isdir("Machine_Readable_Data\%s" %(self.string))==False):
            os.mkdir("Machine_Readable_Data\%s" %(self.string))
        os.chdir("Machine_Readable_Data\%s" %(self.string))
        
        f=open("%s_AdjList.txt" % (self.string), 'w')
        
        self.k=[]
        
        for i in range(0, len(self.foodweb)):
            m=0
            f.write("%d" %(i))
            for j in self.foodweb[i,:]:
                if j>0:
                    f.write(" %d" %(m))
                    if( m==i):
                        print("Boo!")
                        self.k.append(int(i))
                        
                m+=1
            f.write("\n")
        f.flush()
        f.close()
        
        print(self.foodweb.shape)
        #Reading Adjacency List into Directed Graph
        g=open("%s_AdjList.txt" %(self.string),'rb')
        self.DirGraph=nex.read_adjlist(g, create_using=nex.DiGraph)
        g.flush()
        g.close()
        
     
    def node_anotation(self):
        
        for x in self.DirGraph.nodes():
            if (self.DirGraph.in_degree(x)==0): 
                #Nodes with no inflow, ergo sources or Trophic Level 0 (Producers)
                self.DirGraph.nodes[x]['trophic']=0
                
        trophiclvl=nex.get_node_attributes(self.DirGraph,'trophic')
        #Returns dict of nodes with assigned trophic values
        print(trophiclvl)
        trophiclvl0=trophiclvl
        self.DirGraph.add_node('s', trophic=-1)
        #Adding the super node, the ultimate source of all energy.
        
        for s in trophiclvl0.keys():
            self.DirGraph.add_edge('s',s)
                
        self.m=0 
        #Stores the value of the highest trophic level that's been assigned.
        while(len(trophiclvl)<len(list(self.DirGraph.nodes()))):
                    
            for (x,y) in list(self.DirGraph.nodes(data='trophic')):
            
                #Returns node and trophic value
                if (y==self.m):
                    #Checking if x is in Trophic Level m
                    for t in self.DirGraph.neighbors(x):
                    
                        #Getting all neighbours of species of trophic level m
                        if (t not in trophiclvl.keys()):
                            #If neighbours of above species haven't been assigned yet
                            self.DirGraph.nodes[t]['trophic']=self.m+1
                        '''if(x !=t ):
                            #Cannibalistic self-loops don't get assigned
                            self.DirGraph[x][t]['capacity']=10**(2-m)'''
                    
            
            
            trophiclvl=nex.get_node_attributes(self.DirGraph,'trophic')
            print(trophiclvl)
            print(len(trophiclvl))
            self.m+=1
            
        
        print("The trophic level of the system is:\t%d" %(self.m))
        
        
    def edge_annotation(self):          #Assigning capacities to all edges except self-loops.
        
        
        t=-1
        trophiclvl=nex.get_node_attributes(self.DirGraph,'trophic')
        print(trophiclvl)
        while (t<=self.m):
            #Iterarting through trophic levels
            for (key, val) in trophiclvl.items():
                if (val==t):
                    #For a given trophic level
                    for n in self.DirGraph.neighbors(key):
                        #Iterating through it's neighbours
                        if(n!=key):
                            #Provided it is not a self-loop (cannibalistic)
                            self.DirGraph[key][n]['capacity']=10**(self.m-t)
            t+=1
            
        print(len(list(self.DirGraph.edges())))
        edgecap=nex.get_edge_attributes(self.DirGraph,'capacity')
        print("Number of Annotated Edges:\t%d" %(len(edgecap)))
        
        r=0
        #Counting number of self-loops
        for x in self.DirGraph.edges():
            if x[0]==x[1]:
                r+=1
                print(x)
        print("Number of self loops:\t%d" %(r))
        
        
    def node_cap(self):         #Computes node capacities.
        
        edgecap=nex.get_edge_attributes(self.DirGraph,'capacity')
        #A dict with edge tuples as as keys and capacities as values.
        trophiclvl=nex.get_node_attributes(self.DirGraph,'trophic')
        for n in list(self.DirGraph.nodes()):
            #Running through all the nodes in the the graph.
            ncap=0 #Stores the capacity of all incoming edges to n
            if(n != 's'):
                for p in self.DirGraph.predecessors(n):
                    if(n==p):
                        # For cannibalistic edges use trophic level to estimate capacity
                        ncap+=10**(self.m-trophiclvl[n])
                    else:    
                        ncap+= edgecap[(p,n)]
                self.DirGraph.nodes[n]['node_cap']=ncap
        
        
    def output(self): 
        f=open('log_unabridged.txt','w')
        f.write("Max Trophic level is:\t%d\n" %(self.m))
        nex.write_graphml(self.DirGraph, '%s_Annotated.graphml' %(self.string))
        #Outputting min vertex cut graph in graphml format
        f.flush(), f.close()
        
obj=I_O()
if __name__ == '__main__':
    obj.control_panel()
                    
        
        