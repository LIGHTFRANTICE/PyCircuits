#from multiprocessing import Pool
from bitAdder import full_adder

#def nBitRCA(nBitDataStr0, nBitDataStr1):
#    processNum = len(nBitDataStr0)


def nBitBCA(nBitDataStr0, nBitDataStr1, carry='0'):

    sumStr = ''
    bitLen = len(nBitDataStr0)

    for i in range(bitLen):
        if(i==0):
            sum, carry_out = full_adder(nBitDataStr0[bitLen-1-i], nBitDataStr1[bitLen-1-i], carry)
        else:
            sum, carry_out = full_adder(nBitDataStr0[bitLen-1-i], nBitDataStr1[bitLen-1-i], carry_out)

        sumStr = sum + sumStr

    return sumStr, carry_out

def main():
    a = nBitBCA('00101', '11100')
    print(a)

if __name__ == "__main__":
    main()
