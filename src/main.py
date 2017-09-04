#!/usr/bin/python
# -*- coding: UTF-8 -*-
import Encoder, Utils
import sys, getopt

def usage():

    print ('Usage: main.py -i <inputfile>')
    sys.exit(2)

def main(argv):

    if len(argv) < 2:
         usage()
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-i", "--ifile"):
            filein = arg
        elif opt in ("-s", "--source"):
            filein = arg


    print ("Reading from file " + filein)
    result = Utils.readFromFile(filein)
    result = result.replace('\n','').replace('\r', '')

    print Utils.getTextAlphabet(result)

    print ('')
    print("Source from string")
    src = Utils.getSymbolsProbs(result)
    print (src)

    txt = result
    print ('')
    print ("Minim. length (optimal?): ")
    k =  int(Utils.computeMinimumLength(src, txt))
    print k

    print "Going to encode text: " + txt
    print ('')
    print ("Arithmetic encoding: ")
    codeword = Encoder.arithmeticEncode(txt, src, k)
    print ("Arithmetic encoding FINISHED. Codeword: " + codeword)

    print ('')
    print ('')
    print ("Arithmetic decoding: ")
    decodedText =  Encoder.arithmeticDecode(codeword, src, k, len(txt))
    print ("Arithmetic decoding FINISHED. Decoded text:  " + decodedText)

    print ("")
    print "Before: " + txt
    print "Code word: " + codeword
    print "After: " + decodedText
    print "Is the text the same?: " + str((txt == decodedText))

if __name__ == "__main__":
   main(sys.argv[1:])
