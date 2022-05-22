from sys import argv
import os, sys
import json, argparse
import bs4, wget, requests
from pathlib import Path


def check_input():
    conf_file = ''
    out_file = ''

    if (len(sys.argv) == 5) & (sys.argv[1] == '-c') & (sys.argv[3] == '-o'):
        conf_file = sys.argv[2]
        out_file = sys.argv[4]
    
    else:
        print("[Error] invalid parameters")
        exit()
    
    return conf_file, out_file


def get_info(file):

    with open(file) as f:
        data = json.load(f)
        
    f.close()
    
    return data['cache_dir'], data['target_people']


def create_cache_path(input_path, input_file):
    cache_dir = (os.path.abspath(os.path.join(input_file, os.pardir)))
    final_path = ''
    if (input_path[:1] != '/'):
        final_path = cache_dir+"/"+input_path
    else:
        final_path = input_path
        
    
    if not os.path.exists(final_path):
        os.makedirs(final_path)
        
    return final_path


def download_data(cache_dir, people):
    for i in people:
        url = 'https://www.whosdatedwho.com/dating/'+i
        if(not os.path.exists(cache_dir + "/" + i)):
            wget.download(url, out=cache_dir)


def get_dating(cache_path, person):
    rtn = []
    
    path = cache_path+"/"+person
    soup = bs4.BeautifulSoup(open(path, 'r'), 'html.parser')
    res = soup.find('script')

    try:
        json_object = json.loads(res.contents[0])
    except:
        return []

    arr = json_object['itemListElement']
    
    for i in arr:
        rtn.append("-".join(i['item']['name'].split(" ")))
        
    return rtn


def write(people, dating_arr, file):
    
    write_dict= {}
    
    for i in range(len(people)):
        write_dict[people[i]] = dating_arr[i]

    with open(file, 'w') as f_out:
            
            json.dump(write_dict, f_out, indent=4)

    f_out.close()


def main():
    conf_file, out_file = check_input()
    input_dir, people = get_info(conf_file)
    cache_dir = create_cache_path(input_dir,conf_file)
    download_data(cache_dir, people)
  
    dating_arr = []

    for i in people:
        dating_arr.append(get_dating(cache_dir, i))
        
    write(people, dating_arr, out_file)


if __name__ == '__main__':
    main()



