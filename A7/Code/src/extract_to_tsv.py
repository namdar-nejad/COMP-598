import json, random, csv, sys, os

def check_input():
    out_file = ''

    if (len(sys.argv) == 5) & (sys.argv[1] == '-o'):
        out_file = sys.argv[2]
        json_file = sys.argv[3]
        num_posts = sys.argv[4]
        
    
    else:
        print("[Error] invalid parameters")
        exit()
    
    return out_file, json_file, num_posts


def load_data(json_file):
    
    data = []

    if '.json' not in json_file:
        json_file = json_file + ".json"
    
    with open(json_file, 'r') as f:
        for line in f:
            try: data.append(json.loads(line))
            except: pass
            
    f.close()
    
    return data


def process(data_arr, out_file, num_posts):

    if '.tsv' not in out_file:
        out_file = out_file + ".tsv"
    
    if len(data_arr) <= int(num_posts):
        num_posts = len(data_arr)
        
    random_data = random.sample(data_arr, int(num_posts))
    
    with open(out_file, 'wt') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['Name', 'title', 'coding'])
        for i in random_data:
            string = '"{0}"'.format(i['data']['title'])
            f.write("%s\t%s\t\n" % (i['data']['name'], string))
    
    f.close()
    

def main():
    out_file, json_file, num_posts = check_input()

    par_dir = (os.path.abspath(os.path.join(out_file, os.pardir)))

    print(out_file)
    print(par_dir)

    if not os.path.exists(par_dir):
        os.makedirs(par_dir)


    data_arr = load_data(json_file)
    process(data_arr, out_file, num_posts)


if __name__ == '__main__':
    main()




