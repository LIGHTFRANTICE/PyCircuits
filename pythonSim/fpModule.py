from logicGates import LogicGates
import bitAdder
from nBitCA import nBitBCA
from bitTools import getMinus, binarySort
from bitTools import rightShift

class fpModule:

    def __init__(self, dataStr0, dataStr1, precision):
        self.precision = precision
        self.dataStr0 = dataStr0
        self.dataStr1 = dataStr1
        
        self.sign0 = self.dataStr0[0]
        self.sign1 = self.dataStr1[0]

        if self.precision == 'fp32':
            self.exponent0 = self.dataStr0[1:8]
            self.mantissa0 = self.dataStr0[9:31]
            self.exponent1 = self.dataStr1[1:8]
            self.mantissa1 = self.dataStr1[9:31]
        elif self.precision == 'fp16':
            self.exponent0 = self.dataStr0[1:5]
            self.mantissa0 = self.dataStr0[6:15]
            self.exponent1 = self.dataStr1[1:5]
            self.mantissa1 = self.dataStr1[6:15]
        elif self.precision == 'fp8':
            self.exponent0 = self.dataStr0[1:4]
            self.mantissa0 = self.dataStr0[5:7]
            self.exponent1 = self.dataStr1[1:4]
            self.mantissa1 = self.dataStr1[5:7]
        else:
            raise ValueError(f"Unsupported precision type: {self.precision}")
   
            
    def fp32Adder(self):

        if self.sign0 == '0':
            self.mantissa0 = getMinus(self.mantissa0)
        if self.sign1 == '0':
            self.mantissa1 = getMinus(self.mantissa1)
        
        if self.exponent0 == self.exponent1:
            sumMantissa = nBitBCA('1'+self.mantissa0, '1'+self.mantissa1)
        else:
            binaryStr0, binaryStr1, biggerStr = binarySort(self.exponent0, self.exponent1)
            reversedBinaryStr1 = getMinus(binaryStr1)
            exponentGap = nBitBCA(binaryStr0, reversedBinaryStr1)
            if biggerStr == '0':
                sumMantissa = nBitBCA('1'+self.mantissa0, rightShift('1'+self.mantissa1, exponentGap))
            else:
                sumMantissa = nBitBCA(rightShift('1'+self.mantissa0, exponentGap), '1'+self.mantissa1)

        result = 
        return result


        
def main():
    a = getMinus('1010100')
    print(a)

if __name__ == "__main__":
    main()