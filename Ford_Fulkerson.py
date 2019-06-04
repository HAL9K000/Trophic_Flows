# -*- coding: utf-8 -*-
"""
Created on Fri May 31 12:51:59 2019

@author: Koustav
"""


import os
import matplotlib.pyplot as plt
import seaborn as sea
import networkx as nex
import copy
import pandas as pan


class FordFulkerson:
    
    def __init__(self):
        
        self.string = "fw_coachella"
        self.DirGraph=nex.read_graphml("Machine_Readable_Data\%s\%s_Annotated.graphml" %(self.string, self.string))
        self.min_edge_flowval=self.min_node_flowval= 100000
        self.max_edge_flowval=self.max_node_flowval= 0
        #Stores the min and max flow values of edge and vertex cuts out of all 65 possibilities.
        self.min_cap_e= self.max_cap_e=[] #Stores corresponding target node.
        self.min_cap_n= self.max_cap_n=[]
        
        self.storage_edge={}
        #A dict that will store interesting data on edge cuts
        self.storage_vex={}
        #A dict that will store interesting data on vertex cuts
        
        if(os.path.isdir("Results\%s" %(self.string))==False):
            os.mkdir("Results\%s" %(self.string))
        os.chdir("Results\%s" %(self.string))
        
        
        
    def sanctum(self):
        print(self.DirGraph.nodes())
        trophiclvl=nex.get_node_attributes(self.DirGraph, 'trophic')
        i=0 #Used to provide stop-line services
        for n in self.DirGraph.nodes():     
            if(n != 's'):
                #Not sink or producers
                self.min_edge_cut(n)
                if (trophiclvl[n] !=0):
                    #If producer, only way for it to go extinct is to remove the source or theprducer itself.
                    self.node_trans(n)
                    self.min_node_cut(n)
                
            if(i%19==0):
                #Provides a stop-line after every fifteen iterations
                inp=input("This is a stop-line. Press any key to continue.\n")
            
            i+=1
        self.statistics()
        self.statistics_adv()
        print("Total number of iterations run:\t%d" %(i))
    
    
    def min_edge_cut(self, n):      #Performing an edge cut, and storing the data about it.
        
        if(os.path.isdir("TargetNode-%3d" %(int(n)))==False):
            os.mkdir("TargetNode-%3d" %(int(n)))
        os.chdir("TargetNode-%3d" %(int(n)))
        #Changing the directory
        
        f=open('edgecut_log.txt', 'w')
        
        cut_val, partitions = nex.minimum_cut(self.DirGraph, 's', n)
        
        print("Max Flow Value:\t%d" %(int(cut_val)))
        print("Set of nodes in the 's' partition: " + str(partitions[0]))
        print("Set of nodes in the 't' partition: " + str(partitions[1]))
        
        f.write("Max Flow Value:\t%d\n" %(int(cut_val)))
        edge_cut=[]
        for p1_node in partitions[0]:
            for p2_node in partitions[1]:
                if self.DirGraph.has_edge(p1_node,p2_node):
                    edge_cut.append((p1_node,p2_node))
        
        print("Edges of the cut: " + str(edge_cut))
        f.write("Edge Cut:\n")
        f.write(str(edge_cut))
        f.flush(); f.close()
        
        self.NDiGraph= copy.deepcopy(self.DirGraph)
        # Creating a deep copy of self.DirGraph  To Store Cut Edge Data
        
        self.NDiGraph.nodes[n]['colour']='red'
        # Colour coding sink
        
        for x in list(self.NDiGraph.edges()):
            if x in edge_cut:
                print("Rose")
                #This is an edge that got cut in Min-cut.
                self.NDiGraph[x[0]][x[1]]['colour']='red'
        
        nex.write_graphml(self.NDiGraph, '%s_Tar_%d_Col.graphml' %(self.string, int(n)))
        #Outputting colour coded graph in graphml format.
        self.NDiGraph.remove_edges_from(edge_cut)
        nex.write_graphml(self.NDiGraph, '%s_Tar_%d_EdgeCut.graphml' %(self.string, int(n)))
        
        os.chdir("../")
        
        if(cut_val<self.min_edge_flowval):
            #In case of encountering min capacity of cut out of 65 cuts.
            self.min_edge_flowval=cut_val
            self.min_cap_e=[n]
        
        elif(cut_val==self.min_edge_flowval):
            #In case of a tie
            self.min_edge_flowval=cut_val
            self.min_cap_e.append(n)
            
        if(cut_val>self.max_edge_flowval):
            #In case of encountering max capacity of cut out of 65 cuts.
            self.max_edge_flowval=cut_val
            self.max_cap_e=[n]
            
        elif(cut_val == self.max_edge_flowval):
            #In case of a tie.
            self.max_edge_flowval=cut_val
            self.max_cap_e.append(n)
            
        temp=edge_cut
        temp.append(cut_val)
        self.storage_edge[n]=temp
        
        #Storage_edge stores the edge cut tuples of a given target (key) followed by the capacity of the cut.
            
        self.NDiGraph.clear()       #Clear copy
        
        
    def node_trans(self, n):      #Converts graph to node capacity representation.
       
        if(os.path.isdir("TargetNode-%3d" %(int(n)))==False):
            os.mkdir("TargetNode-%3d" %(int(n)))
        os.chdir("TargetNode-%3d" %(int(n)))
        #Changing the directory
        
        
        self.NDiGraph= copy.deepcopy(self.DirGraph)
        # Creating a deep copy of self.DirGraph  for Node Transformation.
        for (n1, n2, d) in self.NDiGraph.edges(data=True):
            #Removing all edge attributes from copy
            d.clear()
            
        self.NDiGraph.nodes[n]['colour']='red'
        # Colour coding sink
        
        
        #Splitting nodes and linking them approriately to apply Ford Fulkerson for min vertex cut
            
        trophiclvl=nex.get_node_attributes(self.NDiGraph,'trophic')
        ncap= nex.get_node_attributes(self.NDiGraph,'node_cap')
        for v in list(self.DirGraph.nodes()):
            if(v != 's' and v != n):
                        # We don't want to split the 's' or 't' nodes
                        p= v+'_duo'
                        self.NDiGraph.add_node(p)
                        #Creating sister node of v
                        edge_val= ncap[v]
                        
                        suc=list(self.NDiGraph.successors(v))
                        print("The node:\t%s" %(v))
                        print("The node:\t%s" %(str(suc)))
                        for x in suc:
                            #Choosing all successors of v
                            if(x != v):
                                #We are removing self-loops if any.
                                self.NDiGraph.add_edge(p,x)
                            #Adding edges between p and x
                            self.NDiGraph.remove_edge(v,x)
                            #Removing outward edges from v to x
                        
                        self.NDiGraph.add_edge(v,p, capacity=edge_val)
                        #Adding edge b/w n and p with capacity = node_capacity
                        self.NDiGraph.nodes[p]['trophic']=trophiclvl[v]
                        #Assigning the same trophic value to clone of v.
        
    
    def min_node_cut(self,n):       #Find min vertex cut and store data about it.
        
        print("Target Node:\t"+str(n))
        
        cut_val, partitions = nex.minimum_cut(self.NDiGraph, 's', n)
        
        
        print("Max Flow Value:\t%d" %(int(cut_val)))
        print("Set of nodes in the 's' partition: " + str(partitions[0]))
        print("Set of nodes in the 't' partition: " + str(partitions[1]))
        edge_cut=[]
        for p1_node in partitions[0]:
            for p2_node in partitions[1]:
                if self.NDiGraph.has_edge(p1_node,p2_node):
                    edge_cut.append((p1_node,p2_node))
        
        print("Edges of the cut: " + str(edge_cut))
        
        #Catalouging the properties of the node cut.
        
        f=open('nodecut_log.txt', 'w')
        f.write("Max Flow Value:\t%d\n" %(int(cut_val)))
        f.write("Node Cut:\n")
        for (x,y) in edge_cut:
            f.write(str(x)+'\t')
        f.flush(); f.close()
        
        self.NDiGraph= copy.deepcopy(self.DirGraph)
        self.NDiGraph.nodes[n]['colour']='red'
        # Colour coding sink
        
        for (x,y) in edge_cut:
            self.NDiGraph.nodes[x]['colour']='orange'
        # Colour coding cut vertices.
              
        nex.write_graphml(self.NDiGraph, '%s_Tar_%d_Col_Node.graphml' %(self.string, int(n)))
        #Outputting colour coded graph in graphml format.
        
        for (x,y) in edge_cut:
            self.NDiGraph.remove_node(x)
        
        nex.write_graphml(self.NDiGraph, '%s_Tar_%d_NodeCut.graphml' %(self.string, int(n)))
        
        os.chdir("../")
        
        if(cut_val<self.min_node_flowval):
            #In case of encountering min capacity of cut out of 65 cuts.
            self.min_node_flowval=cut_val
            self.min_cap_n=[n]
        
        elif(cut_val==self.min_node_flowval):
            #In case of a tie
            self.min_node_flowval=cut_val
            self.min_cap_n.append(n)
            
        if(cut_val>self.max_node_flowval):
            #In case of encountering max capacity of cut out of 65 cuts.
            self.max_node_flowval=cut_val
            self.max_cap_n=[n]
            
        elif(cut_val == self.max_node_flowval):
            #In case of a tie.
            self.max_node_flowval=cut_val
            self.max_cap_n.append(n)
            
        temp=[]    
        for (x,y) in edge_cut:
            temp.append(x)
        temp.append(cut_val)
        
        self.storage_vex[n]=temp
        
        #Storage_vex stores the vertices of a given target (key) followed by the capacity of the cut.
            
        self.NDiGraph.clear()       #Clear copy
                
        
    def statistics(self):  #Noting the overall trends in vertex and edge cuts and creating master-binder.
        
        if(os.path.isdir("General Statistics")==False):
            os.mkdir("General Statistics")
        os.chdir("General Statistics")
        #Changing the directory
        stat=open("Gen_Stat_Log.txt", 'w')
        stat.write("Min Edge Cut Flow Value: %d\n" %(self.min_edge_flowval))
        stat.write("Corresponding Target Nodes\t:"+ str(self.min_cap_e)+"\n")
        
        stat.write("Max Edge Cut Flow Value: %d\n" %(self.max_edge_flowval))
        stat.write("Corresponding Target Nodes\t:"+ str(self.max_cap_e)+"\n")
        
        stat.write("Min Node Cut Flow Value: %d\n" %(self.min_node_flowval))
        stat.write("Corresponding Target Nodes\t:"+ str(self.min_cap_n)+"\n")
        
        stat.write("Max Node Cut Flow Value: %d\n" %(self.max_node_flowval))
        stat.write("Corresponding Target Nodes\t:"+ str(self.max_cap_n)+"\n")
        
        stat.flush(); stat.close()
        
        #Creating the master-binder
        
        self.masterbinder={}
        #Stores data about the edges and nodes and can be used for visualisation.
        #Creating keys
        self.masterbinder['Vertex ID']=[]
        self.masterbinder['Trophic Level']=[]
        self.masterbinder['# of Edge Cuts']=[]
        self.masterbinder['Capacity of Edge Cuts']=[]
        self.masterbinder['# of Vertex Cuts']=[]
        self.masterbinder['Capacity of Vertex Cuts']=[]
        
        trophiclvl=nex.get_node_attributes(self.DirGraph,'trophic')
        #Formulating values for all the above keys      
        for x, y in trophiclvl.items():
            if( x!= 's' and y !=0):
                #Producers and sink not included
                self.masterbinder['Vertex ID'].append(x)
                self.masterbinder['Trophic Level'].append(y)
                #print("Before:\t%d" %(len(self.storage_edge[x])))
                ops=copy.copy(self.storage_edge[x])
                flowval=ops.pop()
                #print("After:\t%d" %(len(self.storage_edge[x])))
                self.masterbinder['# of Edge Cuts'].append(len(ops))
                self.masterbinder['Capacity of Edge Cuts'].append(flowval)
                ops=copy.copy(self.storage_vex[x])
                flowval=ops.pop()
                self.masterbinder['# of Vertex Cuts'].append(len(ops))
                self.masterbinder['Capacity of Vertex Cuts'].append(flowval)
                
            elif(y==0):
                #At trophic level 0 (Producers)
                self.masterbinder['Vertex ID'].append(x)
                self.masterbinder['Trophic Level'].append(y)
                ops=copy.copy(self.storage_edge[x])
                flowval=ops.pop()
                self.masterbinder['# of Edge Cuts'].append(len(ops))
                self.masterbinder['Capacity of Edge Cuts'].append(flowval)
                
                self.masterbinder['# of Vertex Cuts'].append(0)
                self.masterbinder['Capacity of Vertex Cuts'].append(0)
                
                
        
    def statistics_adv(self):       #Finds and presents more detailed insights into the generated data.
        
        if(os.path.isdir("Trophic Statistics")==False):
            os.mkdir("Trophic Statistics")
        os.chdir("Trophic Statistics")
        #Changing the directory
        
        self.trophic_fuel()
        
        
        
        
    def trophic_fuel(self):     #Presents details about the Trophic level architecture and stability of network.
        trophiclvl=nex.get_node_attributes(self.DirGraph, 'trophic')
        
        top=max(list(trophiclvl.values())) #Finds max trophic value
        
        stat=open("Adv_Stat_Log.txt", 'w')
        
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
            
        
     
        stat.flush(); stat.close()
        
        self.trophic_visualisation()
        
        
    def trophic_visualisation(self): #Create a DataFrame to visualise scatterplots and graph them.
        
        if(os.path.isdir("Plots")==False):
            os.mkdir("Plots")
        os.chdir("Plots")
        #Changing the directory
        
        jailkeeper=pan.DataFrame(self.masterbinder)
        print(jailkeeper)
        print("Height of data frame is:\t%d" %(len(jailkeeper.index)))
        
        g1= sea.catplot(x='Trophic Level', y='# of Edge Cuts', kind="strip", data=jailkeeper)
        
        plt.savefig("# Edges_Scatterplot.png", dpi=300)
        plt.show()
        plt.close()
        
        g2= sea.catplot(x='Trophic Level', y='# of Vertex Cuts', kind="strip", data=jailkeeper)
        plt.savefig("# Vertices_Scatterplot.png", dpi=300)
        plt.show()
        plt.close()
        
        g3= sea.catplot(x='Trophic Level', y='Capacity of Edge Cuts', kind="strip", data=jailkeeper)
        plt.savefig("Capacity Edge Cut_Scatterplot.png", dpi=300)
        plt.show()
        plt.close()
        
        g4= sea.catplot(x='Trophic Level', y='Capacity of Vertex Cuts', kind="strip", data=jailkeeper)
        plt.savefig("Capacity Vertex Cut_Scatterplot.png", dpi=300)
        plt.show()
        plt.close()

        #Plotting box-plots

        g1 = sea.boxplot(x='Trophic Level', y='# of Edge Cuts', data=jailkeeper)
        g1 = sea.swarmplot(x='Trophic Level', y='# of Edge Cuts', data=jailkeeper, color=".25")
        plt.savefig("# Edges_Boxplot.png", dpi=300)
        plt.show()
        plt.close()
        
        g2 = sea.boxplot(x='Trophic Level', y='# of Vertex Cuts', data=jailkeeper)
        g2 = sea.swarmplot(x='Trophic Level', y='# of Vertex Cuts', data=jailkeeper, color=".25")
        plt.savefig("# Vertex_Boxplot.png", dpi=300)
        plt.show()
        plt.close()
        
        g3 = sea.boxplot(x='Trophic Level', y='Capacity of Edge Cuts', data=jailkeeper)
        g3 = sea.swarmplot(x='Trophic Level', y='Capacity of Edge Cuts', data=jailkeeper, color=".25")
        plt.savefig("Capacity Edge Cut_Boxplot.png", dpi=300)
        plt.show()
        plt.close()
        
        g4 = sea.boxplot(x='Trophic Level', y='Capacity of Vertex Cuts', data=jailkeeper)
        g4 = sea.swarmplot(x='Trophic Level', y='Capacity of Vertex Cuts', data=jailkeeper, color=".25")
        plt.savefig("Capacity Vertex Cut_Boxplot.png", dpi=300)
        plt.show()
        plt.close()
                
        
                
obj=FordFulkerson()
                
if __name__ == '__main__':
    obj.sanctum()        
        