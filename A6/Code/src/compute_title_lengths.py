from sys import argv
import sys
import json


def load_data(file):
    data = []
    
    with open(file, 'r') as f:
        for line in f:
            try: data.append(json.loads(line))
            except: pass

    f.close()
    
    return data


def check_input():
    
    file = ''
    
    if (len(sys.argv) == 2):
        file = sys.argv[1]
        
    else:
        print("[Error] invalid parameters")
        exit()
        
    return file


def get_average(arr):
    total_sum = 0
    total_size = len(arr)
    
    for i in arr:
        total_sum += len(i['data']['title'])
    
    return (total_sum/total_size)


def main():
    file = check_input()
    data = load_data(file)
    average = get_average(data)
    
    print(round(average,2))


if __name__ == '__main__':
    main()



