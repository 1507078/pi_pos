import os,sys
import termios
import time
from lcd_display import lcd

total=0
current=0
operator=' '

def getchar():
    fd = sys.stdin.fileno()
    if os.isatty(fd):
	old = termios.tcgetattr(fd)
	new = termios.tcgetattr(fd)
        new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
        new[6] [termios.VMIN] = 1
        new[6] [termios.VTIME] = 0
        try:
            termios.tcsetattr(fd, termios.TCSANOW, new)
            termios.tcsendbreak(fd,0)
            ch = os.read(fd,7)
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, old)
    else:
        ch = os.read(fd,7)
    return(ch)


my_lcd = lcd()
my_lcd.display_string("Welcome".center(16), 1)
time.sleep(0.1)
my_lcd.display_string("*Welcome*".center(16), 1)
time.sleep(0.1)
my_lcd.display_string("**Welcome**".center(16), 1)
time.sleep(0.1)
my_lcd.display_string("***Welcome***".center(16), 1)

time.sleep(3)
my_lcd.clear()
my_lcd.display_string("0".rjust(16),2)

i=0
while 1 :
    ch=getchar()
    if ord(ch) >= ord('0') and ord(ch) <= ord('9') :
        current = current * 10 + int(ch)
        my_lcd.display_string(operator + str(current).rjust(15), 2)
    elif ch == '+' or ch == '-' or ch == '*' or ch == '/':
	print operator
        if operator == '+' :
	    total+= current
        elif operator == '-' :
	    total-= current
	elif operator == '*' :
	    total*= current
	elif operator == '/' :
	    total/= current
	elif operator == ' ' :
	    total = current
	current=0
        my_lcd.display_string(str(total).rjust(16),1)
        my_lcd.display_string(ch.ljust(16),2)
	operator=ch
        i=0
    elif ch == '=' :
        if operator == '+' :
            total+= current
        elif operator == '-' :
            total-= current
        elif operator == '*' :
            total*= current
        elif operator == '/' :
            total/= current
        elif operator == ' ' :
            total = current
        current=total
        my_lcd.display_string("Total".center(16,'*'),1)
        my_lcd.display_string(str(total).rjust(16),2)
        operator=' '
        i=0


    i+=1
    if i >14 :
        my_lcd.display_string("Err",2)
        i=0
#my_lcd.display_string("Sophie", 2)

