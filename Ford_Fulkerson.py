# -*- coding: utf-8 -*-
"""
Created on Fri May 31 12:51:59 2019

@author: Koustav
"""


import os
#import matplotlib.pyplot as plt
import networkx as nex
import copy

class FordFulkerson:
    
    def __init__(self):
        
        self.string = "fw_tuesday_lake"
        self.DirGraph=nex.read_graphml("Machine_Readable_Data\%s\%s_Annotated.graphml" %(self.string, self.string))
        self.min_edge_flowval=self.min_node_flowval= 10000
        self.max_edge_flowval=self.max_node_flowval= 0
        #Stores the min and max flow values of edge and vertex cuts out of all 65 possibilities.
        self.min_cap_e= self.max_cap_e=[] #Stores corresponding target node.
        self.min_cap_n= self.max_cap_n=[]
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
                
            if(i%15==0):
                #Provides a stop-line after every ten iterations
                inp=input("This is a stop-line. Press any key to continue.\n")
            
            i+=1
        self.statistics()
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
        
        if(cut_val==self.min_edge_flowval):
            #In case of a tie
            self.min_edge_flowval=cut_val
            self.min_cap_e.append(n)
            
        if(cut_val>self.max_edge_flowval):
            #In case of encountering max capacity of cut out of 65 cuts.
            self.max_edge_flowval=cut_val
            self.max_cap_e=[n]
            
        if(cut_val == self.max_edge_flowval):
            #In case of a tie.
            self.max_edge_flowval=cut_val
            self.max_cap_e.append(n)
            
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
            
        self.NDiGraph.clear()       #Clear copy
                
        
    def statistics(self):  #Noting the overall trends in vertex and edge cuts.
        
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
                
obj=FordFulkerson()
                
if __name__ == '__main__':
    obj.sanctum()        
        