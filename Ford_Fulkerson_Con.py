# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:33:16 2019

@author: Koustav
"""

import os
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import seaborn as sea
import networkx as nex
import copy
import pandas as pan
import numpy as np
import pickle
from Ford_Fulkerson import FordFulkerson

''' This program finds trophic stability results as a function of a varying network parameters called 
    connectance'''

class FordFulkerson_Connectance(FordFulkerson):
    
    def __init__(self):
        os.chdir("../../")
        #Due to  __init__(self) in base class
        os.chdir(r"Machine_Readable_Data\Mult\Connectance")
        self.config=[name for name in os.listdir("Set I") if os.path.isdir(os.path.join("Set I", name))]
        #Gets the names of all sub-directories in "Machine_Readable_Data\Mult\Connectance"
        #Change Set number for different connections, Also change it in inner_temple for read operations.
        os.chdir("../../../")
        
        self.min_edge_flowval=self.min_node_flowval= 100000
        self.max_edge_flowval=self.max_node_flowval= 0
        #Refer to Ford_Fulkerson.py (superclass) for details.
        
        self.avg_edge_cut=[]
        self.avg_edge_flow_val=[]
        '''Stores the avg # edge cut and avg flow values for each trophic level in a matrix, with different rows indicating different
           connectances and different columns representing different trophic levels'''
        
        self.avg_node_cut=[]
        self.avg_node_flow_val=[]
        
        self.sd_edge_cut=[]
        self.sd_edge_flow_val=[]
        '''Stores the standard dev (sd) of # edge cut and of flow values for each trophic level in a matrix, with different rows indicating 
           different connectances and different columns representing different trophic levels'''
        
        self.sd_node_cut=[]
        self.sd_node_flow_val=[]
        
        self.storage_edge={}
        #A dict that will store interesting data on edge cuts
        self.storage_vex={}
        #A dict that will store interesting data on vertex cuts
        
        self.string="connectance"
        
        self.r=0    #Used as a flag to denote first instantiation of self.trend_setter(), callable via self.sanctum()
        
        self.edgecutnum=[]; self.vercutnum=[]
        
    def inner_temple(self):
        #The door way to the sanctum.
        
        self.intracon=[]
        self.intercon=[]
        #Stores all the different intra-trophic and inter-trophic scaling factors respectively.
        
        
        self.intracol=[]
        self.intercol=[]
        #Stores the connectace data of normalised edge & vertex cuts. Check self.normalise()
        
        
        for x in self.config:
            #Iterating over the different sub-directories.
            
            self.DirGraph=nex.read_graphml(r"Machine_Readable_Data\Mult\Connectance\Set I\%s\Connectance_Annotated.graphml" %(x))
            
            #Ascertaining the scaling factors
            p= x.find("_")
            
            self.intercon.append(float(x[:p]))
            self.intracon.append(float(x[p+1:]))
            
            #Changing to appropriate directory in results
            if(os.path.isdir("Results/Varying")==False):
                os.mkdir("Results/Varying")
            os.chdir("Results/Varying")
            
            if(os.path.isdir("Connectance")==False):
                os.mkdir("Connectance")
            os.chdir("Connectance")
            
            if(os.path.isdir("Set I")==False):
                os.mkdir("Set I")
            os.chdir("Set I")
            
            if(os.path.isdir(x)==False):
                os.mkdir(x)
            os.chdir(x)
            
            
            self.sanctum()
            
            self.DirGraph.clear()
            #Clearing the stables.
            
            os.chdir("../../../../")
            #Now in root directory, works as control has shifted to Set I directtory after execution of sanctum()
            print("Current working Directory:\t %s" %(os.getcwd()))
            
            
        self.CSV_output()
        #Outputs trophic level data in readable CSV format. 
        
        self.trend_plot()
        #Plots the final trends
        
            
    def sanctum(self):
         
        trophiclvl=nex.get_node_attributes(self.DirGraph, 'trophic')
        i=0 #Used to provide a count
        for n in self.DirGraph.nodes():     
            if(n != 's'):
                #Not sink.
                self.min_edge_cut(n)
                if (trophiclvl[n] !=0):
                    #If producer, only way for it to go extinct is to remove the source or the producer itself.
                    self.node_trans(n)
                    self.min_node_cut(n)
                i+=1
        
        self.statistics()
        self.statistics_adv()
        print("Total number of iterations run:\t%d" %(i))
        
    def statistics_adv(self):       #Finds and presents more detailed insights into the generated data.
        print("MC Zulu")
        
        os.chdir("../../")
        #Now in Set I Directory.
        
        if(os.path.isdir("Trends")==False):
            os.mkdir("Trends")
        os.chdir("Trends")
        #Changing the directory
        
        self.trend_setter()
        os.chdir("../")
        
    def trend_setter(self):     #Collates information
        
        
        top=max(self.masterbinder['Trophic Level'])
        #Find max trophic level.
        
        if(self.r==0):
            #Used to find first instantiation of trend_setter()
            
            self.edgecutnum=[[] for t in range(0,top+1)]
            self.vercutnum=[[] for t in range(0,top+1)]
            self.cap_edgeval=[[] for t in range(0,top+1)]
            self.cap_verval=[[] for t in range(0,top+1)]
            
            #Creating the variables which will store the normalised data
            
            self.r=1 #Changing the flag
            
        
        edgecutnum=[]   
        '''Arrays storing information on # edge cuts ( & # node cuts) of a particular vertex in a particular config belonging
            to a particular trophic level'''
        vercutnum=[]
        
        cap_edgeval=[]
        cap_verval=[]
        ''' Arrays storing info on the capacities od edge & node cuts respectively, of a particular vertex in a particular
            config belonging to a particular trophic level'''
            
        edgecut_mean=[]; vercut_mean=[]; cap_edgeval_mean=[]; cap_verval_mean=[]
        edgecut_sd=[]; vercut_sd=[]; cap_edgeval_sd=[]; cap_verval_sd=[];
        
        
        for t in range(0,top+1):
            #Iterating through the trophic levels
            
            edgecutnum=[]; vercutnum=[]; cap_edgeval=[]; cap_verval=[]
            #Resetting to default values before starting off on a new trophic level
            
            for x in range(0, len(self.masterbinder['Vertex ID'])):
                #Iterating through all the nodes
                if( self.masterbinder['Trophic Level'][x]==t):
                                                        
                    edgecutnum.append(self.masterbinder['# of Edge Cuts'][x])
                    vercutnum.append(self.masterbinder['# of Vertex Cuts'][x])
                    cap_edgeval.append(self.masterbinder['Capacity of Edge Cuts'][x])
                    cap_verval.append(self.masterbinder['Capacity of Vertex Cuts'][x])
            
            
            self.normalise( t, edgecutnum, vercutnum, cap_edgeval, cap_verval)       
            '''Normalises edgecutnum, vercutnum, cap_edgeval, cap_verval'''
            
            '''WARNING! ASSUMES that the artificial net has 20-20-20-... symmetric structure.
               Normalisation uses the total number of possible connections in a preceding level as the normalisation factor'''
            
            #Determination of mean and SD of four matrices determined above.
            
            edgecut_mean.append(np.mean(edgecutnum, dtype=np.float64))
            vercut_mean.append(np.mean(vercutnum, dtype=np.float64))
            cap_edgeval_mean.append(np.mean(cap_edgeval, dtype=np.float64))
            cap_verval_mean.append(np.mean(cap_verval, dtype=np.float64))
            
            #These store the means for # edge cuts etc as a row where each element indicates a given trophic level.
            
            edgecut_sd.append(np.std(edgecutnum, dtype=np.float64, ddof=1))
            vercut_sd.append(np.std(vercutnum, dtype=np.float64, ddof=1))
            cap_edgeval_sd.append(np.std(cap_edgeval, dtype=np.float64, ddof=1))
            cap_verval_sd.append(np.std(cap_verval, dtype=np.float64, ddof=1))
            
            #These store the standard deviations for # edge cuts etc as a row where each element indicates a given trophic level.
            
            print("Edge Cut Number: "+str(edgecutnum))
            print("Length of Edge Cut Number: "+str(len(edgecutnum)))
            print("Edge Cut Number SD: "+str(np.std(edgecutnum, dtype=np.float64, ddof=1)))
            
            
            
            
        
        self.avg_edge_cut.append(edgecut_mean)  
        self.avg_edge_flow_val.append(cap_edgeval_mean)
        
        self.avg_node_cut.append(vercut_mean)
        self.avg_node_flow_val.append(cap_verval_mean)
        

        #Refer to __init__()
        
        self.sd_edge_cut.append(edgecut_sd)  
        self.sd_edge_flow_val.append(cap_edgeval_sd)
        
        self.sd_node_cut.append(vercut_sd)
        self.sd_node_flow_val.append(cap_verval_sd)
        
        
    def normalise(self, t, edgecutnum, vercutnum, cap_edgeval, cap_verval):   
        
        '''WARNING! ASSUMES that the artificial net has 20-20-20-... symmetric structure.'''
        
        i=len(self.intracon)-1 # Last ( & current ) index of latent self.intracon/self.intercon
        
        #Determining normalisztion factor (maxi) which is maximim number of edges possible at or below the level.
        
        maxi=20.0
        
        for p in range(0,t):
            maxi= maxi+ self.intercon[i]*20*20*0.11
            
            if(p==0):
                #t=1 exists, i.e. there is at least trophic level one in the system.
                maxi= maxi+ self.intracon[i]*20*20*0.05
            elif(p==1):
                #t=2 exists. Accounting for all possible (2,2) connections.
                maxi= maxi+self.intracon[i]*20*20*0.027
                
        edgecutnum[:]=[x/maxi for x in edgecutnum]
        vercutnum[:]=[x/maxi for x in vercutnum]
        cap_edgeval[:]=[x/maxi for x in cap_edgeval]
        cap_verval[:]=[x/maxi for x in cap_verval]
        
        #Normalising edgecutnum, vercutnum,cap_edgeval, cap_verval
                
        
        #Arrays whose different rows store all the normalised information about trophic levels 0,1,2
        
        self.edgecutnum[t].extend(edgecutnum)
        self.vercutnum[t].extend(vercutnum)
        self.cap_edgeval[t].extend(cap_edgeval)
        self.cap_verval[t].extend(cap_verval)
                
        if(t==0):
            #We create one inter=col and intra-col that we use for all the different trophic levels.
            for p in range(0,len(edgecutnum)):
                #Adding the same number of entries as aove to the columns storing intra-connectance and inter-connectance
                self.intracol.append(self.intracon[i])
                self.intercol.append(self.intercon[i])
            
        
    def CSV_output(self):   #Outputting trophic data in machine readable format.
        
        top=max(self.masterbinder['Trophic Level'])
        #Find max trophic level.
        
        os.chdir("Results/Varying/Connectance/Set I/Trends")
        if os.path.isdir("Trophic Data")==False:
            os.mkdir("Trophic Data")
        os.chdir("Trophic Data")
        
        for k in range(0,top+1):
        
            output=np.zeros([len(self.edgecutnum[k]),6])
        
            output[:,0]=self.intercol #First column stores the interconnectance data.
            output[:,1]=self.intracol #Second column stores the intra-connectance data.
            output[:,2]=self.edgecutnum[k]     #Third column stores the normalised # edge cut data of kth trophic lvl.
            output[:,3]=self.vercutnum[k]     #Third column stores the normalised # ver cut data of kth trophic lvl.
            output[:,4]=self.cap_edgeval[k]     #Third column stores the min capacity edge cut data of kth trophic lvl.
            output[:,5]=self.cap_verval[k]     #Third column stores the min capacity vertex cut data of kth trophic lvl.
            
            np.savetxt('Trp Lvl %d.csv' %(k), output, delimiter=",", header="Interconnectance SF, Intraconnectance SF, # Edge Cut, # Ver Cut, Min Cap of Edge Cut, Min Cap of Ver Cut")
        
        os.chdir("../../../../../../")
            
            
        
    def trend_plot(self): #Plotting various metrics of different distributions
        
        os.chdir("Results/Varying/Connectance/Set I/Trends")
        
        #print("SELF Avg Edge Cut: "+str(self.avg_edge_cut))
        
        if(os.path.isdir("Rickle Pickle")==False):
                os.mkdir("Rickle Pickle")
        #Stores pcikle data.
        
        avg_edge_cut=np.array(self.avg_edge_cut)
        avg_node_cut=np.array(self.avg_node_cut)
        avg_edge_flow_val=np.array(self.avg_edge_flow_val)
        avg_node_flow_val=np.array(self.avg_node_flow_val)
        
        #Switching to Numpy format for easy indexing.
        
        sd_edge_cut=np.array(self.sd_edge_cut)
        sd_node_cut=np.array(self.sd_node_cut)
        sd_edge_flow_val=np.array(self.sd_edge_flow_val)
        sd_node_flow_val=np.array(self.sd_node_flow_val)
        
        print("Avg Edge Cut: "+str(avg_edge_cut))
        print("Avg Node Cut: "+str(avg_node_cut))
        
        print("SD of Edge Cut: "+str(sd_edge_cut))
        print("SD of Node Flow Val: "+str(sd_node_flow_val))
        
        top=max(self.masterbinder['Trophic Level'])
        
        x=self.intercon         #Interconnections along x-axis
        y=self.intracon         #Intraconnections along y-axis.
        
        for t in range(0,top+1):
            #Plotting as per trophic level.
            
            
            '''Below you have triangulation plots followed by scatter plots of the various parameters determined above
               such as avg_edge_cut etc for different trophic levels seperately'''
            
            fig=plt.figure()
            ax = plt.axes(projection='3d')
            
            z=avg_edge_cut[:,t] # Avg Edge cuts for t th trophic level along z-axis.
            
            surf =ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')
            fig.colorbar(surf, shrink=0.5)
            ax.set_title("Avg # Edge Cut Tr Level %d" %(t))
            ax.set_xlabel("Inter-connections")
            ax.set_ylabel("Intra-connections")
            plt.savefig("Triangulation # Edge Cut Tr Level %d.png" %(t), dpi=300)
            pickle.dump(fig, open("Rickle Pickle/Level %d Triangulation # Edge Cut.pickle" %(t), 'wb'))
            plt.show()
            plt.close()
            
                
            #Avg min edge-cut capacity
            fig=plt.figure()
            ax = plt.axes(projection='3d')
            
            z=avg_edge_flow_val[:,t] # Avg edge-cut capacity for t th trophic level along z-axis.
            
            surf =ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')
            fig.colorbar(surf, shrink=0.5)
            ax.set_title("Avg Edge Max Flow Val Tr Level %d" %(t))
            ax.set_xlabel("Inter-connections")
            ax.set_ylabel("Intra-connections")
            plt.savefig("Triangulation Avg Min Edge Cut Capacity Tr Level %d.png" %(t), dpi=300)
            pickle.dump(fig, open("Rickle Pickle/Level %d Triangulation Avg Min Edge Cut Capacity.pickle" %(t), 'wb'))
            plt.show()
            plt.close()
            
            
            
            #Avg min node-cut capacity
            fig=plt.figure()
            ax = plt.axes(projection='3d')
            
            z=avg_node_flow_val[:,t] # Avg min node-cut capacity for t th trophic level along z-axis.
            
            surf =ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')
            fig.colorbar(surf, shrink=0.5)
            ax.set_title("Avg Node Max Flow Val Level %d" %(t))
            ax.set_xlabel("Inter-connections")
            ax.set_ylabel("Intra-connections")
            plt.savefig("Triangulation Avg Min Node Cut Capacity Tr Level %d.png" %(t), dpi=300)
            pickle.dump(fig, open("Rickle Pickle/Level %d Triangulation Avg Min Node Cut Capacity.pickle" %(t), 'wb'))
            plt.close()
            
            
            
            # Avg node cut
            fig=plt.figure()
            ax = plt.axes(projection='3d')
            
            z=avg_node_cut[:,t] # Avg Node cuts for t th trophic level along z-axis.
            
            surf =ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')
            fig.colorbar(surf, shrink=0.5)
            ax.set_title("Avg # Node Cut Tr Level %d" %(t))
            ax.set_xlabel("Inter-connections")
            ax.set_ylabel("Intra-connections")
            plt.savefig("Triangulation # Node Cut Tr Level %d.png" %(t), dpi=300)
            pickle.dump(fig, open("Rickle Pickle/Level %d Triangulation # Node Cut.pickle" %(t), 'wb'))
            plt.show()
            plt.close()
            
            
            
            '''Plotting the scatter plots with error bars'''
            
            
            
            
            fig=plt.figure()
            ax = plt.axes(projection='3d')
            
            z=avg_edge_cut[:,t] # Avg Edge cuts for t th trophic level along z-axis.
            zerr= sd_edge_cut[:,t]      #Corresponding SD
            
            ax.scatter(x, y, z, c=z, cmap='viridis', linewidth=0.5)
            
            for p in range(0,len(self.intercon)):
                #Plotting SD bars
                ax.plot([x[p], x[p]], [y[p], y[p]], [z[p] + zerr[p], z[p] - zerr[p]], marker="_", markerfacecolor='k')
                
            ax.set_title("Avg # Edge Cut Tr Level %d" %(t))
            ax.set_xlabel("Inter-connections")
            ax.set_ylabel("Intra-connections")
            plt.savefig("Scatter # Edge Cut Tr Level %d.png" %(t), dpi=300)
            pickle.dump(fig, open("Rickle Pickle/Level %d Scatter # Edge Cut.pickle" %(t), 'wb'))
            plt.show()
            plt.close()
            
                
            #Avg min edge-cut capacity
            fig=plt.figure()
            ax = plt.axes(projection='3d')
            
            z=avg_edge_flow_val[:,t] # Avg Max Edge Flow Val for t th trophic level along z-axis.
            zerr= sd_edge_flow_val[:,t]      #Corresponding SD
            
            ax.scatter(x, y, z, c=z, cmap='viridis', linewidth=0.5)
            
            for p in range(0,len(self.intercon)):
                #Plotting SD bars
                ax.plot([x[p], x[p]], [y[p], y[p]], [z[p] + zerr[p], z[p] - zerr[p]], marker="_", markerfacecolor='k')
                
            ax.set_title("Avg Edge Max Flow Val Level %d" %(t))
            ax.set_xlabel("Inter-connections")
            ax.set_ylabel("Intra-connections")
            plt.savefig("Scatter Avg Min Edge Cut Capacity Tr Level %d.png" %(t), dpi=300)
            pickle.dump(fig, open("Rickle Pickle/Level %d Scatter Avg Min Edge Cut Capacity.pickle" %(t), 'wb'))
            plt.close()
            
            
            
            
            #Avg min node-cut capacity
            fig=plt.figure()
            ax = plt.axes(projection='3d')
            
            z=avg_node_flow_val[:,t] # Avg Max Edge Flow Val for t th trophic level along z-axis.
            zerr= sd_node_flow_val[:,t]      #Corresponding SD
            
            ax.scatter(x, y, z, c=z, cmap='viridis', linewidth=0.5)
            
            for p in range(0,len(self.intercon)):
                #Plotting SD bars
                ax.plot([x[p], x[p]], [y[p], y[p]], [z[p] + zerr[p], z[p] - zerr[p]], marker="_", markerfacecolor='k')
                
            ax.set_title("Avg Node Max Flow Val Level %d" %(t))
            ax.set_xlabel("Inter-connections")
            ax.set_ylabel("Intra-connections")
            plt.savefig("Scatter Avg Min Node Cut Capacity Tr Level %d.png" %(t), dpi=300)
            pickle.dump(fig, open("Rickle Pickle/Level %d Scatter Avg Min Node Cut Capacity.pickle" %(t), 'wb'))
            plt.show()
            plt.close()
            
            
            # Avg node cut
            fig=plt.figure()
            ax = plt.axes(projection='3d')
            
            z=avg_node_cut[:,t] # Avg Edge cuts for t th trophic level along z-axis.
            zerr= sd_node_cut[:,t]      #Corresponding SD
            
            ax.scatter(x, y, z, c=z, cmap='viridis', linewidth=0.5)
            
            for p in range(0,len(self.intercon)):
                #Plotting SD bars
                ax.plot([x[p], x[p]], [y[p], y[p]], [z[p] + zerr[p], z[p] - zerr[p]], marker="_", markerfacecolor='k')
                
            ax.set_title("Avg # Node Cut Tr Level %d" %(t))
            ax.set_xlabel("Inter-connections")
            ax.set_ylabel("Intra-connections")
            plt.savefig("Scatter # Node Cut Tr Level %d.png" %(t), dpi=300)
            pickle.dump(fig, open("Rickle Pickle/Level %d Scatter # Node Cut.pickle" %(t), 'wb'))
            plt.show()
            plt.close()
            
            
        os.chdir("../../../../../")
        print("Current working Directory:\t %s" %(os.getcwd()))
        
            
        

obj=FordFulkerson_Connectance()
                
if __name__ == '__main__':
    obj.inner_temple()
            