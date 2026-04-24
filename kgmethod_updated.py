import pandas as pd
import numpy as np 
import networkx as nx
import matplotlib.pyplot as plt
import random
import os

random.seed(4812)

def generate_csv(workbook_name,sheet_name):

    """This function takes in two string inputs
    workbook_name -> str: Name of the workbook where the metadata is stored
    sheet_name -> str: Name of the sheet in the workbook to be converted to csv

    The output is a csv file which is saved in a folder in the working directory
    """
    path_xlsx = "/Users/a8jain/Desktop/kgmethod/GXAPC/"
    filepath = path_xlsx+workbook_name
    df = pd.read_excel(filepath,sheet_name=sheet_name)
    return df


def analysis (graph):
    
    
    pruned_graph = graph.copy()
    
    # Select Enablers with highest Importance towards Migration and Maturity at or higher than TRL2 first (TRL1 enablers to be considered in future projects)
    for node in graph:
        #print(node)
        #print(usecase_graph.nodes[node])
        #if :
        #    print(node)
        try: 
            if (pruned_graph.nodes[node]["TRL"]>=2 or pruned_graph.nodes[node]["Migration Weight"]>1):
                # print(len(list(usecase_graph.adj[node])))
                # print(sum(data['weight'] for _, _, data in usecase_graph.edges(node,data=True)))
                continue # Do not remove really mature and Migration dependent enablers
            else:    
                pruned_graph.remove_node(node) # Remove the nodes that are not the highest priority and also not mature and do not have a lot of dependencies
        except KeyError as err:
            if err.args[0] == 'TRL' or err.args[0]=='Migration Weight':
                pass
            else:
                raise  
    
    # Remove enablers with the least contribution to the KPI goals. Remove nodes that do not contribute to the KPI at all first.
    pruned_graph_KPI = pruned_graph.copy()

    
    KPI_val_arr = [] # Array to hold all the computed KPI values to perform a frequency analysis later on
    for node in pruned_graph:
        #print(node)
        if node == "DP1" or node == "DP2" or node == "DP3" or node == "DP4" or node == "DP5" or node=="DP6" or node=="DP7" or node=="DP8" or node=="DP9" or node=="DP10":
            continue
        else:
            try:
                KPI_val = pruned_graph.nodes[node]["D2D Latency"] + pruned_graph.nodes[node]["Latency"] + pruned_graph.nodes[node]["Information Transfer Delay"] + pruned_graph.nodes[node]["Bit Error Rate"] + pruned_graph.nodes[node]["Bitrate Control Plane"] + pruned_graph.nodes[node]["Bitrate Data Plane"] + pruned_graph.nodes[node]["Connection Density"] + pruned_graph.nodes[node]["Positioning Accuracy"] + pruned_graph.nodes[node]["Localization Accuracy"] + pruned_graph.nodes[node]["Setup Time"] + pruned_graph.nodes[node]["Migration Time"] + pruned_graph.nodes[node]["Security and Trust (DP)"] + pruned_graph.nodes[node]["Security and Trust (CP)"] + pruned_graph.nodes[node]["Energy Consumption"] + pruned_graph.nodes[node]["Material Reuse"]
                KPI_val_arr.append(KPI_val)
                #print(KPI_val)
                if KPI_val < 1 and pruned_graph.nodes[node]["Migration Weight"]<=1:
                    pruned_graph_KPI.remove_node(node)
                else:
                    continue
            except KeyError as err2:
                if err2.args[0] == 'D2D Latency' or err2.args[0] =='Latency' or err2.args[0] =='Information Transfer Delay' or err2.args[0]=='Bit Error Rate' or err2.args[0]=='Bitrate Control Plane' or err2.args[0]=='Bitrate Data Plane' or err2.args[0]=="Connection Density" or err2.args[0]=='Positioning Accuracy' or err2.args[0]=='Localization Accuracy' or err2.args[0]=='Setup Time' or err2.args[0]=='Migration Time' or err2.args[0]=='Security and Trust (DP)' or err2.args[0]=='Security and Trust (CP)' or err2.args[0]=='Energy Consumption' or err2.args[0]=='Material Reuse' or err2.args[0]=='Migration Weight':
                    pass
                else:
                    raise 

    # Add Enablers in the 
    
    # Plot histogram of the KPI impact to be able to decide on appropriate threshold

    plt.figure(figsize=(20,16))
    plt.hist(KPI_val_arr,bins=max(KPI_val_arr),color="skyblue",edgecolor="black",align='left')
    plt.xlabel('KPI Score',fontsize=44)
    plt.xticks(np.arange(min(KPI_val_arr),max(KPI_val_arr),1))
    plt.ylabel('Number of Enablers',fontsize=44)
    plt.grid(visible=True,which="major",axis="both",linestyle='--',linewidth=0.5)
    plt.xticks(fontsize=42)
    plt.yticks(fontsize=42)
    plt.savefig('KPIimpact.png')

    print(list(graph.nodes))    
    print(len(list(graph.nodes)) - 10)
    
    print(list(pruned_graph.nodes))    
    print(len(list(pruned_graph.nodes)) - 10)
    
    print(list(pruned_graph_KPI.nodes))    
    print(len(list(pruned_graph_KPI.nodes)) - 10)
    # Visualize and Save the pruned graph without KPI Impact
    color_map_prune = []
    for node in pruned_graph:
        if node == "DP1" or node == "DP2" or node == "DP3" or node == "DP4" or node == "DP5" or node=="DP6" or node=="DP7" or node=="DP8" or node=="DP9" or node=="DP10":
            color_map_prune.append('lightgreen')
        elif sum(data['weight'] for _,_, data in pruned_graph.edges(node,data=True)) < 1:
            color_map_prune.append('orange')
        else:
            color_map_prune.append('lightblue')

    edge_color_prune = [pruned_graph[i][j]['color'] for i,j in pruned_graph.edges()]
    pos_prune = nx.spring_layout(pruned_graph,k=1.5)
    labels_prune = nx.get_edge_attributes(pruned_graph,'label')
    plt.figure(figsize=(20,10))
    nx.draw(pruned_graph,pos_prune,with_labels=True,font_size=10,node_size=1800,node_color=color_map_prune,edge_color=edge_color_prune,alpha=0.8)
    nx.draw_networkx_edge_labels(pruned_graph,pos_prune,edge_labels=labels_prune,font_size=8, label_pos=0.3, verticalalignment='baseline')
    plt.title('Pruned Knowledge Graph without KPI Impact')
    plt.savefig('prunedgraphwoKPI.png')
    #plt.show()

    # Visualize and Save the pruned graph without KPI Impact
    color_map_prune_KPI = []
    for node in pruned_graph_KPI:
        if node == "DP1" or node == "DP2" or node == "DP3" or node == "DP4" or node == "DP5" or node=="DP6" or node=="DP7" or node=="DP8" or node=="DP9" or node=="DP10":
            color_map_prune_KPI.append('lightgreen')
        elif sum(data['weight'] for _,_, data in pruned_graph_KPI.edges(node,data=True)) < 1:
            color_map_prune_KPI.append('orange')
        else:
            color_map_prune_KPI.append('lightblue')

    edge_color_prune_KPI = [pruned_graph_KPI[i][j]['color'] for i,j in pruned_graph_KPI.edges()]
    pos_prune_KPI = nx.spring_layout(pruned_graph_KPI,k=1.5)
    labels_prune_KPI = nx.get_edge_attributes(pruned_graph_KPI,'label')
    plt.figure(figsize=(20,10))
    nx.draw(pruned_graph_KPI,pos_prune_KPI,with_labels=True,font_size=10,node_size=1800,node_color=color_map_prune_KPI,edge_color=edge_color_prune_KPI,alpha=0.8)
    nx.draw_networkx_edge_labels(pruned_graph_KPI,pos_prune_KPI,edge_labels=labels_prune_KPI,font_size=8, label_pos=0.3, verticalalignment='baseline')
    plt.title('Pruned Knowledge Graph')
    plt.savefig('prunedgraphKPI.png')
    #plt.show()

    return pruned_graph_KPI


