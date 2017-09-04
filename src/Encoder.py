#!/usr/bin/python
# -*- coding: UTF-8 -*-

import Utils
import sys, unicodedata, math, collections
from sets import Set

## txt: input string
## Src: Source of information (alphabet is the set of letters of 'str')
## k: precision of integers Alpha and Beta
def arithmeticEncode(txt, src, k):


    ######################################
    ######### 1.- Initialization #########
    ######################################

    alpha = '0' * k   #Lower bound, String
    beta = '1' * k    #Upper bound, String
    u = 0

    print "TEXT: " + txt

    index = 0
    code = ''
    for l in txt:

        ######################################
        ######### 2/3.- INTERVALS ###########
        ######################################

        #Update interval
        #Delta as decimal
        delta = int(Utils.convertToDec(beta)) - int(Utils.convertToDec(alpha)) + 1
        upperDec = int(math.floor(delta * Utils.getLetterPi(l, src))) - 1
        lowerDec = int(math.floor(delta * Utils.getLetterPiPrevious(l, src)))

        beta = Utils.convertToBinary(Utils.convertToDec(alpha) + upperDec, k)
        alpha = Utils.convertToBinary(Utils.convertToDec(alpha) + lowerDec, k)

        ######################################
        ######### NORMALIZATION ############
        ######################################

        beta = beta[:k]
        alpha = alpha[:k]

        alphaAsStr = alpha
        betaAsStr = beta

        ######################################
        ######### 4.- RESCALING ############
        ######################################
        isRescaled = False

        while not isRescaled:

            if(betaAsStr[0] == alphaAsStr[0]):
                bitToAppend = alphaAsStr[0]
                code = code + bitToAppend
                betaAsStr = betaAsStr[1:] + "1"
                alphaAsStr = alphaAsStr[1:] + "0"
                if(bitToAppend == "1"):
                    code = code + ("0" * u)
                else:
                    code = code + ("1" * u)
                u = 0

            else:
                isRescaled = True

                ######################################
                ########### 5.- UNDERFLOW ############
                ######################################
                underFlow = True
                while underFlow:

                    if((betaAsStr[1] == "0") and (alphaAsStr[1] == "1")):

                        u = u + 1
                        alphaAsStr = alphaAsStr[0] + alphaAsStr[2:] + "0"
                        betaAsStr = betaAsStr[0] + betaAsStr[2:] + "1"

                    else:
                        underFlow = False

                beta = betaAsStr
                alpha = alphaAsStr

        index = index + 1

    #The code c has to be updated so that while decoding it produces a value between alpha and Beta, and this is achieved by just appending a 1 to it
    code = code + "1"
    return code


## bin: List of binary codes
## Src: Source of information (alphabet is the set of letters of 'str')
## k: precision of integers Alpha, Beta and gamma
## length: number of letters of the original string (whose code is bin)
def arithmeticDecode(binCode, src, k, length):

    alpha = "0" * k
    beta = "1" * k
    gamma = binCode[:k]
    gamma = gamma.ljust(k, "0")

    codeNotUsedYet = binCode[k:]
    decodedText = ''
    index = 0

    while index < length:

        gammaDec = Utils.convertToDec(gamma)

        searching = True
        tuplInd = 0
        while searching:

            l = src[tuplInd][0]

            delta = int(Utils.convertToDec(beta)) - int(Utils.convertToDec(alpha)) + 1

            lowerDec = int(math.floor(delta * Utils.getLetterPiPrevious(l, src)))
            upperDec = int(math.floor(delta * Utils.getLetterPi(l, src))) - 1

            subAlpha = Utils.convertToBinary(Utils.convertToDec(alpha) + lowerDec, k)[:k]
            subBeta = Utils.convertToBinary(Utils.convertToDec(alpha) + upperDec, k)[:k]
            subAlphaDec = Utils.convertToDec(subAlpha)
            subBetaDec = Utils.convertToDec(subBeta)

            if(subBetaDec >= gammaDec and subAlphaDec <= gammaDec):

                searching = False
                decodedText = decodedText + l
                alpha = subAlpha
                beta = subBeta

                #Rescaling
                isRescaled = False
                while not isRescaled:

                    if(alpha[0] == beta[0]):

                        alpha = alpha[1:] + "0"
                        beta = beta[1:] + "1"

                        gammaChar = "0"
                        if(len(codeNotUsedYet) > 0):

                            gammaChar = codeNotUsedYet[0]
                            codeNotUsedYet = codeNotUsedYet[1:]


                        gamma = gamma[1:] + gammaChar
                    else:
                        isRescaled = True

                isUnderflowed = True
                while isUnderflowed:

                    if(alpha[1] == "1" and beta[1] == "0"):

                        alpha = alpha[0] + alpha[2:] + "0"
                        beta = beta[0] + beta[2:] + "1"

                        gammaChar = "0"
                        if(len(codeNotUsedYet) > 0):

                            gammaChar = codeNotUsedYet[0]
                            codeNotUsedYet = codeNotUsedYet[1:]


                        gamma = gamma[0] + gamma[2:] + gammaChar

                    else:
                        isUnderflowed = False

            else:

                tuplInd = tuplInd + 1
                if(tuplInd >= len(src)):
                    searching = False
                    print "Error while searching. Index Out of bounds."

        index = index + 1


    return decodedText
