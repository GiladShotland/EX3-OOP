This project is about implementing a Dirceted Weighted Graph with bunch of Algorithms in Python,
and comparing it to the NetworkX Python Library, which is a library for creating graphes,
and comparing it to my Java implementation (link to the repository below)

In this Project I implemented 2 abstract classes (given by my OOP Course lecturer) with two classes, and a class the represents a node in the graph.

For implementing the DiGraph class I created the NodeInfo class for representing the nodes in the graph.

What's Included In DiGraph?
Creating a graph,adding a node,adding a directed and weighted edge between two nodes, deleting node and edges

What's included in GraphAlgo?
Saving a graph to json, loading a graph from json, getting shortest path between two nodes, getting a strong connected compontns of node, getting all the strong connected components

Methods in DiGraph:


    v_size() - return a number of vertices (nodes) in the graph

    e_size() - return the number of edges in the graph

    get_all_v() - return a dictionary with all the vertices in the graph (every node object mapped by its id)

    get_mc() - return and integer represents the mode count (number of changes) of the graph

    all_out_edges_of_node(node_id : int) - return a dictionary with all the edges that going out from the node (the weight of the edge is mapped by the destination node's id)

    all_int_edges_of_node(node_id : int) - return a dictionary with all the edges that going into the node (the weight of the edge is mapped by the source node's id)

    add_node(node_id : int) - add a node with a given id to the graph (return true if the node was successfully added)

    add_edge(self, id1: int, id2: int, weight: float) - add an edge to the graph between node1 (represented with id1) as the source and node2 (represented with id2) with weight given (return true if edge was successfully added)

    remove_node(id1 : int) - remove a node given from the graph(and all the edges connected to it, return true if the node was successfully removed)

    remove_e

Methods in GraphAlgo:


    save_to_json( file_name: str) - save the graph which the Algo object is initialized on in a json format to a file named and placed by a String given (the method will return true if the graph was successfully saved)

    load_from_json( file_name: str) - load a graph from a json formatted file(the method will return true if the graph was successfully loaded) For example to a json formatted graph - see below.

    shortest_path(self, id1: int, id2: int) : returns a tuple with the shortest path length and an array with the ids of the nodes in the pat between two nodes in the graph. This implementation uses Dijkstra's algorithm (wikipedia link below)

    connected_component( id1: int) : returns a list with ids of the nodes in the strongly connected component which the given node is at. This implementation uses a version of Kosaraju's Algorithm with a BFS (wikipedia link below)

    connected_components() : returns a list of lists, each list contains ids of a single strongly connected component, such that all the lists in the list represents all the strongly connected components in the graph.

    plot_graph(): plotting the graph using matplotlib library.

Example for a graph implemented and plotted by the project:

![nicegrpah](https://user-images.githubusercontent.com/63782779/104630963-33495000-56a4-11eb-8d88-fae90bd412aa.jpg)



How to use:

	Download Python 3.9
  
	Download matplotlib module
  
	Download Pycharm 
  
	git clone : https://github.com/GiladShotland/EX3-OOP.git
  
	Open it on Pycharm
  
	
How to build a graph:

![create graph](https://user-images.githubusercontent.com/63782779/104630488-7a831100-56a3-11eb-833c-47041f84acdb.jpg)
  
How to load and save graph:

![load save](https://user-images.githubusercontent.com/63782779/104630698-c1710680-56a3-11eb-8e15-f31b83813542.jpg)

How to use the components algorithms and plot the graph:

![plots and components](https://user-images.githubusercontent.com/63782779/104630786-ebc2c400-56a3-11eb-833b-c69a86b25de1.jpg)

How to use the shortest path algorithm: 

![exampleshortest](https://user-images.githubusercontent.com/63782779/104630864-0dbc4680-56a4-11eb-8dea-25dcc2e03b94.jpg)













