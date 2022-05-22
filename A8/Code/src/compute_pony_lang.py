import json, os, sys, math, pandas as pd

PONY_WORDS_DICT = {}

PONIES = [ "twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]


def check_input():
    pony_file = ''
    num_words = 0

    if (len(sys.argv) == 5) & (sys.argv[1] == '-c') & (sys.argv[3] == '-n'):
        pony_file = sys.argv[2]
        num_words = sys.argv[4]
    
    else:
        print("[Error] invalid parameters")
        exit()
    
    return pony_file, num_words


def load_pony_count(pony_file):
    global PONY_WORDS_DICT
    with open(pony_file, "r") as json_file:
        PONY_WORDS_DICT = json.load(json_file)


def tf(w, pony):
    
    if w in PONY_WORDS_DICT[pony]:
        return PONY_WORDS_DICT[pony][w]
    else:
        return 0


def idf(w):
    j = 0
    for i in PONIES:
        if tf(w, i) > 0:
            j+=1
    
    return(math.log10(len(PONIES)/j))


# tf-idf(w, pony, script) = tf(w, pony) x idf(w, script)

def tf_idf(w, pony):
    return tf(w, pony)*idf(w)


def process(num):
    rtn_dict = {
        "twilight sparkle": {},
        "applejack": {},
        "rarity": {},
        "pinkie pie": {},
        "rainbow dash": {},
        "fluttershy": {}
    }
    
    for pony in PONIES:
        
        df = pd.DataFrame({'word': [], 'score': []})
        
        for word in PONY_WORDS_DICT[pony]:
            score = tf_idf(word, pony)
            new_d = pd.DataFrame({'word': [word], 'score': [score]})
            df = df.append(new_d, ignore_index = True)

        df = df.sort_values(by=['score'], ascending = False)

        rtn_dict[pony] = [i[0] for i in df.head(int(num)).to_numpy()]
        
    return rtn_dict



def main():
    global PONY_WORDS_DICT
        
    pony_file, num_words = check_input()
    
    load_pony_count(pony_file)
        
    rtn_dict = process(num_words)
    
    print(json.dumps(rtn_dict, indent=4))



if __name__ == '__main__':
    main()




