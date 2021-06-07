# Telegram: t.me/lysand3r 
# TeamChannel: t.me/cobaltteam
# Proxies Engine Class

import random
import re

class Proxy:
    
    ip = None
    port = None
    username = None
    password = None
    protocol = 'http'

    def __init__(self, proxy):
        if not proxy:
            raise Exception('No proxy string supplied')

        if len(proxy) == 2:
            self.set_ip(proxy[0])
            self.set_port(proxy[1])
        
        if len(proxy) == 4:
            self.set_ip(proxy[0])
            self.set_port(proxy[1])
            self.username = proxy[2]
            self.password = proxy[3]

    def set_ip(self, ip):
        ip_pattern = re.compile('^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$')
        if not ip_pattern.match(ip):
            raise Exception('Wrong ip format')
        self.ip = ip

    def set_port(self, port):
        port_pattern = re.compile('^[0-9]{2,5}$')
        if not port_pattern.match(port):
            raise Exception('wrong port format')
        self.port = port
            
    def with_format(self):
        if self.username and self.password:
            return f'{self.protocol}://{self.username}:{self.password}@{self.ip}:{self.port}'
        return f'{self.protocol}://{self.ip}:{self.port}'
    

class ProxiesEngine:

    file_path = None
    file_lines = None

    def __init__(self, file_path):
        if not file_path:
            raise NotImplementedError('Need to initialize with the proxies filepath')
        self.file_path = file_path
        self.file_lines = self.get_file()

    def get_file(self):
        try:
            with open(self.file_path, 'r') as proxies:
                return proxies.read().splitlines()
        except:
            raise Exception('Unable to load the proxi file')

    def random_proxy(self):
        return random.choice(self.file_lines)
    
    def parse_proxy(self):
        # correct format
        # 127.0.0.1:8000:username:password
        proxy = self.random_proxy().split(':')
        print(proxy)
        return Proxy(proxy)

    def select_one(self):
        return self.parse_proxy()

