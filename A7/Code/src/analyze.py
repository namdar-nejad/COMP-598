import json, random, csv, sys


def check_input():
    out_file = ''
    
    if (len(sys.argv) == 3) & (sys.argv[1] == '-i'):
        coded_file = sys.argv[2]
        out_file = None
        
    elif (len(sys.argv) == 5) & (sys.argv[1] == '-i') & (sys.argv[3] == '-o'):
        coded_file = sys.argv[2]
        out_file = sys.argv[4]

    else:
        print("[Error] invalid parameters")
        exit()
    
    return coded_file, out_file


def write_data(data, file_name):
    
    if '.json' not in file_name:
        file_name = file_name + ".json"
            
    with open(file_name, 'w') as f_out:
            json.dump(data, f_out, indent=0)

    f_out.close()


def process(coded_file):

    data = {
        "course-related": 0,
        "food-related": 0,
        "residence-related": 0,
        "other": 0
    }

    if '.tsv' not in coded_file:
        coded_file = coded_file + ".tsv"
    
    with open(coded_file) as f:
        tsv_file = csv.reader(f, delimiter="\t")
        for line in tsv_file:
            anno = line[2]
            if len(anno) == 1:
                if anno == 'c': data["course-related"] = data["course-related"]+1
                elif anno == 'f': data["food-related"] = data["food-related"]+1
                elif anno == 'r': data["residence-related"] = data["residence-related"]+1
                elif anno == 'o': data["other"] = data["other"]+1
            
    f.close()
    
    return data


def main():
    coded_file, out_file = check_input()

    data = process(coded_file)
    
    if (out_file == None):
        print(json.dumps(data, indent=0))
    else:
        write_data(data, out_file)


if __name__ == '__main__':
    main()


