from bitAdder import full_adder

def nBitRCA(nBitDataStr0, nBitDataStr1, carryIn='0'):
    sum = ''
    bitOfDataStr0 = len(nBitDataStr0)
    bitOfDataStr1 = len(nBitDataStr1)
    if not bitOfDataStr0 == bitOfDataStr1:
        raise ValueError(f'nBitRCA is expecting for two data with same bit length!\nThe first input: {bitOfDataStr0} bits\nThe second input: {bitOfDataStr1} bits')
    else:
        for i in range(bitOfDataStr0-1, -1, -1):
            s, carryOut = full_adder(nBitDataStr0[i], nBitDataStr1[i], carryIn)
            sum = s + sum
            carryIn = carryOut
        return sum, carryOut

'''
def nBitBCA(nBitDataStr0, nBitDataStr1, carry='0'):
    sumStr = ''

    bitOfDataStr0 = len(nBitDataStr0)
    bitOfDataStr1 = len(nBitDataStr1)

    if not bitOfDataStr0 == bitOfDataStr1:
        raise ValueError(f'nBitBCA is expecting for two data with same bit length!')
    else:
        bitLen = bitOfDataStr0
        for i in range(bitLen):
            if(i==0):
                sum, carry_out = full_adder(nBitDataStr0[bitLen-1-i], nBitDataStr1[bitLen-1-i], carry)
            else:
                sum, carry_out = full_adder(nBitDataStr0[bitLen-1-i], nBitDataStr1[bitLen-1-i], carry_out)
            sumStr = sum + sumStr
        return sumStr, carry_out
'''




def main():
    a = nBitRCA('10001', '11100', '0')
    print(a)
    print('True Value: 01101')

if __name__ == "__main__":
    main()
