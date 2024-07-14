from nBitCA import nBitRCA
from nBitMul import shiftMul

from bitTools import getMinus, getGap
from bitTools import rightShift

from convertion import bitStrToNum, numToBitstr


class intModule:

    def __init__(self, dataStr0, dataStr1, precision):
        self.precision = precision
        self.dataStr0 = dataStr0
        self.dataStr1 = dataStr1

        self.sign0 = dataStr0[0]
        self.sign1 = dataStr1[0]
        self.data0 = dataStr0[1:]
        self.data1 = dataStr1[1:]
        
        if precision == 'int32':
            self.bitLen = 32
        elif precision == 'int16':
            self.bitLen = 16
        elif precision == 'int8':
            self.bitLen = 8
        else:
            raise ValueError(f"Unsupported precision type: {self.precision}")

    def adder(self):
        result, carryOut = nBitRCA(self.dataStr0, self.dataStr1)
        if carryOut == '1':
            raise ValueError('The Result is OVERFLOW!')
        else:
            return result
        
    def mult(self):
        
        if self.sign0 == '1':
            dataStr0 = getMinus(self.dataStr0)
        else:
            dataStr0 = self.dataStr0

        if self.sign1 == '1':
            dataStr1 = getMinus(self.dataStr1)
        else:
            dataStr1 = self.dataStr1
        
        print(f'num0: {bitStrToNum(dataStr0, self.precision)}')
        print(f'num1: {bitStrToNum(dataStr1, self.precision)}') 

        result = shiftMul(dataStr0, dataStr1)

        for i in result[:-(self.bitLen+self.bitLen)]:
            if i == '1':
                raise ValueError('The Result is OVERFLOW!')
            else:
                pass
        
        result = result[-(self.bitLen+self.bitLen):]

        if self.sign0 == self.sign1:
            return result
        else:
            return getMinus(result)
        

def main():

    num0 = '2147483647'
    num1 = '2147483647'
    precision = 'int32'

    bitStr0 = numToBitstr(num0, precision)
    bitStr1 = numToBitstr(num1, precision)

    checkResult = intModule(bitStr0, bitStr1, precision).mult()

    print(f"Bit String of Result: {checkResult}")

    print("Result of " + num0 + " × " + num1 + f": {bitStrToNum(checkResult, precision)}")

    print(f'True: {int(num0)*int(num1)}')
    if bitStrToNum(checkResult, precision) == int(num0)*int(num1):
        print(True)
    else:
        print(False)


if __name__ == "__main__":
    main()
