#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, unicodedata, math, collections
from sets import Set


##------------------------------------------------------------------------------
##-------------------------- READING FROM FILE SOURCE --------------------------
##------------------------------------------------------------------------------

#Extracts the text from a file.
def readFromFile(filein):

    file = open(filein, 'r')
    contents = file.read()
    file.close()
    return contents

#Outputs de k-th extensions of a given source src
def sourceExtension(src, k):

    if(k == 1):
        return src

    else:
        ext = sourceExtension(src,  k - 1)
        extendedSrc = []
        for firstKey in ext:
            for secondKey in ext:
                #print(firstKey + " " + secondKey + " " + str(ext[firstKey]) + " " + str(ext[secondKey]))
                extendedSrc.append((firstKey[0] + secondKey[0], firstKey[1] * secondKey[1]))

        return extendedSrc


##------------------------------------------------------------------------------
##---------------------------COMPUTATION OF ENTROPIES---------------------------
##------------------------------------------------------------------------------
#Given a text, returns its alphabet of symbols.
def getTextAlphabet(text):

    return list(Set(text))


#Returns a single letter probability probability computed from given text.
def getSingleLetterProbability(letter, text):

    count = text.count(letter)
    return float(count)/len(text)


#Returns a single letter probability probability computed from given text.
def getSingleLetterCount(letter, text):

    return text.count(letter)

#Returns the symbols probabilities in a dictionary to relate them to its letter.
def getSymbolsProbs(str):

    source = []
    alphabet = getTextAlphabet(str)
    for letter in alphabet:
        letterProb = getSingleLetterProbability(letter, str)
        source.append((letter, letterProb))

    source.reverse()
    return source


##------------------------------------------------------------------------------
##---------------------------------- HELPERS -----------------------------------
##------------------------------------------------------------------------------

#todo: im sure this is not even the best way to conver to binary and decimal
def convertToBinary(dec, k):
    return "{0:b}".format(dec).zfill(k)


def convertToDec(bin):
    return int(bin, 2)

def getLetterPi(letter, src):

    pi_i = 0
    for tupl in src:
        pi_i = pi_i + tupl[1]
        if(tupl[0] == letter):
            return pi_i

    print "JUSTPI: Letter not in src! Are you sure the src corresponds to the text passed?"
    return 0

def getLetterPiPrevious(letter, src):
    pi_i_1 = 0
    for tupl in src:
        if(tupl[0] == letter):
            return pi_i_1
        pi_i_1 = pi_i_1 + tupl[1]

    print "PiPrev: Letter not in src! Are you sure the src corresponds to the text passed?"
    return 0


# Computes a length of K that is enough for the code,
# as seen in slide numb. 56
def computeMinimumLength(src, text):

    totalW = 0
    for tupl in src:
        totalW = totalW + getSingleLetterCount(tupl[0], text)

    return math.ceil(math.log(totalW, 2)) + 2
