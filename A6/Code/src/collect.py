import requests
import json, os

CLIEN_ID = 'jdl7NLjizUM0v8t5oapN5w'
SECRET_KEY = 'Uw1zoE7Pja_bFU3kTKCEHYzzlVIfoQ'

USERNAME = 'Namdar_Nejad'
PASSWORD = 'namdar1234'

headers = {}

SUBS_1 = ['funny', 'AskReddit', 'gaming', 'aww', 'pics', 'Music', 'science', 'worldnews', 'videos', 'todayilearned']
SUBS_2 = ['AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets', 'teenagers', 'PublicFreakout', 'leagueoflegends',
'unpopularopinion']


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

def collect(subs):
    out = []
    for i in subs:
        res = requests.get("https://oauth.reddit.com/r/"+ i +"/new?limit=100", headers=headers)
        out += (res.json()['data']['children'])
    
    return out

def write_data(data, file_name):
    with open(file_name, 'w') as f_out:
        for i in data:
            json.dump(i, f_out)
            f_out.write("\n")

    f_out.close()


def main():
    setup()
    out1 = collect(SUBS_1)
    out2 = collect(SUBS_2)

    abs_path = str(os.path.abspath(__file__))

    if 'submission_template' in abs_path.split("/"):
        path = ((abs_path.split("submission_template"))[0])+"submission_template"
        write_data(out1, path+'/sample1.json')
        write_data(out2, path+'/sample2.json')
    
    elif '260893536_submission_template' in abs_path.split("/"):
        path = ((abs_path.split("260893536_submission_template"))[0])+"260893536_submission_template"
        write_data(out1, path+'/sample1.json')
        write_data(out2, path+'/sample2.json')

    else:
        write_data(out1, './sample1.json')
        write_data(out2, './sample2.json')




if __name__ == '__main__':
    main()


