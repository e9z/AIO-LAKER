#~ 1337JO
#~ CODED BY LAKER HACKER
#~ PRIV8 TOOL 2021
#~ GOOD LUCK ~
import requests,os
from colorama import Fore,init
init(autoreset=True)

g = Fore.WHITE
r = Fore.RED
b = Fore.RED
w = Fore.YELLOW

if os.name == "nt":
	os.system("cls")
else:
	os.system("clear")
	
def print_logo():
    clear = "\x1b[0m"
    colors = [36, 32, 34, 35, 31, 37]
banner = """
{}
  
██╗      █████╗ ██╗  ██╗███████╗██████╗     ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
██║     ██╔══██╗██║ ██╔╝██╔════╝██╔══██╗    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║     ███████║█████╔╝ █████╗  ██████╔╝    ███████║███████║██║     █████╔╝ █████╗  ██████╔╝
██║     ██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗    ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
███████╗██║  ██║██║  ██╗███████╗██║  ██║    ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                            
                                                                                            
                                        
                                                                                                                                                                                            
 {}[{}+{}] INSTA :  @E9_Z_                   {}[{}+{}] TELEGRAM : @LAKER305  
 {}[{}+{}] Github : @e9z                     {}[{}+{}] - LAKER HACKER -

 {}================================================================================{}
 [{}1{}]  DORK MAKER    
 [{}2{}]  DORK SCANNER 
 [{}3{}]  0xDORK BY LAKER 
 [{}4{}]  DOMIN TO IP 
 [{}5{}]  CMS DETECT 
 [{}6{}]  ALL CMS BRUTER 
 [{}7{}]  Paypal Email Cheacker
 [{}8{}]  Amazon Email Cheaker 
 [{}9{}]  Find Path (KCFINDER)
 [{}10{}] JEX SCANNER v1.3 
 [{}11{}] HASH ID  
 [{}12{}] Mass PHP UNIT RCE SCANNER  
 [{}13{}] SMTP CRACKER 
"""
print(banner.format(g,b,g,w,r,b,g,r,g,r,g,r,g,b,g,b,g,b,g,b,g,b,g,b,g,b,g,b,g,b,g,b,g,b,g,b,g,b,g,b,g,b,g,b,g,b,g,b,g,b,g,b,g))
tool = input("choose:")
if tool == "1":
	os.chdir("Tools/TOOL1")
	os.system("python3 dorkmaker.py")
	
elif tool == "2":
	os.chdir("Tools/TOOL2")
	os.system("python3 dorkscanner.py")
	
elif tool == "3":
	os.chdir("Tools/TOOL3")
	os.system("python3 0dorks.py")
		
elif tool == "4":
	os.chdir("Tools/TOOL4")
	os.system("python ipfromdomain.py ")
	
elif tool == "5":
	os.chdir("Tools/TOOL5")
	os.system("python cms.py")
		
elif tool == "6":
	os.chdir("Tools/TOOL6")
	os.system("python bruter.py")
	
elif tool == "7":
	os.chdir("Tools/TOOL7")
	os.system("python check.py")
	
	
elif tool == "8":
	os.chdir("Tools/TOOL8")
	os.system("python3 amazon.cheacker.py")
	
elif tool == "9":
	os.chdir("Tools/TOOL9")
	os.system("python3 find.py")
	
elif tool == "10":
	os.chdir("Tools/TOOL10")
	os.system("python3 main.py")

elif tool == "11":
	os.chdir("Tools/TOOL11")
	os.system("python hash.py")

elif tool == "12":
	os.chdir("Tools/TOOL12")
	os.system("php phpunit.php")

elif tool == "13":
	os.chdir("Tools/TOOL13")
	os.system("python2 smtp.py")
	
