from logicGates import LogicGates
from nBitCA import nBitRCA

def binarySort(binaryStr0, binaryStr1):
    newBinaryStr0 = binaryStr0
    newBinaryStr1 = binaryStr1
    for i in range(len(binaryStr0)):
        if binaryStr0[i] == '1' and binaryStr1[i] == '0':     
            return newBinaryStr0, newBinaryStr1, '0'
        elif binaryStr1[i] == '1' and binaryStr0[i] == '0':
            return newBinaryStr1, newBinaryStr0, '1'
        else:
            pass
    return newBinaryStr0, newBinaryStr1, '0'

def getGap(str0, str1):
    bigger, smaller, p = binarySort(str0, str1)
    smaller = getMinus(smaller)
    gap, throwedCarry = nBitRCA(bigger, smaller)
    return gap, p

def getMinus(mantissaStr):
    reversedMantissaStr = ''
    just1 = ''
    bitLen = len(mantissaStr)

    for bit in mantissaStr:
        bit = LogicGates.notGate(bit)
        reversedMantissaStr = reversedMantissaStr + bit

    for i in range(bitLen-1):
        just1 = just1 + '0'
    just1 = just1 + '1'

    sumStr, carry = nBitRCA(reversedMantissaStr, just1)

    return sumStr

def leftShift(dataStr, shiftBitStr):
    length = len(dataStr)
    newDataStr = dataStr
    lenShiftStr = len(shiftBitStr)
    for i in range(lenShiftStr):
        #print(f'position:{i}')
        if shiftBitStr[lenShiftStr-1-i]=='1':
            addZeroToEnd = newDataStr + '0'*(2**i)
            #print(f'addZero: {addZeroToEnd}')
            newDataStr = addZeroToEnd[2**i:]
            #print(f'new:{newDataStr}')
    return newDataStr

def rightShift(dataStr, shiftBitStr):
    length = len(dataStr)
    newDataStr = dataStr
    lenShiftStr = len(shiftBitStr)
    for i in range(lenShiftStr):
        #print(f'position:{i}')
        if shiftBitStr[lenShiftStr-1-i]=='1':
            addZeroToEnd = '0'*(2**i) + newDataStr
            #print(f'addZero: {addZeroToEnd}')
            newDataStr = addZeroToEnd[0:length]
            #print(f'new:{newDataStr}')
    return newDataStr

def subWithAustrainMethod(strGreater, strSmaller):
    dataLen = len(strGreater)
    austrian = '0'
    result = ''
    for i in range(dataLen-1, -1, -1):
        if strGreater[i] == '1' and strSmaller[i] == '0' and austrian == '0':
            result = '1' + result
        elif strGreater[i] == '1' and strSmaller[i] == '0' and austrian == '1':
            result = '0' + result
        elif strGreater[i] == '1' and strSmaller[i] == '1' and austrian == '0':
            result = '0' + result
        elif strGreater[i] == '1' and strSmaller[i] == '1' and austrian == '1':
            result = '1' + result
            austrian = '1'
        elif strGreater[i] == '0' and strSmaller[i] == '0' and austrian == '0':
            result = '0' + result
        elif strGreater[i] == '0' and strSmaller[i] == '0' and austrian == '1':
            result = '1' + result
            austrian = '1'
        elif strGreater[i] == '0' and strSmaller[i] == '1' and austrian == '0':
            result = '1' + result
            austrian = '1'
        elif strGreater[i] == '0' and strSmaller[i] == '1' and austrian == '1':
            result = '0' + result
            austrian = '1'
    return result




def main():
    a = subWithAustrainMethod('1001', '0010')
    print(a)

if __name__ == "__main__":
    main()
