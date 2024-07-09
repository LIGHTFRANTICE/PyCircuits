from logicGates import LogicGates

def half_adder(a, b):
    """
    Perform half adder operation.
    :param a: First input bit
    :param b: Second input bit
    :return: A tuple (sum, carry)
    """
    sum = LogicGates.xorGate(a, b)  # XOR operation
    carry = LogicGates.andGate(a, b)  # AND operation
    return sum, carry

def full_adder(a, b, carry_in):
    """
    Perform full adder operation.
    :param a: First input bit
    :param b: Second input bit
    :param carry_in: Carry input bit
    :return: A tuple (sum, carry_out)
    """
    sum1, carry1 = half_adder(a, b)
    sum2, carry2 = half_adder(sum1, carry_in)
    carry_out = LogicGates.orGate(carry1, carry2) # OR operation
    return sum2, carry_out

def main():
    print(half_adder('1', '1'))
    print(full_adder('1', '1', '0'))

if __name__ == '__main__':
    main()