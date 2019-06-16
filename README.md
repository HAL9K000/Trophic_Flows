#    <div style="text-align: center"> The Network Ecologist's DIY Handbook </div>
######  <div style="text-align: right"> - hal9k000 </div>
---
## The Keynote Address:

The Ford-Fulkerson algorithm (1961) <sup>[1][2] </sup> is a powerful dual-optimisation tool in Graph-Theory that can be applied to determine the:
* Maximum flow in a directed network
* Concurrently the minimum capacity of a cut seperating a pre-defined *source (node from which energy flows out to the rest of the network, in this case an abiotic source like the sun)* from a *sink (a node where energy flows into)*.
* The minumum number of edges that if eliminated *(min edge cut)* will disconnect the source ***(s)*** from the sink ***(t)***.
* The minimum number of nodes that if eliminated *(min vertex cut)* will disconnect *s* from *t*.

Furthermore it can readily be extended to account for multiple sinks/sources <sup>[3] </sup>.

The code above basically generates a properly annotated graph (outputted in .graphml format) from raw CSV data on trophic interactions and then performs the above algorithm (both edge cuts and vertex cuts) several times, treating each node in the trophic network (whether producer, first-order consumer, second-order consumer or so on) as the *sink* in each iteration, saving the results of each to an appropriate sub-directory in *Results*.

## The Starter Kit:

To run the code above, you'll need *Python 3.X* installed on your workstation, together with the following Python packages:
* NetworkX <sup>[4] </sup>
* NumPy
* Pandas
* Matplotlib
* Seaborn

Additionally, applications such as [Cytoscape](https://cytoscape.org/ "Cytoscape") or [Gephi](https://gephi.org/ "Gephi") might be useful for graph visualisation.

## The How-To Section:

* First, after cloning this repository, store the trophic network data in the form of a *.CSV* spreadsheet in the folder *CSV Data*. The CSV spreadsheet must be configured such that the each row in it corresponds to the adjacency list of the indexed node *(see method `creator(self)` in I0.py for further details)*.

* Next, after having made your spreadsheet (say  *dilettante.csv*  for instance) your next task would be to open up *I0.py*, scroll over to `__init__(self)` and change:

      self.string = "fw_tuesday_lake"

    to:

      self.string = "dilettante"

    (Should be the same name as the .CSV file)

* Run *I0.py*. The annotated graph (with trophic level of nodes, edge and node capacities automatically assigned) will be saved in the directory *"Machine_Readable_Data"*.

* Next, similarly, change the assigned value to `self.string` in *Ford_Fulkerson.py* (under `__init__(self)`) to:
      self.string = "dilettante"
and execute. The output will similarly be saved in *.graphml* format to the *"Results"* directory.

* To analyse the connectance in *dilettante* between trophic levels, run it through *ConnecFinder.py* having made the same changes to `self.string` in *ConnecFinder.py* as above. Make sure you run *I0.py* before this.

* After having run *I0.py* and *ConnecFinder.py* (in that order) for *dilettante*, if you choose, you can make an artificial network based on the connectance data of *dilettante* by running *ArcNet.py*. By default, it will create an artificial network of 24 nodes, but you can modify this as you see fit by altering
      self.n = 24
under `__init__(self)` accordingly.

* *ArcNet.py* also provides a few pre-defined trophic configurations *(default number of trophic levels= 3)* for the artificially generated networks such as *Pyramidal* (represented by *'Tr'*), *Rectangular* (represented by *'Rect'*), *Diamond* (represented by *'Dia'*) and so on. Alternatively, you can choose your own node distribution and the number of trophic levels for the artificial network. The generated trophic network is outputted in .graphml format which can in turn be fed into *"Ford_Fulkerson.py"* for min edge and vetrex cut information.

## References:

[1]: Douglas B. West: *Introduction To Graph Theory*

[2]: Reinhard Diestel: *Graph Theory*

[3]: https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/flowext.pdf "Carl Kingsford's slides on extensions to Ford-Fulkerson"

[4]: https://networkx.github.io/documentation/networkx-2.3/reference/introduction.html "NetworkX Introduction"
