import re, json, sys, os, pandas as pd
from os.path import dirname, abspath

STOP_WORDS = []

FINAL_DICT = {
    "twilight sparkle": {},
    "applejack": {},
    "rarity": {},
    "pinkie pie": {},
    "rainbow dash": {},
    "fluttershy": {}
}

def check_input():
    out_file = ''
    in_file = ''

    if (len(sys.argv) == 5) & (sys.argv[1] == '-o') & (sys.argv[3] == '-d'):
        out_file = sys.argv[2]
        in_file = sys.argv[4]
    
    else:
        print("[Error] invalid parameters")
        exit()
    
    return out_file, in_file


def load_stop_words():
    global STOP_WORDS
    STOP_WORDS = []

    with open((dirname(dirname(abspath(__file__)))) + '/data/stopwords.txt', 'r') as f:
        for word in f:
            if not (word[0] == '#' or word[0] == ' '):
                STOP_WORDS.append(word.split('\n')[0])


def add_to_dict(name, string):
    global FINAL_DICT
    
#     remove punctuation
    string = re.sub(r"[\,\.\-\&\#\?\!\;\:\[\]\(\)]", " ", string)
    
#     tokenize
    tokens = string.split()
    
#     get words that only contain alphabets
    tokens = [each_string for each_string in tokens if each_string.isalpha()]
    
#     all lower case
    tokens = [token.lower() for token in tokens]
    
#     remore stop words
    tokens = [token for token in tokens if token not in STOP_WORDS]
    
    name = name.lower()
    
    for token in tokens:
        
        if name in FINAL_DICT:
            if token in FINAL_DICT[name]:
                FINAL_DICT[name][token] =  FINAL_DICT[name][token]+1
            else:
                FINAL_DICT[name][token] = 1


def remove_dict_word(word):
    for pony in FINAL_DICT:
        if word in FINAL_DICT[pony]:
            amount = FINAL_DICT[pony].pop(word)

def remove_low_freqauncy():
    
    all_words = []
    
    for pony in FINAL_DICT:
        for word in FINAL_DICT[pony]:
            if word not in all_words:
                all_words.append(word)
                
    for word in all_words:
        
        frequancy = 0
        
        for pony in FINAL_DICT:
            if word in FINAL_DICT[pony]:
                # print(pony, word, FINAL_DICT[pony][word])
                frequancy += FINAL_DICT[pony][word]
        
        if frequancy < 5:
            remove_dict_word(word)


def count(in_file):
    global FINAL_DICT
    
    data = pd.read_csv(in_file)
    df = data[['pony', 'dialog']]
    
    for i in df.to_numpy():
        if str(i[0].lower()) in FINAL_DICT.keys():
            add_to_dict(i[0].lower(), i[1])
            
    remove_low_freqauncy()


def write_dict(out_file):
        
    dir_path = os.path.abspath(os.path.join(out_file, os.pardir))

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    with open(out_file, 'w') as f:
        json.dump(FINAL_DICT, f, indent=4)


def main():
    out_file, in_file = check_input()

    load_stop_words()
    count(in_file)
    write_dict(out_file)


if __name__ == '__main__':
    main()
