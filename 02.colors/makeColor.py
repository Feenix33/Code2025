"""
Dumb utility program to convert colors.csv to various formats

input a string for the output example for pygame 
    c=(r,g,b) 
    field names: name=c, family=f, hex=h, rgb
    or maybe
      c/C=color as is (camel case)
      N=upper case
      n=lower case
      some other for lower/camel/upper with _ between names
    hex format
      h=#hex
      H=#HEX
      x=0xhex
      X=0xHEX

flags
 -c# color min width
 -t  rgb are 3 spaces wide
 -i  input file
 -a str to add to fmt string (eg color prefix) also z for more
 -s color in snake case (auto to lowercase)
    

output filename

NAME,FAMILY,HEX,RED,GREEN,BLUE
 0    1      2   3    4    5
"""
#TODO
# add flag to put '' around values? -t (text)

import csv
import argparse

FILENAME = "refColors.csv"
FmtOut = "{color}=({red:>3},{green:>3},{blue:>3})\n"
FmtRGB = ""
FmtColor = ""
args = None
FmtA = ""
FmtZ = ""
FmtSnake = False

#processing flags
upColor = False
loColor = False
upHex = False
loHex = False
xoHex = False

def prepOutstring(instr):
    global upColor, loColor, xoHex, upHex, loHex
    global FmtA, FmtZ, FmtSnake
    outstr = ""
    for letter in instr:
        match letter:
            case 'r':
                outstr += "{red" + FmtRGB + "}"
            case 'g':
                outstr += "{green" + FmtRGB + "}"
            case 'b':
                outstr += "{blue" + FmtRGB + "}"
            case 'f':
                outstr += "{family}"
            case 'c':
                outstr += "{color" + FmtColor + "}"
            case 'n':
                outstr += "{color" + FmtColor + "}"
                loColor = True
            case 'N':
                outstr += "{color" + FmtColor + "}"
                upColor = True
            case 'x':
                outstr += "{chex}"
                loHex = True
                xoHex = True
            case 'X':
                outstr += "{chex}"
                upHex = True
                xoHex = True
            case 'h':
                outstr += "{chex}"
                loHex = True
            case 'H':
                outstr += "{chex}"
                upHex = True
            case 'a':
                outstr += "{aStr}"
            case 'z':
                outstr += "{zStr}"
            case _:
                outstr += letter
    outstr += '\n'
    return outstr

def processLine(fout, parms):
    global upColor, loColor, xoHex, upHex, loHex
    global FmtA, FmtZ, FmtSnake

    if FmtSnake:
        color = camel2snake(parms[0])
    elif upColor:
        color = parms[0].upper()
    elif loColor:
        color = parms[0].lower() 
    else:
        color = parms[0]
    family = parms[1]
    if xoHex:
        chex = "0x" + parms[2][2:]
    else:
        chex = parms[2]
    if upHex:
        chex = chex.upper()
    elif loHex:
        chex = chex.lower()
    red = parms[3]
    green = parms[4]
    blue = parms[5]
    aStr = FmtA
    zStr = FmtZ

    message = FmtOut.format(color=color, family=family,chex=chex,
                            red=red,green=green,blue=blue,
                            aStr=aStr, zStr=zStr)
    fout.write(message)

def camel2snake(s):
    result = s[0].lower()
    for c in s[1:]:
        if c.isupper():
            result += '_' + c.lower()
        else:
            result += c
    return result
    
def main():
    global FmtOut
    global args
    global FmtA, FmtZ, FmtSnake

    #print (FmtA, FmtZ)
    processArguments()
    #print (args)
    FmtOut = prepOutstring(args.formatString)
    #print (FmtOut)

    #fout = open('cme.py', 'w', encoding='utf-8')
    fout = open(args.outFilename, 'w', encoding='utf-8')
    with open(FILENAME, mode='r') as csvfile:
        ctable = csv.reader(csvfile)
        next(ctable) # skip the header row
        for row in ctable:
            processLine(fout, row)
    fout.close()

def processArguments():
    global args
    global FmtRGB, FmtRGB, FmtSnake, FmtColor
    global FmtA, FmtZ

    parser = argparse.ArgumentParser(description="Utility program to format color definitions")
    parser.add_argument('formatString', help="Format string for output")
    parser.add_argument('outFilename', help="Output filename")
    parser.add_argument('-i','--inFilename', help="Input filename for color.csv")
    parser.add_argument('-a','--aString', help="User formatted a string")
    parser.add_argument('-z','--zString', help="User formatted z string")
    parser.add_argument('-t', dest='triRGB', action="store_true", help="Force rgb numbers to be 3 spaces wide")
    parser.add_argument('-c','--wColor', help="Min width of color name field")
    parser.add_argument('-s', dest='snake', action="store_true", help="Color names in snake case")
    args = parser.parse_args()
    #print (args)
    if args.aString != None: FmtA = args.aString
    if args.zString != None: FmtZ = args.zString
    FmtRGB = ":>3" if args.triRGB else ""
    FmtColor = "" if args.wColor== None else ":" + args.wColor
    if args.snake: 
        FmtSnake = True
        loColor = True
    
if __name__ == "__main__":
    main()
