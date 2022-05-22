import networkx as nx
import pandas as pd
import os, sys, json



def check_input():
    in_file = ''
    out_file = ''

    if (len(sys.argv) == 5) & (sys.argv[1] == '-i') & (sys.argv[3] == '-o'):
        in_file = sys.argv[2]
        out_file = sys.argv[4]
    
    else:
        print("[Error] invalid parameters")
        exit()
    
    return in_file, out_file



def load_file(in_file):
    with open(in_file, "r") as json_file:
        intraction_dict = json.load(json_file)
        
    return intraction_dict



def create_graph(intract_dict):
    
    G = nx.Graph()
    
    for a, value in intract_dict.items():
        for b, w in value.items():
            if not G.has_edge(a,b):
                G.add_edge(a,b,weight=w)
    
    return G



def count(graph):
    data_dict = {}
        
    for i in graph.nodes():
        inner = {"degree": 0, "total weight":0, "betweenness": 0}
        
        neighbours = graph.edges(i)
        
        w = 0
        for n in neighbours:
            w += ((graph.get_edge_data(i, n[1]))["weight"])
            
        inner["degree"] = graph.degree(i)
        inner["total weight"] = w
        
        data_dict[i] = inner
    
    for key,value in nx.betweenness_centrality(graph).items():
        data_dict[key]["betweenness"] = value
    

    return(data_dict)



def crete_dict(data_dict):
    
    rtn_dict = {
        "most_connected_by_num": [],
        "most_connected_by_weight": [],
        "most_central_by_betweenness": []
    }
    
    length = 3
    if len(data_dict) < 3:
        length = len(data_dict)
    
    df = pd.DataFrame.from_dict(data_dict, orient='index')
    
    df = df.sort_values(by ="degree",ascending=False)    
    rtn_dict["most_connected_by_num"] = list((df[:length].head()).index)
    
    
    df = df.sort_values(by ="total weight",ascending=False)
    rtn_dict["most_connected_by_weight"] = list((df[:length].head()).index)
    
    
    df = df.sort_values(by ="betweenness",ascending=False)
    rtn_dict["most_central_by_betweenness"] = list((df[:length].head()).index)
    

    return rtn_dict



def write_dict(data_dict, out_file): 

    dir_path = os.path.abspath(os.path.join(out_file, os.pardir))

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    with open(out_file, 'w') as f:
        json.dump(data_dict, f, indent=4)



def main():
    
    in_file, out_file = check_input()
    
    intract_dict = load_file(in_file)
    graph = create_graph(intract_dict)
    data_dict = count(graph)
    data_dict = crete_dict(data_dict)
    write_dict(data_dict, out_file)



if __name__ == '__main__':
    main()