def graphprocess(df_Maturity,df_KPI,df_Dependency,df_KVI,df_hardware_dep,df_prioritization):
    """This function takes in six dataframes as input and processes them to create a knowledge graph"""

    # Develop the knowledge graph using MultiGraph to allow multiple edges between same nodes
    graph_str = nx.MultiDiGraph()
    
    # Add the dependencies for each enabler to the KG
    # Track edges to avoid double counting (store edge type and node pair)
    added_edges = {}  # Dict to track: {(node1, node2): set of edge types}
    
    for _,rowdep in df_Dependency.iterrows():
        if(rowdep['Dependencies']=='None'):
            continue
        else:
            # Add dependency edge only if not already added and if Dependencies value exists
            # Direction: dependency → enabler (dependency flows INTO the enabler)
            if pd.notna(rowdep['Dependencies']):
                dep_edge = tuple(sorted([rowdep['Enabler'], rowdep['Dependencies']]))
                if dep_edge not in added_edges:
                    added_edges[dep_edge] = set()
                
                if 'dependency' not in added_edges[dep_edge]:
                    graph_str.add_edge(rowdep['Dependencies'],rowdep['Enabler'],weight = 0, color = 'r', edge_type='dependency', label='dependency')
                    added_edges[dep_edge].add('dependency')
            
            # Add impact edge only if not already added and if Impacts value exists
            # Note: Column name has a leading space ' Impacts'
            impact_col = ' Impacts' if ' Impacts' in rowdep.index else 'Impacts'
            if impact_col in rowdep.index and pd.notna(rowdep[impact_col]):
                impact_edge = tuple(sorted([rowdep['Enabler'], rowdep[impact_col]]))
                if impact_edge not in added_edges:
                    added_edges[impact_edge] = set()
                
                if 'impact' not in added_edges[impact_edge]:
                    graph_str.add_edge(rowdep['Enabler'],rowdep[impact_col],weight = 0, color = 'g', edge_type='impact', label='impact')
                    added_edges[impact_edge].add('impact')
    
    # Set Hardware Dependency attributes
    hwdep_attrs = {} # Create an empty dictionary
    for _,rowhwdep in df_hardware_dep.iterrows():
        hwdep_attrs |= {rowhwdep['Enabler']:{"HWDEP":rowhwdep['HW Dependency']}}
    
    nx.set_node_attributes(graph_str,hwdep_attrs)        
    
    # Set Prioritization attributes
    prior_attrs = {} # Create an empty dictionary
    for _,rowprior in df_prioritization.iterrows():
        prior_attrs |= {rowprior['Enabler']:{"Prioritization":rowprior['Priority Encoded']}}

    nx.set_node_attributes(graph_str,prior_attrs)
    # Set Maturity attributes
    matur_attrs = {} # Create an empty dictionary
    for _,rowmatur in df_Maturity.iterrows():
        matur_attrs |= {rowmatur['Enabler']:{"TRL":rowmatur['TRL']}}
    
    nx.set_node_attributes(graph_str,matur_attrs)  

    # Set KPI attributes
    kpi_attrs = {} # Create an empty dictionary for KPI data
    for _,rowKPI in df_KPI.iterrows():
        kpi_attrs |= {rowKPI['Enabler']:{"Latency":rowKPI["E2E-Latency (ms)"],"Throughput":rowKPI["Throughput(gain)"],"System Capacity":rowKPI["System Capacity "],
                                         "Resilience":rowKPI["Resiliency(RLF/HO failure rate)"],"Complexity":rowKPI["Complexity(UE implementation, NW impl, None, Both)"],"Signaling overhead":rowKPI["Signaling overhead(number of messages/transactions)"],
                                         "Resource reservation":rowKPI["Resource reservation (number cells per UE context)"]}}
        
    nx.set_node_attributes(graph_str,kpi_attrs)

    # Set KVI attributes
    kvi_attrs = {} # Create an empty dictionary for KVI data
    for _,rowKVI in df_KVI.iterrows():
        kvi_attrs |= {rowKVI['Enabler']:{"Energy Efficiency":rowKVI["Energy Efficiency"],"Coverage Enhancement":rowKVI["Coverage Enhancement"],"Human Usage":rowKVI["Human Usage"],
                                         "Time Usage":rowKVI["Time Usage"],"Geographical Usage":rowKVI["Geographical Usage"]}}

    nx.set_node_attributes(graph_str,kvi_attrs)

    # Create a color map 
    color_map = []
    for node in graph_str:
        if sum(data['weight'] for _,_, data in graph_str.edges(node,data=True)) < 1:
            color_map.append('orange')
        else:
            color_map.append('lightblue')
 
    # Extract edge colors from MultiDiGraph (need to handle multiple edges)
    edge_color = [graph_str[i][j][k]['color'] for i,j,k in graph_str.edges(keys=True)]
    
    # Visualize the KG with directed arrows
    pos = nx.spring_layout(graph_str,k=1.5)
    
    plt.figure(figsize=(20,10))
    nx.draw(graph_str,pos,with_labels=True,font_size=10,node_size=1800,node_color = color_map, edge_color = edge_color, alpha=0.8, arrows=True, arrowsize=20, arrowstyle='->', connectionstyle='arc3,rad=0.1')
    plt.title('Knowledge Graph of Enabler relationships for WP3')
    plt.savefig('KGmethod.png')
    plt.show()
    #pruned_graph = analysis(graph_str) # Analyze and prune the graph

    # Save the list of Enablers in a text file
    """ with open('selected_enablers.txt', 'w') as f:
        for node in pruned_graph:
            if node == "DP1" or node == "DP2" or node == "DP3" or node == "DP4" or node == "DP5" or node=="DP6" or node=="DP7" or node=="DP8" or node=="DP9" or node=="DP10":
                pass
            else:
                f.write(f"{node}:")
                for _,rowabbv in Abbv.iterrows():
                    #print(rowabbv)
                    if node == rowabbv['Enabler']:
                        full_form = rowabbv['Full Form']
                        f.write(f" {full_form} \n") """
                     
if __name__ == "__main__":
    df_Maturity = generate_csv("MetaData_Table_GX+APC.xlsx","Maturity")
    #df_Migration = generate_csv("MetaData_Table_GX+APC.xlsx","")
    df_KPI = generate_csv("MetaData_Table_GX+APC.xlsx","KPI")
    df_Dependency = generate_csv("MetaData_Table_GX+APC.xlsx","Enabler Dependencies")
    #df_Allenab = generate_csv("MetaData_Table_GX+APC.xlsx","Maturity")
    df_KVI = generate_csv("MetaData_Table_GX+APC.xlsx","KVIs")
    df_hardware_dep = generate_csv("MetaData_Table_GX+APC.xlsx","Hardware Dependencies")
    df_prioritization = generate_csv("MetaData_Table_GX+APC.xlsx","Prioritization")
    print(df_Dependency.head())
    graphprocess(df_Maturity,df_KPI,df_Dependency,df_KVI,df_hardware_dep,df_prioritization)
    #print(df_KVI.head())
    