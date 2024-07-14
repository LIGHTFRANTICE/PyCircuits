import argparse

from fpModule import fpModule
from intModule import intModule
from convertion import bitStrToNum, numToBitstr


def main():

    parser = argparse.ArgumentParser(description='Set precision and calculate mode.')
    
    parser.add_argument('-p', '--precision', choices=['fp64', 'fp32', 'fp16', 'fp8', 'bf16', 'int8', 'int16', 'int32'], help='Choose a precision', required=True)
    parser.add_argument('-c', '--calmode', choices=['add', 'mult'], help='Choose a calculating mode, add or mult.', required=True)
    
    parser.add_argument('data0', help='The first data to be calculated.')
    parser.add_argument('data1', help='The second data to be calculated.')

    args = parser.parse_args()

    #test args
    #print(args)

    mode = args.calmode

    precision = args.precision

    dataStr0 = numToBitstr(args.data0, precision)
    dataStr1 = numToBitstr(args.data1, precision)

    result = ''

    if mode == 'add':

        if precision == 'fp64' or precision == 'fp32' or precision == 'fp16' or precision == 'fp8' or precision == 'bf16':
            result = fpModule(dataStr0, dataStr1, precision).adder()
        elif precision == 'int32' or precision == 'int16' or precision == 'int8':
            result = intModule(dataStr0, dataStr1, precision).adder()

        else:
            raise TypeError(f"Unsupported precision type: {precision}")

    elif mode == "mult":

        if precision == 'fp64' or precision == 'fp32' or precision == 'fp16' or precision == 'fp8' or precision == 'bf16':
            result = fpModule(dataStr0, dataStr1, precision).mult()
        elif precision == 'int32' or precision == 'int16' or precision == 'int8':
            result = intModule(dataStr0, dataStr1, precision).mult()

        else:
            raise TypeError(f"Unsupported precision type: {precision}")
    else:
        raise TypeError(f"Unsupported calculating type: {mode}")
        
    
    
    deResult = bitStrToNum(result, precision)

    return args.data0, args.data1, mode, result, deResult, precision


if __name__ == "__main__" :
    #print(numToBitstr(3.12, 'fp32'))
    
    num0, num1, mode, result, deResult, precision = main()

    if precision == 'fp64':
        roundUp = '.14e'
    elif precision == 'fp32':
        roundUp = '.6e'
    elif precision == 'fp16':
        roundUp = '.2e'
    elif precision == 'fp8':
        roundUp = '.0e'
    elif precision == 'bf16':
        roundUp = '.1e'
    else:
        roundUp = ''
    
    print(f'Binary Result: {result}')
    print(f'Decimal Result: {format(deResult, roundUp)}')

    if 'int' in precision:
        if mode == 'add':
            trueResult = int(num0)+int(num1)
        elif mode == 'mult':
            trueResult = int(num0)*int(num1)
    elif 'fp' in precision or 'bf' in precision:
        if mode == 'add':
            trueResult = format(float(num0)+float(num1), roundUp)
        elif mode == 'mult':
            trueResult = format(float(num0)*float(num1), roundUp)

    print(f'True Result: {trueResult}')
    if deResult == trueResult:
        print(True)
    else:
        print(False)