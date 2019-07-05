# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 13:19:51 2019

@author: Koustav
"""

import os
import matplotlib.pyplot as plt
import seaborn as sea
import networkx as nex
import copy
import pandas as pan
import numpy as np
from Ford_Fulkerson import FordFulkerson

''' This program finds trophic stability results as a function of some varying networkk paraeter such as node ratio, 
    connectance or total number of nodes'''

class FordFulkerson_Iterable(FordFulkerson):
    
    def __init__(self):
        os.chdir("../../")
        #Due to  __init__(self) in base class
        os.chdir(r"Machine_Readable_Data\Mult\Node Distribution")
        self.config=[name for name in os.listdir("Set II") if os.path.isdir(os.path.join("Set II", name))]
        #Gets the names of all sub-directories in "Machine_Readable_Data\Mult\Node Distribution"
        #Change Set number for different distributions, Also change itin inner_temple for read operations.
        os.chdir("../../../")
        
        self.min_edge_flowval=self.min_node_flowval= 100000
        self.max_edge_flowval=self.max_node_flowval= 0
        #Refer to Ford_Fulkerson.py (superclass) for details.
        
        self.avg_edge_cut=[]
        self.avg_edge_flow_val=[]
        '''Stores the avg # edge cut and avg flow values for each trophic level in a matrix, with different rows indicating different node
           node distributions and different columns representing different trophic levels'''
        
        self.avg_node_cut=[]
        self.avg_node_flow_val=[]
        
        self.storage_edge={}
        #A dict that will store interesting data on edge cuts
        self.storage_vex={}
        #A dict that will store interesting data on vertex cuts
    
    def inner_temple(self):
        #The doorway to the sanctum
        
        self.config_list=[] #Stores all the different node distributions iterated over (each distribution a row)
        
        for x in self.config:
            self.DirGraph=nex.read_graphml(r"Machine_Readable_Data\Mult\Node Distribution\Set II\%s\%s_Annotated.graphml" %(x, x))            
            f=open(r"Machine_Readable_Data\Mult\Node Distribution\Set II\%s\log_unabridged.txt" %(x))
            self.string=x
            #All names to be based on this.
            #Storing the node distribution in self.config_list
            flag=0  
            a=[]
            for l in f.readlines():
                if( l== "Node Distribution:\n"):
                    flag=1
                    continue
                if(flag==1):
                    a.append(float(l.rstrip('\n')))
            self.config_list.append(a)
            
            #Changing to appropriate directory in results
            if(os.path.isdir("Results\Varying")==False):
                os.mkdir("Results\Varying")
            os.chdir("Results\Varying")
            
            if(os.path.isdir("Node Distribution")==False):
                os.mkdir("Node Distribution")
            os.chdir("Node Distribution")
            
            if(os.path.isdir("Set II")==False):
                os.mkdir("Set II")
            os.chdir("Set II")
            
            if(os.path.isdir(x)==False):
                os.mkdir(x)
            os.chdir(x)
            
            
            self.sanctum()
            
            self.DirGraph.clear()
            #Clearing the stables.
            
            os.chdir("../../../../")
            #Now in root directory
            print("Current working Directory:\t %s" %(os.getcwd()))
        
        print(self.config_list)
        print("Iterations run:\t%d" %(len(self.config)))
        
        self.trend_plot()
        #Plotting the results of the final distribution.
            
        
    def sanctum(self): #Pia mater. The nerve centre.
        
        trophiclvl=nex.get_node_attributes(self.DirGraph, 'trophic')
        i=0 #Used to provide stop-line services
        for n in self.DirGraph.nodes():     
            if(n != 's'):
                #Not sink or producers
                self.min_edge_cut(n)
                if (trophiclvl[n] !=0):
                    #If producer, only way for it to go extinct is to remove the source or the producer itself.
                    self.node_trans(n)
                    self.min_node_cut(n)
                
            if(i%200==0):
                #Provides a stop-line after every 200 iterations
                inp=input("This is a stop-line. Press any key to continue.\n")
            
            i+=1
        self.statistics()
        self.statistics_adv()
        print("Total number of iterations run:\t%d" %(i))
        
    def statistics_adv(self):       #Finds and presents more detailed insights into the generated data.
        print("MC Zulu")
        
        os.chdir("../../")
        #Now in Set II Directory.
        
        if(os.path.isdir("Trends")==False):
            os.mkdir("Trends")
        os.chdir("Trends")
        #Changing the directory
        
        self.trend_setter()
        os.chdir("../")
        
    def trend_setter(self):     #Collates information
        
        trophiclvl=nex.get_node_attributes(self.DirGraph, 'trophic')
        
        top=max(list(trophiclvl.values())) #Finds max trophic value
        
        stat=open("Adv_Stat_Log_%s.txt" %(self.string), 'w')
        
        edge_row=[]
        edgeflow_row=[]
        '''Stores the row data for avg_edge_cut and  avg_edge_flow_val matrices (i.e the trophic level data for a given 
         distribution)'''
        
        node_row=[]
        nodeflow_row=[]
        
        trp_num=0
        edgecut_sum=0.0
        edgeflow_val_sum=0.0
        for v in list(self.DirGraph.nodes()):
            
            if (trophiclvl[v]==0):
                #Iterating through species in the 0th trophic level.
                trp_num+=1
                ops=copy.copy(self.storage_edge[v])
                # black ops stores all the data related to min edge cut of graph with sink 'v'
                edgeflow_val= ops.pop()
                edgecut_sum += len(ops)
                edgeflow_val_sum += edgeflow_val
        
        edge_row.append(float(edgecut_sum/trp_num))
        edgeflow_row.append(float(edgeflow_val_sum/trp_num))
        node_row.append(0)
        nodeflow_row.append(0)
        #For 0 Trophic level there are no valid node cuts.
        
        avg_edge_cut= float(edgecut_sum/trp_num)
        avg_flow_val= float(edgeflow_val_sum/trp_num)
        
        print("Number of species in 0th Trophic Level:\t%d\n" %(trp_num))
        stat.write("Number of species in 0th Trophic Level:\t%2.0f\n\n" %(trp_num))
        print("Average size of edge-cut in 0th Trophic Level:\t%5.3f" %(avg_edge_cut))
        stat.write("Average size of edge-cut in 0th Trophic Level:\t%5.3f\n" %(avg_edge_cut))
        print("Average flow-value (capacity) of edge-cut in 0th Trophic Level:\t%5.3f" %(avg_flow_val))
        stat.write("Average flow-value (capacity) of edge-cut in 0th Trophic Level:\t%8.4f\n" %(avg_flow_val))
        
        stat.write("\t\t\t***\n")
        print("\t\t\t***\n")
        
        
        for trp in range(1,top+1):
            #Iterating through all trophic levels from 1 to top.
            trp_num=0
            #Number of species in a given trophic level.
            edgecut_sum= vercut_sum = 0.0
            edgeflow_val_sum= verflow_val_sum= 0.0
            
            for v in list(self.DirGraph.nodes()):
                #Iterating through all vertices.
                if (trophiclvl[v]==trp):
                    trp_num+=1  
                    ops_ee=copy.copy(self.storage_edge[v])
                    ops_v=copy.copy(self.storage_vex[v])
                    # black ops stores all the data related to min edge & vertex cut of graph with sink 'v'
                    edgeflow_val= ops_ee.pop()
                    verflow_val=ops_v.pop()
                    
                    edgecut_sum += len(ops_ee)
                    edgeflow_val_sum += edgeflow_val
                    #Calculating statistics of edge cut
                    vercut_sum += len(ops_v)
                    verflow_val_sum += verflow_val
                    #Calculating statistics of vertex cut
            
            avg_edge_cut= float(edgecut_sum/trp_num)
            avg_edge_flow_val= float(edgeflow_val_sum/trp_num)
            avg_node_cut= float(vercut_sum/trp_num)
            avg_node_flow_val= float(verflow_val_sum/trp_num)
            
            edge_row.append(avg_edge_cut)
            edgeflow_row.append(avg_edge_flow_val)
            node_row.append(avg_node_cut)
            nodeflow_row.append(avg_node_flow_val)
            
            
            print("Number of species in %dth Trophic Level:\t%d\n" %(trp, trp_num))
            stat.write("Number of species in %dth Trophic Level:\t%2.0f\n\n" %(trp, trp_num))
            print("Average size of edge-cut in %dth Trophic Level:\t%5.3f" %(trp, avg_edge_cut))
            stat.write("Average size of edge-cut in %dth Trophic Level:\t%5.3f\n" %(trp, avg_edge_cut))
            print("Average flow-value (capacity) of edge-cut in %dth Trophic Level:\t%5.3f\n" %(trp, avg_edge_flow_val))
            stat.write("Average flow-value (capacity) of edge-cut in %dth Trophic Level:\t%8.4f\n\n" %(trp, avg_edge_flow_val))
            
            print("Average size of vertex-cut in %dth Trophic Level:\t%5.3f" %(trp, avg_node_cut))
            stat.write("Average size of vertex-cut in %dth Trophic Level:\t%5.3f\n" %(trp, avg_node_cut))
            print("Average flow-value (capacity) of vertex-cut in %dth Trophic Level:\t%5.3f\n" %(trp, avg_node_flow_val))
            stat.write("Average flow-value (capacity) of vertex-cut in %dth Trophic Level:\t%8.4f\n" %(trp, avg_node_flow_val))
            
            stat.write("\t\t\t***\n")
            
        
        self.avg_edge_cut.append(edge_row)
        self.avg_edge_flow_val.append(edgeflow_row)
        '''Updating the node distribution data matrices (refer to __init__() for more details'''
        
        self.avg_node_cut.append(node_row)
        self.avg_node_flow_val.append(nodeflow_row)
        
        stat.flush(); stat.close()
        
        
        self.storage_edge={}
        self.storage_vex={}
        
    
    def trend_plot(self): #Plotting various  metrics of different distributions
        
        avg_edge_cut=np.array(self.avg_edge_cut)
        avg_edge_flow_val=np.array(self.avg_edge_flow_val)
        avg_node_cut=np.array(self.avg_node_cut)
        avg_node_flow_val=np.array(self.avg_node_flow_val)
        
        config_list=np.array(self.config_list)
        #Rewriting variables as np arrays for easier iterations.
        
        os.chdir("Results/Varying/Node Distribution/Set II/Trends")
        
        x ,y = config_list.shape #Gives dimensions of the arrays.
        
        print("Average Edge Cut:")
        print(avg_edge_cut)
        print("Average Vertex Cut:")
        print(avg_node_cut)
        print("Config List:")
        print(config_list)
        
        for x in range(0, y):
            #Iterating over the different trophic levels.
            
            plt.plot(config_list[:,1], avg_edge_cut[:,x], marker='o', markerfacecolor='none', 
                     label="Avg number of # Edge cuts to disconnect Tr %d" %(x))
            plt.plot(config_list[:,1], avg_node_cut[:,x],  marker='o', markerfacecolor='none', 
                     label="Avg number of # Node cuts to disconnect Tr %d" %(x))
        plt.xlabel("Node Distribution of Trophic Level 1 (Primary Consumers)")
        plt.ylabel("Number of cuts")
        plt.legend()
        plt.savefig("One.png", dpi=300)
        plt.show()
        plt.clf()
        plt.close()
        
        for x in range(0, y):
            #Iterating over the different trophic levels.
            
            plt.plot(config_list[:,1], avg_edge_flow_val[:,x],  marker='o', markerfacecolor='none', 
                     label="Avg flow value of Edge cuts to disconnect Tr %d" %(x))
            plt.plot(config_list[:,1], avg_node_flow_val[:,x], marker='o', markerfacecolor='none',
                     label="Avg Flow val of Node cuts to disconnect Tr %d" %(x))
        plt.xlabel("Node Distribution of Trophic Level 1 (Primary Consumers)")
        plt.ylabel("Number of cuts")
        plt.legend()
        plt.savefig("Two.png", dpi=300)
        plt.show()
        plt.clf()
        plt.close()
            
        os.chdir("../../../../")
        print("Current working Directory:\t %s" %(os.getcwd()))
        
    
    
obj=FordFulkerson_Iterable()
                
if __name__ == '__main__':
    obj.inner_temple()