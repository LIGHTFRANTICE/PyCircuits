from logicGates import LogicGates
from nBitCA import nBitBCA

def binarySort(binaryStr0, binaryStr1):
    for i in range(len(binaryStr0)):
        if binaryStr0[i] == '1' and binaryStr1[i] == '0':
            return binaryStr0, binaryStr1, '0'
        elif binaryStr0[i] == '1' and binaryStr1[i] == '0':
            return binaryStr1, binaryStr0, '1'
        else:
            pass
    return binaryStr0, binaryStr1


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

    sumStr, carry = nBitBCA(reversedMantissaStr, just1)

    return sumStr

def leftShift(dataStr, shiftBitStr):
    length = len(dataStr)
    newDataStr = dataStr
    lenShiftStr = len(shiftBitStr)
    for i in range(lenShiftStr):
        print(f'position:{i}')
        if shiftBitStr[lenShiftStr-1-i]=='1':
            addZeroToEnd = newDataStr + '0'*(2**i)
            print(f'addZero: {addZeroToEnd}')
            newDataStr = addZeroToEnd[2**i:]
            print(f'new:{newDataStr}')
    return newDataStr

def rightShift(dataStr, shiftBitStr):
    length = len(dataStr)
    newDataStr = dataStr
    lenShiftStr = len(shiftBitStr)
    for i in range(lenShiftStr):
        print(f'position:{i}')
        if shiftBitStr[lenShiftStr-1-i]=='1':
            addZeroToEnd = '0'*(2**i) + newDataStr
            print(f'addZero: {addZeroToEnd}')
            newDataStr = addZeroToEnd[0:length]
            print(f'new:{newDataStr}')
    return newDataStr

def main():
    a = rightShift('1010100', '0010')
    print(a)

if __name__ == "__main__":
    main()
