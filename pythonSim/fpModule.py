from nBitCA import nBitRCA
from nBitMul import shiftMul

from bitTools import getMinus, getGap
from bitTools import rightShift

from convertion import bitStrToNum, numToBitstr


class fpModule:

    def __init__(self, dataStr0, dataStr1, precision):
        self.precision = precision

        self.sign0 = dataStr0[0]
        self.sign1 = dataStr1[0]

        if self.precision == 'fp64':
            self.exponent0 = dataStr0[1:12]
            self.significand0 = dataStr0[12:]
            self.exponent1 = dataStr1[1:12]
            self.significand1 = dataStr1[12:]
            self.significandBits = 53
            self.lenOfExponent = 11
            self.bias = '01111111111'
        elif self.precision == 'fp32':
            self.exponent0 = dataStr0[1:9]
            self.significand0 = dataStr0[9:]
            self.exponent1 = dataStr1[1:9]
            self.significand1 = dataStr1[9:]
            self.significandBits = 24
            self.lenOfExponent = 8
            self.bias = '01111111'
        elif self.precision == 'fp16':
            self.exponent0 = dataStr0[1:6]
            self.significand0 = dataStr0[6:]
            self.exponent1 = dataStr1[1:6]
            self.significand1 = dataStr1[6:]
            self.significandBits = 11
            self.lenOfExponent = 5
            self.bias = '01111'
        elif self.precision == 'fp8':
            self.exponent0 = dataStr0[1:5]
            self.significand0 = dataStr0[5:]
            self.exponent1 = dataStr1[1:5]
            self.significand1 = dataStr1[5:]
            self.significandBits = 4
            self.lenOfExponent = 4
            self.bias = '0111'
        elif self.precision == 'bf16':
            self.exponent0 = dataStr0[1:9]
            self.significand0 = dataStr0[9:]
            self.exponent1 = dataStr1[1:9]
            self.significand1 = dataStr1[9:]
            self.significandBits = 8
            self.lenOfExponent = 8
            self.bias = '01111111'
        else:
            raise ValueError(f"Unsupported precision type: {self.precision}")

    def adder(self):
        significandBits = self.significandBits
        lenOfExponent = self.lenOfExponent

        if self.sign0 == self.sign1:
            # set sign to sign0
            sign = self.sign0

            # print(f'sign: {sign}')

            # get the sub of exponents
            exponentGap, theBiggerIs = getGap(self.exponent0, self.exponent1)

            #print(f'exGap: {exponentGap}\ntheBiggerIs: {theBiggerIs}')

            # when exponent0 is bigger
            if theBiggerIs == '0':
                # right shift significand1 to set exponent1 the same to exponent0
                significand1 = rightShift('1' + self.significand1, exponentGap)

                #print(f"significand0: {'1' + self.significand0}")
                #print(f'significand1: {significand1}')

                # set exponent to exponent0
                exponent = self.exponent0

                #print(f'exponent: {exponent}')

                # add two significands
                significand, carryOut = nBitRCA('1'+self.significand0, significand1)

                #print(f'significand: {significand} \ncarryOut: {carryOut}')

                if carryOut == '1':
                    significand = '1' + significand

                #print(f'significand: {significand}')

                frontZeros = 0
                for i in significand:
                    if i == '1':
                        break
                    else:
                        frontZeros = frontZeros + 1

                significand = significand[frontZeros:]

                #print(f'significand: {significand}')

                lenOfsignificand = len(significand)

                #print(f'Length of significand: {lenOfsignificand}')

                if lenOfsignificand >= significandBits:
                    bitsToBeShifted = format(lenOfsignificand-significandBits, f'0{lenOfExponent}b')

                    #print(f'lenOfsignificand-significandBits: {lenOfsignificand-significandBits}')
                    #print(f'bitsToBeShifted: {bitsToBeShifted}')

                    exponent, throwedCarry = nBitRCA(exponent, bitsToBeShifted)
                    significand = rightShift(significand, bitsToBeShifted)
                    # throw away the '0's in the head
                    significand = significand[lenOfsignificand -
                                              significandBits:]
                else:
                    bitsToBeShifted = format(significandBits-lenOfsignificand, f'0{lenOfExponent}b')
                    exponent, throwedCarry = nBitRCA(exponent, getMinus(bitsToBeShifted))
                    significand = significand + '0' * (significandBits-lenOfsignificand)

                #print(f'exponent: {exponent}')

            else:
                significand0 = rightShift('1' + self.significand0, exponentGap)
                # set exponent to exponent1
                exponent = self.exponent1
                # add two significands
                significand, carryOut = nBitRCA(
                    '1'+self.significand1, significand0)

                if carryOut == '1':
                    significand = '1' + significand

                frontZeros = 0
                for i in significand:
                    if i == '1':
                        break
                    else:
                        frontZeros = frontZeros + 1
            
                significand = significand[frontZeros:]
                lenOfsignificand = len(significand)
                if lenOfsignificand >= significandBits:
                    bitsToBeShifted = format(
                        lenOfsignificand-significandBits, f'0{lenOfExponent}b')
                    exponent, throwedCarry = nBitRCA(exponent, bitsToBeShifted)
                    significand = rightShift(significand, bitsToBeShifted)
                else:
                    bitsToBeShifted = format(significandBits-lenOfsignificand, f'0{lenOfExponent}b')
                    exponent, throwedCarry = nBitRCA(exponent, getMinus(bitsToBeShifted))
                    significand = significand + '0' * (significandBits-lenOfsignificand)

        else:
            # get the sub of exponents
            exponentGap, theBiggerIs = getGap(self.exponent0, self.exponent1)

            if theBiggerIs == '0':

                significand1 = '1' + self.significand1

                # right shift significand1 to set exponent1 the same to exponent0
                significand1 = rightShift(significand1, exponentGap)

                # set exponent to exponent0
                exponent = self.exponent0

                significand, p = getGap('1' + self.significand0, significand1)

                if p == '0':
                    sign = self.sign0
                else:
                    sign = self.sign1

                frontZeros = 0
                for i in significand:
                    if i == '1':
                        break
                    else:
                        frontZeros = frontZeros + 1

                significand = significand[frontZeros:]
                lenOfsignificand = len(significand)
                if lenOfsignificand >= significandBits:
                    bitsToBeShifted = format(lenOfsignificand-significandBits, f'0{lenOfExponent}b')
                    exponent, throwedCarry = nBitRCA(exponent, bitsToBeShifted)
                    significand = rightShift(significand, bitsToBeShifted)
                    # throw away the '0's in the head
                    significand = significand[lenOfsignificand-significandBits:]
                else:
                    bitsToBeShifted = format(significandBits-lenOfsignificand, f'0{lenOfExponent}b')
                    exponent, throwedCarry = nBitRCA(exponent, getMinus(bitsToBeShifted))
                    significand = significand + '0' * (significandBits-lenOfsignificand)
            
            else:

                significand0 = '1' + self.significand0

                # right shift significand0 to set exponent0 the same to exponent1
                significand0 = rightShift(significand0, exponentGap)

                # set exponent to exponent1
                exponent = self.exponent1

                significand, p = getGap(significand0, '1'+self.significand1)
                
                if p == '0':
                    sign = self.sign0
                else:
                    sign = self.sign1  

                frontZeros = 0
                for i in significand:
                    if i == '1':
                        break
                    else:
                        frontZeros = frontZeros + 1

                significand = significand[frontZeros:]
                lenOfsignificand = len(significand)
                if lenOfsignificand >= significandBits:
                    bitsToBeShifted = format(lenOfsignificand-significandBits, f'0{lenOfExponent}b')
                    exponent, throwedCarry = nBitRCA(exponent, bitsToBeShifted)
                    significand = rightShift(significand, bitsToBeShifted)
                    significand = significand[lenOfsignificand-significandBits:]# throw away the '0's in the head
                else:
                    bitsToBeShifted = format(significandBits-lenOfsignificand, f'0{lenOfExponent}b')
                    exponent, throwedCarry = nBitRCA(exponent, getMinus(bitsToBeShifted))
                    significand = significand + '0' * (significandBits-lenOfsignificand)

        if exponent == '1' * self.lenOfExponent:
            significand = '0' * (self.significandBits-1)

        # print(f'significand: {significand}')
        return sign + exponent + significand[1:]

    def mult(self):

        # decide sign
        if self.sign0 == self.sign1:
            sign = '0'
        else:
            sign = '1'
        
        # add two exponents
        exponent, carryOut = nBitRCA(self.exponent0, self.exponent1)
        
        exponent, throwedCarry = nBitRCA(carryOut+exponent, getMinus('0' + self.bias))
        
        if exponent[0] == '1':
            raise ValueError("The Result is OVERFLOW!")
        else:
            exponent = exponent[1:]
 
        #print(f'exponent: {exponent}')

        significand0 = '1' + self.significand0
        significand1 = '1' + self.significand1  

        #print(f'significand0: {significand0}')
        #print(f'significand1: {significand1}')

        significand = shiftMul(significand0, significand1)

        #print(f'significand: {significand}')


        frontZeros = 0
        for i in significand:
            if i == '1':
                break
            else:
                frontZeros = frontZeros + 1

        significand = significand[frontZeros:self.significandBits+1]

        #print(f'significand: {significand}')

        lenOfsignificand = len(significand)
        if lenOfsignificand >= self.significandBits:
            bitsToBeShifted = format(lenOfsignificand-self.significandBits, f'0{self.lenOfExponent}b')
            exponent, throwedCarry = nBitRCA(exponent, bitsToBeShifted)
        
            significand = rightShift(significand, bitsToBeShifted)
            significand = significand[lenOfsignificand-self.significandBits:]# throw away the '0's in the head
        else:
            bitsToBeShifted = format(self.significandBits-lenOfsignificand, f'0{self.lenOfExponent}b')
            exponent, throwedCarry = nBitRCA(exponent, getMinus(bitsToBeShifted))
            
            significand = significand + '0' * (self.significandBits-lenOfsignificand)

        if exponent == '1' * self.lenOfExponent:
            if significand is not '0' * (self.significandBits-1):
                raise ValueError("The Result is OVERFLOW!")

        return sign + exponent + significand[1:]     



        

def main():

    num0 = '-173.25'
    num1 = '147.25'
    precision = 'fp16'

    if precision == 'fp64':
        roundUp = '.14e'
    elif precision == 'fp32':
        roundUp = '.6e'
    elif precision == 'fp16':
        roundUp = '.2e'
    elif precision == 'fp8':
        roundUp = '.0e'

    bitStr0 = numToBitstr(num0, precision)
    bitStr1 = numToBitstr(num1, precision)

    checkResult = fpModule(bitStr0, bitStr1, precision).mult()

    print("Result of " + num0 + " × " + num1 + f": {bitStrToNum(checkResult, precision)}")

    print(f'True: {format(float(num0)*float(num1), roundUp)}')
    if format(bitStrToNum(checkResult, precision), roundUp) == format(float(num0)*float(num1), roundUp):
        print(True)
    else:
        print(False)


if __name__ == "__main__":
    main()
