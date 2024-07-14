from bitAdder import full_adder, half_adder
from nBitCA import nBitRCA
from convertion import bitStrToNum, numToBitstr

def shiftMul(bitStr0, bitStr1):

    #print(f"bitStr0: {bitStr0}, decimal: {bitStrToNum(bitStr0, 'int32')}")
    #print(f"bitStr1: {bitStr1}, decimal: {bitStrToNum(bitStr1, 'int32')}")

    bitLen = len(bitStr0)
    result = '0' * bitLen

    carryOut = '0'

    for i in range(bitLen-1, -1, -1):
        if bitStr1[i] == '1':
            shiftedBitstr0 = bitStr0 + '0'*(bitLen-1-i)
            result = '0'*(len(shiftedBitstr0)-len(result))+result
            result, carryOut = nBitRCA(result, shiftedBitstr0, carryOut)
            result = carryOut + result           
        else:
            pass

    #print(f"result: {result}, decimal: {bitStrToNum(result, 'int32')}")
    return result


def main():

    num0 = '125'
    num1 = '125'
    precision = 'int32'

    bitStr0 = numToBitstr(num0, precision)
    bitStr1 = numToBitstr(num1, precision)

    checkResult = shiftMul(bitStr0, bitStr1)

    print("Result of " + num0 + "x" + num1 + f": {bitStrToNum(checkResult, precision)}")
    
    print(f"Bit String of Result: {checkResult}")

    if bitStrToNum(checkResult, precision) == int(num0)*int(num1):
        print(True)
    else:
        print(False)

if __name__ == "__main__":
    main()