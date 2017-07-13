import os,sys
import termios
import datetime
from decimal import *

import send

log_path = "data/"

Operator_Symbol = ' '
Flag_Float = False

line_1_digital=0
line_1_float_len=0
line_2_digital=0
line_2_float_len=0

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

def log_money(money):
    currentDT = datetime.datetime.now()
    log_time = "%04d-%02d-%02d %02d:%02d:%02d" %(currentDT.year, currentDT.month, currentDT.day, currentDT.hour, currentDT.minute, currentDT.second)
    #print log_time
    log_date = "%04d-%02d-%02d-%02d-%02d-%02d" %(currentDT.year, currentDT.month, currentDT.day, currentDT.hour, currentDT.minute, currentDT.second)
    path= log_path + log_date +'.txt'
    s_file = open(path,'a')
    s_file.write(log_time + " $" + str(money)+'\n')
    s_file.close()
    send.do_send()
    
def MAX_LENGTH():
    return 5
def show_line():
    global line_1_digital
    global line_1_float_len
    global line_2_digital
    global line_2_float_len
    global Flag_Float
    global Operator_Symbol

    #print "line_1_digital:", line_1_digital
    #print "line_1_float_len", line_1_float_len
    #print "line_2_digital", line_2_digital
    #print "line_2_float_len", line_2_float_len
    f=0.0
    print "*******************"
    if Operator_Symbol == ' ':
        print "Line1: "
    else:
        if line_1_float_len == 0:
            print "Line1: ", str(line_1_digital)
        else:
            print 
            f = Decimal(line_1_digital) / Decimal(10 ** line_1_float_len)
            print "Line1: ", str(f)

            
    if line_2_float_len == 0 and line_2_digital == 0 and Flag_Float == False:
        print "Line2:", Operator_Symbol
    elif line_2_float_len == 0:
        if Flag_Float == False:
            print "Line2:", Operator_Symbol + str(line_2_digital)
        else:
            print "Line2:", Operator_Symbol + str(line_2_digital) + '.'
            
    else:
        f = Decimal(line_2_digital) / Decimal(10 ** line_2_float_len)
        print "Line2:", Operator_Symbol + str(f)
    print "==================="
    
def input_digitial(a):
    #print "a", a
    global line_2_digital
    global line_2_float_len
    global Flag_Float
    line_2_digital = line_2_digital*10 + a
    
    if line_2_float_len != 0 or Flag_Float == True:
        line_2_float_len = line_2_float_len + 1
    show_line()

def input_dot():
    global Flag_Float
    if Flag_Float == True:
        return
    Flag_Float = True
    show_line()
    
def input_operator(operator):
    global line_1_digital
    global line_2_digital
    global line_1_float_len
    global line_2_float_len
    global Operator_Symbol
    global Flag_Float
    #print "Operator_Symbol", Operator_Symbol
    f_1 = Decimal(line_1_digital) / Decimal(10 ** line_1_float_len)
    f_2 = Decimal(line_2_digital) / Decimal(10 ** line_2_float_len)
    
    if Operator_Symbol == '+':
        s = f_1 + f_2
        line_1_float_len = 0
        while line_1_float_len < MAX_LENGTH():
            if s == int(s):
                break;
            line_1_float_len += 1
            s *= 10
        line_1_digital = int(s)

    elif Operator_Symbol == '-':
        s = f_1 - f_2
        line_1_float_len = 0
        while line_1_float_len < MAX_LENGTH():
            if s == int(s):
                break;
            line_1_float_len += 1
            s *= 10
        line_1_digital = int(s)
        
    elif Operator_Symbol == '*':
        s = f_1 * f_2
        #print "s", s
        line_1_float_len = 0
        while line_1_float_len < MAX_LENGTH():
            #print "int_s", int(s)
            if s == int(s):
                break;
            line_1_float_len += 1
            s *= 10
        line_1_digital = int(s)
        
    elif Operator_Symbol == '/':
        s = f_1 / f_2
        line_1_float_len = 0
        while line_1_float_len < MAX_LENGTH():
            if s == int(s):
                break;
            line_1_float_len += 1
            s *= 10
        line_1_digital = int(s)
        
    elif Operator_Symbol == ' ':
        line_1_digital = line_2_digital
        line_1_float_len = line_2_float_len
        
    line_2_digital = 0
    line_2_float_len = 0
    Operator_Symbol = operator
    Flag_Float = False
    show_line()


    
def get_sum():
    global line_1_digital
    global line_2_digital
    global line_1_float_len
    global line_2_float_len
    global Operator_Symbol
    global Flag_Float
    f_1 = Decimal(line_1_digital) / Decimal(10 ** line_1_float_len)
    f_2 = Decimal(line_2_digital) / Decimal(10 ** line_2_float_len)
    if Operator_Symbol == '+':
        s = f_1 + f_2
        line_2_float_len = 0
        while line_2_float_len < MAX_LENGTH():
            if s == int(s):
                break;
            line_2_float_len += 1
            s *= 10
        line_2_digital = int(s)
        line_1_digital = 0
        line_1_float_len = 0
        Operator_Symbol = ' '
        if line_2_float_len == 0:
            Flag_Float = False
        show_line()
    elif Operator_Symbol == '-':
        s = f_1 - f_2
        line_2_float_len = 0
        while line_2_float_len < MAX_LENGTH():
            if s == int(s):
                break;
            line_2_float_len += 1
            s *= 10
        line_2_digital = int(s)
        line_1_digital = 0
        line_1_float_len = 0
        Operator_Symbol = ' '
        if line_2_float_len == 0:
            Flag_Float = False
        show_line()
    elif Operator_Symbol == '*':
        s = f_1 * f_2
        line_2_float_len = 0
        while line_2_float_len < MAX_LENGTH():
            if s == int(s):
                break;
            line_2_float_len += 1
            s *= 10
        line_2_digital = int(s)
        line_1_digital = 0
        line_1_float_len = 0
        Operator_Symbol = ' '
        if line_2_float_len == 0:
            Flag_Float = False
        show_line()
    elif Operator_Symbol == '/':
        if f_2 == 0:
            return
        s = f_1 / f_2
        line_2_float_len = 0
        while line_2_float_len < MAX_LENGTH():
            if s == int(s):
                break;
            line_2_float_len += 1
            s *= 10
        line_2_digital = int(s)
        line_1_digital = 0
        line_1_float_len = 0
        Operator_Symbol = ' '
        if line_2_float_len == 0:
            Flag_Float = False
        show_line()
    log_money(Decimal(line_2_digital) / Decimal(10 ** line_2_float_len))
    line_2_digital = 0
    line_2_float_len = 0


while 1:
	ret = getchar()
#	print "ret[0] ", ord(ret[0])
#	print "0 ", ord('0')
#	print "9 ", ord('9')
	if ord(ret[0]) >= ord('0') and ord(ret[0]) <= ord('9'):
#		print "number: ", ret[0]
		input_digitial(int(ret[0]))
	elif ord(ret[0]) == ord('+') or ord(ret[0]) == ord('-') or ord(ret[0]) == ord('*') or ord(ret[0]) == ord('/'):
#		print ret[0]
		input_operator(ret[0])
	elif ord(ret[0]) == 10:
		get_sum()
	else:
		print "other: ", ord(ret[0])	

#	i = 0
#	print "len", len(ret)
#	while i < len(ret):
#		print ord(ret[i])
#		i+=1
