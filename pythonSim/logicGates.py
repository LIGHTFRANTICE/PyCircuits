class LogicGates:

    def __init__(self) -> None:
        pass

    def andGate(bitStr1, bitStr2):
        if (bitStr1=='1' and bitStr2=='1'):
            return '1'
        else:
            return '0'
        
    def nandGate(bitStr1, bitStr2):
        if (bitStr1=='1' and bitStr2=='1'):
            return '0'
        else:
            return '1'

    def notGate(bitStr):
        if (bitStr=='1'):
            return '0'
        else:
            return '1'

    def xorGate(bitStr1, bitStr2):
        if ((bitStr1=='0' and bitStr2=='0') or (bitStr1=='1' and bitStr2=='1')):
            return '0'
        else:
            return '1'
    
    def orGate(bitStr1, bitStr2):
        if (bitStr1=='1' or bitStr2=='1'):
            return '1'
        else:
            return '0'

def main():
    print(LogicGates.orGate('1', '1'))

if __name__ == '__main__':
    main()