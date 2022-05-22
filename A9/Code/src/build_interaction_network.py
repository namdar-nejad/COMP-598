import pandas as pd
import numpy as np
import itertools, os, sys, json


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



def read_file(in_file):
    df = pd.read_csv(in_file)
    df = df.drop(['writer', 'dialog'], axis=1)
    df["pony"] = df["pony"].str.lower()
    return df




def get_top(df, num=101, att='pony'):
    
    counts = df[att].value_counts().to_dict()
    
    top_names = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    rtn = []
    for i in top_names:
        if (not 'all' in i[0].split()) and (not 'others' in i[0].split()) and (not 'ponies' in i[0].split()) and (not 'and' in i[0].split()):
            rtn.append(i[0])
        
    return rtn[:101]




def filter_name(pony, values = ['all', 'others', 'ponies', 'and']):
    
    for i in values:
        if i in pony.split():
            return True
        
    return False




def create_graph_dict(df):
    
    conv_dict = {}
    
    top_names = get_top(df)
    
    for i, row in enumerate(df.values):
        cur_date = df.index[i]
        
        if(i+1 < len(df)):
        
            next_data = df.index[i+1]

            cur_title, cur_pony = df.loc[cur_date]
            next_title, next_pony = df.loc[next_data]

            
            if (not cur_pony == next_pony) and (cur_pony in top_names) and (next_pony in top_names) and (not filter_name(cur_pony)) and (not filter_name(next_pony)) and (cur_title == next_title):
                if (cur_pony, next_pony) in conv_dict:
                    conv_dict[(cur_pony, next_pony)] += 1

                elif (next_pony, cur_pony) in conv_dict:
                    conv_dict[(next_pony, cur_pony)] += 1

                else:
                    conv_dict[(cur_pony, next_pony)] = 1
                    
                
    return conv_dict




def create_file(conv_dict):
    rtn_dict = {}
    
    for key, value in conv_dict.items():
        a,b = key
        
        if not (a in rtn_dict):
            rtn_dict[a] = {}
            
        if not (b in rtn_dict):
            rtn_dict[b] = {}
            
        rtn_dict[b][a] = value
        rtn_dict[a][b] = value
        
        
    return rtn_dict




def write_dict(conv_dict, out_file):
    
    new_dict = {}

    for key, value in conv_dict.items():
        inner_dict = {}
        for key_1, value_1 in value.items():
            inner_dict[key_1.lower()] = value_1

        new_dict[key.lower()] = inner_dict
        
    dir_path = os.path.abspath(os.path.join(out_file, os.pardir))

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    with open(out_file, 'w') as f:
        json.dump(new_dict, f, indent=4)




def main():
    in_file, out_file = check_input()
    
    df = read_file(in_file)   
    conv_dict = create_graph_dict(df)
    conv_dict = create_file(conv_dict)
    write_dict(conv_dict, out_file)



if __name__ == '__main__':
    main()




