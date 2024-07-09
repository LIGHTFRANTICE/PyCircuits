import argparse

from fpModule import fpModule
from multsByPrecisions import FPMult

class TranslateToBinary:
    def __init__(self) -> None:
        pass

    def dataStrToNum(dataStr, precision):
        if 'fp' in precision:
            dataList = dataStr.split('.')
            intPart = dataList[0]
            decimalPart = dataList[1]
           
            if precision == 'fp32':
                pass
            

    def toBinary(dataStr, precision):
        pass
          

def main():

    parser = argparse.ArgumentParser(description='Set precision and calculate mode.')
    
    parser.add_argument('-p', '--precision', choices=['fp32', 'fp16', 'fp8', 'bf16', 'int8', 'int16', 'int32', 'tf32'], help='Choose a precision', required=True)
    parser.add_argument('-c', '--calmode', choices=['add', 'mult'], help='Choose a calculating mode, add or mult.', required=True)
    
    parser.add_argument('dataStr0', help='The first data to be calculated.')
    parser.add_argument('dataStr1', help='The second data to be calculated.')

    args = parser.parse_args()

    #test args
    print(args)

    mode = args.calmode

    precision = args.precision

    dataStr0 = args.dataStr0
    dataStr1 = args.dataStr1

    result = ''

    if precision == 'fp32':
            if mode == "add":
                result = fpModule(dataStr0, dataStr1, precision).fp32Adder
            elif mode == "mult":
                result = FPMult.fp32(dataStr0, dataStr1)
            else:
                raise ValueError(f"Unsupported calculating type: {mode}")
        
    else:
        raise ValueError(f"Unsupported precision type: {precision}")
    
    return result


if __name__ == "__main__" :
    result = main()
    print(result)