# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 11:55:27 2019

@author: Koustav
"""

#Used to display interactive 3D maps.

import pickle
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import os

def main():
    os.chdir("Results/Varying/Connectance/Set I/Trends/Rickle Pickle")
    
    for t in range(0,3):
    
        fig= pickle.load(open("Level %d Triangulation # Edge Cut.pickle" %(t), 'rb'))
        plt.show()
        plt.close()
        
        fig= pickle.load(open("Level %d Triangulation Avg Min Node Cut Capacity.pickle" %(t), 'rb'))
        plt.show()
        plt.close()
        
        fig= pickle.load(open("Level %d Triangulation # Node Cut.pickle" %(t), 'rb'))
        plt.show()
        plt.close()
        
        fig= pickle.load(open("Level %d Scatter # Edge Cut.pickle" %(t), 'rb'))
        plt.show()
        plt.close()
        
        fig= pickle.load(open("Level %d Scatter Avg Min Node Cut Capacity.pickle" %(t), 'rb'))
        plt.show()
        plt.close()
        
        fig= pickle.load(open("Level %d Triangulation Avg Min Edge Cut Capacity.pickle" %(t), 'rb'))
        plt.show()
        plt.close()
        
        fig= pickle.load(open("Level %d Scatter # Node Cut.pickle" %(t), 'rb'))
        plt.show()
        plt.close()
        
main()
    
    