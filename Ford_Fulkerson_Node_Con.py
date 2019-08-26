# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 17:40:55 2019

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


class FordFulkerson_NodeConnectance(FordFulkerson):
    
    def __init__(self):
        
        os.chdir("../../")
        #Due to  __init__(self) in base class
        
        self.string="node_connectance"
        os.chdir(r"Machine_Readable_Data\Mult\Node-Connectance")
        self.config=[name for name in os.listdir("Set VI") if os.path.isdir(os.path.join("Set VI", name))]
        #Gets the names of all sub-directories in "Machine_Readable_Data\Mult\Connectance"
        #Change Set number for different connections, Also change it in inner_temple for read operations.
        os.chdir("../../../")
        
        self.min_edge_flowval=self.min_node_flowval= 100000
        self.max_edge_flowval=self.max_node_flowval= 0
        #Refer to Ford_Fulkerson.py (superclass) for details.
        
        self.storage_edge={}
        #A dict that will store interesting data on edge cuts
        self.storage_vex={}
        #A dict that will store interesting data on vertex cuts
        
        self.masterbinder0={}
        #Stores a continually updated version of the masterbinder data for 3D plotting (see trendsetter)
        
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
        
        
        
        self.intraconnectance={(0, 0): 0.0, (1, 1): 0.05, 
                               (2, 2): 0.027777777777777776, (2, 3): 0.11}
        #Used for normalisation.
        
        self.sd_node_cut=[]
        self.sd_node_flow_val=[]

        
    def inner_temple(self):
        
        self.intercon=[]
        #Stores the inter-connectance data.
        
        self.nodenum=[]
        #Stores the number of nodes in altered trophic level.
        
        for x in self.config:
            #Iterating over the different sub-directories.
            
            self.DirGraph=nex.read_graphml(r"Machine_Readable_Data\Mult\Node-Connectance\Set VI\%s\Connectance_NodeNum_Annotated.graphml" %(x))
            
            #Ascertaining the scaling factors
            p= x.find("_")
            y=float(x[p+1:])
            #Interconnectance values
            self.intercon.append(y)
            #Storing the interconnectance data of the current config here.
            
            f=open("Machine_Readable_Data/Mult/Node-Connectance/Set VI/%s/log_unabridged.txt" %(x), 'r')
            
            flag=0 #Used to determine altered level
            
            for l in f.readlines():
                if( l== "Number Of Nodes in Altered Trophic Level:\n"):
                    flag=1
                    continue
                if(flag==1):
                    self.nodenum.append(float(l.rstrip('\n')))
                    flag=0 #Changing back to the status quo.
                    
            #Changing to appropriate directory in results
            if(os.path.isdir("Results/Varying")==False):
                os.mkdir("Results/Varying")
            os.chdir("Results/Varying")
            
            if(os.path.isdir("Node-Connectance")==False):
                os.mkdir("Node-Connectance")
            os.chdir("Node-Connectance")
            
            if(os.path.isdir("Set VI")==False):
                os.mkdir("Set VI")
            os.chdir("Set VI")
            
            if(os.path.isdir(x)==False):
                os.mkdir(x)
            os.chdir(x)
            
            self.sanctum()
            
            self.DirGraph.clear()
            #Clearing the stables.
            
            os.chdir("../../../../")
            #Now in root directory, works as control has shifted to Set I directtory after execution of sanctum()
            print("Current working Directory:\t %s" %(os.getcwd()))
            
        
        #self.CSV_output()
        
        self.trend_plot()
        #Plotting a swift exit.
            
    
    
    def sanctum(self):
        
        trophiclvl=nex.get_node_attributes(self.DirGraph, 'trophic')
        
        for n in self.DirGraph.nodes():
            #Iterating through all the nodes.
            
            if(n != 's'):
                #Not sink
                
                '''The following function comes from FordFulkerson.py'''             
                self.min_edge_cut(n)
                
                if (trophiclvl[n] !=0):
                    #If producer, only way for it to go extinct is to remove the source or the producer itself.
                    self.node_trans(n)
                    self.min_node_cut(n)
                
        self.statistics()
        self.statistics_adv()
            
    def statistics_adv(self):
        
        print("MC Zulu")
        
        os.chdir("../../")
        #Now in Set VI Directory.
        
        if(os.path.isdir("Trends")==False):
            os.mkdir("Trends")
        os.chdir("Trends")
        #Changing the directory
        
        self.trend_setter()
        os.chdir("../")
        
    def trend_setter(self):
        
        tr=1
        #Trophic level being altered.
        
        if "Vertex ID" not in self.masterbinder0:
            self.masterbinder0['Vertex ID']=[]
            self.masterbinder0['Trophic Level']=[]
            self.masterbinder0['# of Edge Cuts']=[]
            self.masterbinder0['Capacity of Edge Cuts']=[]
            self.masterbinder0['# of Vertex Cuts']=[]
            self.masterbinder0['Capacity of Vertex Cuts']=[]
            self.masterbinder0["Node Number In Altered Level %d" %(tr)]=[]
            self.masterbinder0["Interconnectance"]=[]
            #Creating these entries in master-binder0 for first time
            
        self.masterbinder0['Vertex ID'].append(self.masterbinder['Vertex ID'])
        self.masterbinder0['Trophic Level'].append(self.masterbinder['Trophic Level'])
        self.masterbinder0['# of Edge Cuts'].append(self.masterbinder['# of Edge Cuts'])
        self.masterbinder0['Capacity of Edge Cuts'].append(self.masterbinder['Capacity of Edge Cuts'])
        self.masterbinder0['# of Vertex Cuts'].append(self.masterbinder['# of Vertex Cuts'])
        self.masterbinder0['Capacity of Vertex Cuts'].append(self.masterbinder['Capacity of Vertex Cuts'])
        
        for x in range(0, len(self.masterbinder['Vertex ID'])):
            self.masterbinder0["Node Number In Altered Level %d" %(tr)].append(self.nodenum[-1])
            # self.nodenum[-1] stores the value of the number of nodes in the altered level of the current graph.
            self.masterbinder0["Interconnectance"].append(self.intercon[-1])
        
        #Extened catalouging accomplished.
        
        
        top=max(self.masterbinder['Trophic Level'])
        
        edgecut_mean=[]; vercut_mean=[]; cap_edgeval_mean=[]; cap_verval_mean=[]
        edgecut_sd=[]; vercut_sd=[]; cap_edgeval_sd=[]; cap_verval_sd=[]
        
        '''Stores the means and standard deviations of the # Edge Cut, # Ver Cut, Capacity of Edge Cuts, 
        Capacity of Vertex Cuts data of self.masterbinder for a particular trophic level of a particular graph'''
        
        for t in range(0,top+1):
            
            edgecutnum=[]; vercutnum=[]; cap_edgeval=[]; cap_verval=[]
            #Resetting to default values before starting off on a new trophic level
            
            for x in range(0, len(self.masterbinder['Vertex ID'])):
             
                if (self.masterbinder['Trophic Level'][x]==t):
                    
                    edgecutnum.append(self.masterbinder['# of Edge Cuts'][x])
                    vercutnum.append(self.masterbinder['# of Vertex Cuts'][x])
                    cap_edgeval.append(self.masterbinder['Capacity of Edge Cuts'][x])
                    cap_verval.append(self.masterbinder['Capacity of Vertex Cuts'][x])
            
            norm= self.normalise(t, tr)     #Stores the normalisation constant.
            
            edgecutnum[:]= [y/norm for y in edgecutnum]
            vercutnum[:]= [y/norm for y in vercutnum]
            cap_edgeval[:]= [y/norm for y in cap_edgeval]
            cap_verval[:]= [y/norm for y in cap_verval]
            
            '''Normalises all the generated data. Note that intra-connection values are fixed.'''
            
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
        
        
    def normalise(self, t, tr):
        
        '''Normalises the data sent to it, t is the trophic level being normalised, 
            tr is the trophic level being altered'''
            
        maxi=20.0
        
        '''maxi stores the normalisation factor, which is the maximum number of edges possible b/w nodes present
        in the t th tropic level or lower (both intra-connections and inter-connections)'''
        
        if(tr== 0):
           maxi=self.nodenum[-1]
           #self.nodenum[-1] stores the number of nodes in the altered level.
           
        for i in range(0,t):
            '''Iterating over the trophic levels finding the inter-connections between the ith and i+1 th trophic levels
            as well the intra-connections in the i+1 th trophic level'''
            
            if (i== tr-1):
                # The i+1 th level has altered number of nodes.
                # Mapping inter-connections b/w the tr-1 and tr th level
                maxi= maxi + 20*self.nodenum[-1]*self.intercon[-1]*0.11
                #maxi= maxi+ 20*self.nodenum[-1]
                
                #Next the intra-connections in the tr th trophic level.
                maxi= maxi + self.nodenum[-1]*self.nodenum[-1]*self.intraconnectance[(tr,tr)]
                #maxi= maxi + self.nodenum[-1]*self.nodenum[-1]
                
                
            elif (i== tr):
                # Mapping inter-connections b/w the tr and tr +1 th level
                maxi= maxi+ self.nodenum[-1]*20*self.intercon[-1]*0.11
                
                #maxi= maxi+ self.nodenum[-1]*20
                
                # Mapping intra-connections in the tr+1 th level
                
                maxi= maxi+ 20*20*self.intraconnectance[(tr+1,tr+1)]
                
                #maxi= maxi +20*20
                
            else:
                #Mapping inter-connections
                maxi= maxi + 20*20*self.intercon[-1]*0.11
                
                #maxi= maxi + 20*20
                
                #Mapping intra-connections.
                maxi= maxi + 20*20*self.intraconnectance[i+1,i+1]
                
                #maxi= maxi + 20*20
        
        return maxi
    
    
    def trend_plot(self):         #Collates information.
        
        os.chdir("Results/Varying/Node-Connectance/Set VI/Trends")
        
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
        
        tr=1
        
        x= self.nodenum
        y= self.intercon
        
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
            ax.set_xlabel("Number of Nodes in Trophic Level %d" %(tr))
            ax.set_ylabel("Inter-connection Scaling Factor")
            ax.view_init(elev=20.0, azim=-30.0)
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
            ax.set_ylabel("Inter-connection Scaling Factor")
            ax.set_xlabel("Number of Nodes in Trophic Level %d" %(tr))
            #ax.set_zlabel("Avg Min Edge Cut Capacity of Tr Level %d.png" %(t))
            ax.view_init(elev=20.0, azim=-30.0)
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
            ax.set_ylabel("Inter-connection Scaling Factor")
            ax.set_xlabel("Number of Nodes in Trophic Level %d" %(tr))
            #ax.set_zlabel("Avg Min Node Cut Capacity of Tr Level %d.png" %(t))
            ax.view_init(elev=20.0, azim=-30.0)
            plt.savefig("Triangulation Avg Min Node Cut Capacity Tr Level %d.png" %(t), dpi=300)
            pickle.dump(fig, open("Rickle Pickle/Level %d Triangulation Avg Min Node Cut Capacity.pickle" %(t), 'wb'))
            plt.show()
            plt.close()
            
            
            
            # Avg node cut
            fig=plt.figure()
            ax = plt.axes(projection='3d')
            
            z=avg_node_cut[:,t] # Avg Node cuts for t th trophic level along z-axis.
            
            surf =ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')
            fig.colorbar(surf, shrink=0.5)
            ax.set_title("Avg # Node Cut Tr Level %d" %(t))
            ax.set_ylabel("Inter-connection Scaling Factor")
            ax.set_xlabel("Number of Nodes in Trophic Level %d" %(tr))
            ax.view_init(elev=20.0, azim=-30.0)
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
                ax.plot([x[p], x[p]], [y[p], y[p]], [z[p] + zerr[p], z[p] - zerr[p]], marker="_", markeredgecolor='k')
                
            ax.set_title("Avg # Edge Cut Tr Level %d" %(t))
            ax.set_xlabel("Number of Nodes in Trophic Level %d" %(tr))
            ax.set_ylabel("Inter-connection Scaling Factor")
            ax.view_init(elev=20.0, azim=-30.0)
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
            ax.set_xlabel("Number of Nodes in Trophic Level %d" %(tr))
            ax.set_ylabel("Inter-connection Scaling Factor")
            ax.view_init(elev=20.0, azim=-30.0)
            plt.savefig("Scatter Avg Min Edge Cut Capacity Tr Level %d.png" %(t), dpi=300)
            pickle.dump(fig, open("Rickle Pickle/Level %d Scatter Avg Min Edge Cut Capacity.pickle" %(t), 'wb'))
            plt.show()
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
            ax.set_xlabel("Number of Nodes in Trophic Level %d" %(tr))
            ax.set_ylabel("Inter-connection Scaling Factor")
            ax.view_init(elev=20.0, azim=-30.0)
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
            ax.set_xlabel("Number of Nodes in Trophic Level %d" %(tr))
            ax.set_ylabel("Inter-connection Scaling Factor")
            ax.view_init(elev=20.0, azim=-30.0)
            plt.savefig("Scatter # Node Cut Tr Level %d.png" %(t), dpi=300)
            pickle.dump(fig, open("Rickle Pickle/Level %d Scatter # Node Cut.pickle" %(t), 'wb'))
            plt.show()
            plt.close()
            
            
        os.chdir("../../../../../")
        print("Current working Directory:\t %s" %(os.getcwd()))
        
        
        
obj=FordFulkerson_NodeConnectance()
                
if __name__ == '__main__':
    obj.inner_temple()
                
        
        
        
        
        
            
        
        
        
        
        
        
        
                
                
            
            
            