import requests, json, os, sys

CLIEN_ID = 'jdl7NLjizUM0v8t5oapN5w'
SECRET_KEY = 'Uw1zoE7Pja_bFU3kTKCEHYzzlVIfoQ'

USERNAME = 'Namdar_Nejad'
PASSWORD = 'namdar1234'

headers = {}

def check_input():
    conf_file = ''
    out_file = ''

    if (len(sys.argv) == 5) & (sys.argv[1] == '-o') & (sys.argv[3] == '-s'):
        out_file = sys.argv[2]
        sub = sys.argv[4]
    
    else:
        print("[Error] invalid parameters")
        exit()
    
    return out_file, sub

def setup():
    global headers
    auth = requests.auth.HTTPBasicAuth(CLIEN_ID, SECRET_KEY)

    data = {
        'grant_type': 'password',
        'username': USERNAME ,
        'password': PASSWORD
    }

    headers = {'User-Agent': 'MyAPI/0.0.1'}

    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

    TOKEN = res.json()['access_token']
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)


def collect(sub):
    
    if 'r/' in sub:
        sub = sub.split("r/")[1] 

    elif '/r/' in sub:
        sub = sub.split("/r/")[1] 
    
    out = []
    res = requests.get("https://oauth.reddit.com/r/"+ sub +"/new?limit=100", headers=headers)
    out += (res.json()['data']['children'])
    
    return out


def write_data(data, file_name):
    
    if '.json' not in file_name:
        file_name = file_name + ".json"
    
    with open(file_name, 'w') as f_out:
        for i in data:
            json.dump(i, f_out)
            f_out.write("\n")

    f_out.close()


def main():
    setup()
    out_file, sub = check_input()

    par_dir = (os.path.abspath(os.path.join(out_file, os.pardir)))

    if not os.path.exists(par_dir):
        os.makedirs(par_dir)
        
    out = collect(sub)
    write_data(out, out_file)


if __name__ == '__main__':
    main()

