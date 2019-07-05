# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 17:00:24 2019

@author: Koustav
"""

import networkx as nex
import os

class ConnectednessDet:
    
    
    def __init__(self):
        self.string = "fw_ythan91"
        self.DirGraph=nex.read_graphml("Machine_Readable_Data\%s\%s_Annotated.graphml" %(self.string, self.string))
        self.trophiclvl=nex.get_node_attributes(self.DirGraph, 'trophic')
        '''Stores trophic level information as a dict with node labels serving as keys and corresponding trophic levels
        as values'''
        if(os.path.isdir("Connectedness Analysis\%s" %(self.string))==False):
            os.mkdir("Connectedness Analysis\%s" %(self.string))
        os.chdir("Connectedness Analysis\%s" %(self.string))
        
        
    def dura_mater(self): #The mother lode.
        
        top=max(list(self.trophiclvl.values())) #Finding maximum trophic level
        self.trophiclist= self.sorting_trophic(top)
        
        self.connectance(top)
        #self.log()
     
        
    def sorting_trophic(self, top): #Makes a list of possible trophic interactions
        
        l=[]
        for x in range(0,top+1):
            l.append((x,x))
            #Considering self-loops
            if(x != top): #Not top level consumers
                l.append((x, x+1))
            if (x>1): #Not producers or primary consumers
                for y in range(x-1, 0, -1):
                    #Conidering higher trophic level to lower trophic level interactions.
                    l.append((x,y))
        
        return l
    
    def connectance(self, top):      #This calculates the connectance b/w any two given trophic levels
        
        p={}
                   
        for x in range(0,top+1):
            p[x]=0
            # p is a dictionary that stores all the number of nodes at any given trophic level
            for n in self.DirGraph.nodes():
                if (self.trophiclvl[n]==x):
                    p[x]+=1
                    
        print(p)
        self.conn_dict={}
        
        for (x,y) in self.trophiclist:
            self.conn_dict[(x,y)]=0
            for e in list(self.DirGraph.edges()):
                if( self.trophiclvl[e[0]]== x and self.trophiclvl[e[1]]== y):
                    #If they fit the bill of the trophic level.
                    self.conn_dict[(x,y)]+=1                
            self.conn_dict[(x,y)]=self.conn_dict[(x,y)]/(p[x]*p[y])
            '''Connectance is defined as edges present between two trophic levels divided 
            by total no of edges possible b/w the given trophic lvl.'''
        
        print(self.conn_dict)
        
     
     
    def log(self):
        
        f=open("log.txt", 'w')
        
        for key, val in self.conn_dict.items():           
            f.write(str(key)+"\t%6.5f\n" %(val))
        f.flush(); f.close()
    
            

obj=ConnectednessDet()
if __name__ == '__main__':
    obj.dura_mater()        
    