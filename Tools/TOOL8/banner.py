import sys
import random
import time

def logo():
 clear = "\x1b[0m"
 colors = [36, 32, 34, 35, 31, 37]
 x = """ 

  ___  ___  ___  ___   ___________ _   _   _____  _   _  _____  ___  _____  _   __ ___________ 
 / _ \ |  \/  | / _ \ |___  /  _  | \ | | /  __ \| | | ||  ___|/ _ \/  __ \| | / /|  ___| ___ \
/ /_\ \| .  . |/ /_\ \   / /| | | |  \| | | /  \/| |_| || |__ / /_\ \ /  \/| |/ / | |__ | |_/ /
|  _  || |\/| ||  _  |  / / | | | | . ` | | |    |  _  ||  __||  _  | |    |    \ |  __||    / 
| | | || |  | || | | |./ /__\ \_/ / |\  | | \__/\| | | || |___| | | | \__/\| |\  \| |___| |\ \ 
\_| |_/\_|  |_/\_| |_/\_____/\___/\_| \_/  \____/\_| |_/\____/\_| |_/\____/\_| \_/\____/\_| \_|
                                                                                               
                                                                                                   
                                                                          
 Amazon Valid Email Checker    |  Code by LAKER                                
 
 [+] instagram : @E9_z_


 [+] 1. Run Amazon Valid Email Checker 
 [+] 2. About me [ for any help ! ] 

+-------- With Great Power Comes Great Responsibilities! --------+

			                  """
 for N, line in enumerate( x.split( "\n" ) ):
        sys.stdout.write( " \x1b[1;%dm%s%s\n " % (random.choice( colors ), line, clear) )
        time.sleep( 0.05 )