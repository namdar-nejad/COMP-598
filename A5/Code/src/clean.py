from sys import argv
import sys
import json
import datetime   
import pytz
import dateutil.parser

local = pytz.timezone('UTC')


i_file = ''
o_file = ''
data = []


def check_input():
    global i_file
    global o_file

    if (len(sys.argv) == 5) & (sys.argv[1] == '-i') & (sys.argv[3] == '-o'):
        i_file = sys.argv[2]
        o_file = sys.argv[4]
    
    else:
        print("[Error] invalid parameters")
        exit()

def set_files(inputf, outputf):
    global i_file
    global o_file

    i_file = inputf
    o_file = outputf

def load_data():
    global data
    data = []
    with open(i_file, 'r') as f:
        for line in f:
            try: data.append(json.loads(line))
            except: pass

    f.close()


def process():

    new_data = data.copy()
    remove = []

    for i in range(len(new_data)):
        slot = new_data[i]

        if not ('title' in slot or 'title_text' in slot):
            remove.append(i)

        if ('title_text' in slot):
            slot['title'] = slot['title_text']
            del slot['title_text']
        
            
        if ('author' in slot) and ((slot['author'] == None) or (slot['author'] == 'N/A') or (slot['author'] == '')):
            remove.append(i)

        if ('createdAt' in slot):
            try:
                cur_date = dateutil.parser.isoparse(slot['createdAt'])
                utc_dt = cur_date.astimezone(local)
                slot['createdAt'] = "T".join(str(utc_dt).split(" "))

            except:
                remove.append(i)

        if ('total_count' in slot):

            typ = type(slot['total_count'])

            if not ((typ == int) or (typ == str) or (typ == float)):
                remove.append(i)

            else:
                try:
                    slot['total_count'] = int(slot['total_count'])
                except:
                    remove.append(i)

        if ('tags' in slot):
            tags = slot['tags']
            new_arr = []

            for i in tags:
                new_arr += (i.split())

            slot['tags'] = new_arr



    remove = list(set(remove))

    for j in remove:

        slot = data[j].copy()
        new_data.remove(slot)
        
    return new_data


def write_data(new_data):
    with open(o_file, 'w') as f_out:
        for i in new_data:
            json.dump(i, f_out)
            f_out.write("\n")

    f_out.close()
        

def main():
    check_input()
    load_data()
    new_data = process()
    write_data(new_data)


if __name__ == '__main__':
    main()



