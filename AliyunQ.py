
import time
import json
import requests
from termcolor import colored
from argparse import ArgumentParser
from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions

class AliyunStorage:
    def __init__(self):
        self.user_id = ""
        self.nick_name = ""
        self.access_token = ""
        self.refresh_token = ""
        self.signin_count = ""

def AliyunQFirst(username , password):
    co = ChromiumOptions()
    co.set_argument('--incognito')
    page = ChromiumPage()

    page.get(url="https://www.aliyundrive.com/sign/in?spm=aliyundrive.index.0.0.2d836f60PHejjP")

    page.ele('xpath://*[@id="login"]/div[1]/div/div[1]/a').click()
    time.sleep(1)

    page.ele("#fm-login-id").input(username)
    page.ele("#fm-login-password").input(password)
    page.ele("@class=fm-button fm-submit password-login").click()
    time.sleep(3)
    AliyunQ()

def AliyunQ():
    co = ChromiumOptions()
    co.set_argument('--incognito')
    aliyunQ = AliyunStorage()

    page = ChromiumPage()
    page.get("https://www.aliyundrive.com/drive/my/feed")
    time.sleep(3)
    tokenValue = page.get_local_storage(item="token")
    tokenValueJSON = json.loads(tokenValue)

    aliyunQ.user_id = tokenValueJSON["user_id"]
    aliyunQ.nick_name = tokenValueJSON["nick_name"]
    aliyunQ.is_first_login = tokenValueJSON["is_first_login"]
    aliyunQ.refresh_token = tokenValueJSON["refresh_token"]

    postData = {
        "grant_type": "refresh_token",
        "refresh_token": aliyunQ.refresh_token
    }

    response = requests.post(url="https://auth.aliyundrive.com/v2/account/token",json=postData).json()

    aliyunQ.access_token = response["access_token"]

    if aliyunQ.access_token == "undefined":
        print("出错了")
    else:
        access_token = "Bearer "+ aliyunQ.access_token
        postData = {
            "_rx-s": "mobile"
        }
        headers = {
            "Authorization": access_token
        }

        response = requests.post(url="https://member.aliyundrive.com/v1/activity/sign_in_list",headers=headers,json=postData).json()
        aliyunQ.signin_count = response["result"]["signInCount"]
        print(" [ 阿里云 ] 用户 "  + aliyunQ.nick_name + " 签到次数 : " + str(aliyunQ.signin_count))

    postData = {
        "signInDay": aliyunQ.signin_count
    }
    response = requests.post(url="https://member.aliyundrive.com/v1/activity/sign_in_reward?_rx-s=mobile",headers=headers,json=postData).json()
    print(" [ 阿里云 ] 用户 " + aliyunQ.nick_name+ " 本次签到获得 : " + response["result"]["notice"])
    page.run_js_loaded("localStorage.clear()")

if __name__ == '__main__':
    name_data = " [阿里云自动签到] "
    lod = colored(
        """
        
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .-----------------. .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |      __      | || |   _____      | || |     _____    | || |  ____  ____  | || | _____  _____ | || | ____  _____  | || |    ___       | |
| |     /  \     | || |  |_   _|     | || |    |_   _|   | || | |_  _||_  _| | || ||_   _||_   _|| || ||_   \|_   _| | || |  .'   '.     | |
| |    / /\ \    | || |    | |       | || |      | |     | || |   \ \  / /   | || |  | |    | |  | || |  |   \ | |   | || | /  .-.  \    | |
| |   / ____ \   | || |    | |   _   | || |      | |     | || |    \ \/ /    | || |  | '    ' |  | || |  | |\ \| |   | || | | |   | |    | |
| | _/ /    \ \_ | || |   _| |__/ |  | || |     _| |_    | || |    _|  |_    | || |   \ `--' /   | || | _| |_\   |_  | || | \  `-'  \_   | |
| ||____|  |____|| || |  |________|  | || |    |_____|   | || |   |______|   | || |    `.__.'    | || ||_____|\____| | || |  `.___.\__|  | |
| |              | || |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 

        """,'magenta'
    )
    print(lod + colored( "                                                                                     v1.0 by:L_favork"),'blue')

    arg = ArgumentParser(description=colored(name_data,'cyan'))
    arg.add_argument("-fl" ,"--firstLogin" ,help="是否是第一次使用本程序 -fl 1")
    arg.add_argument("-u","--username",help="第一次使用需要输入用户名 -u 手机号")
    arg.add_argument("-p","--password",help="第一次使用需要输入密码 -p 密码")
    args = arg.parse_args()

    firstLogin = args.firstLogin
    username = args.username
    password = args.password

    if firstLogin == "1":
        if username == "" or password == "":
            print("[ 阿里云 ] 请输入 用户名 和 密码 ")
        print(" [ 阿里云 ] 用户 " + username + " 正在登录...")
        AliyunQFirst(username , password)
    elif firstLogin == "0":
        AliyunQ()



