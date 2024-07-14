import numpy as np
import struct

def numToBitstr(num, precision):
    if precision == 'fp64':
        # Convert the float to a numpy float64
        fp = np.float64(num)
        # View the float32 as an unsigned 64-bit integer
        int_rep = fp.view(np.uint64)
        # Convert the integer to a 64-bit binary string
        bitStr = format(int_rep, '064b')

    elif precision == 'fp32':
        fp = np.float32(num)
        int_rep = fp.view(np.uint32)
        bitStr = format(int_rep, '032b')

    elif precision == 'fp16':
        fp = np.float16(num)
        int_rep = fp.view(np.uint16)
        bitStr = format(int_rep, '016b')

    elif precision == 'fp8':
        num = float(num)
        if num == 0:
            return '00000000'
        
        sign = 0 if num > 0 else 1
        num = abs(num)
        
        exponent = int(np.floor(np.log2(num)))
        significand = num / (2**exponent) - 1
        
        exponent += 7
        
        if exponent <= 0:
            # Handle subnormal numbers
            exponent = 0
            significand = num / 2**(-6)
        elif exponent >= 15:
            # Handle overflow
            exponent = 15
            significand = 0
        
        exponent_bits = format(exponent, '04b')
        significand_bits = format(int(significand * (2**3)), '03b')
        
        bitStr = f'{sign}{exponent_bits}{significand_bits}'
    
    elif precision == 'bf16':
        # Convert the string to a float
        number = float(num)
        
        # Pack the float as a 32-bit float, then unpack as an integer
        packed = struct.pack('>f', number)
        intRepr = struct.unpack('>I', packed)[0]
        
        # Extract the sign bit, exponent bits, and significand bits for BF16
        sign = (intRepr >> 31) & 0x1
        exponent = (intRepr >> 23) & 0xFF
        significand = (intRepr >> 16) & 0x7F
        
        # Combine the sign, exponent, and significand to form the BF16 bit string
        bf16Int = (sign << 15) | (exponent << 7) | significand
        bitStr = format(bf16Int, '016b')

    elif precision == 'int32':
        # Convert the input string to an integer
        num = int(num)
        
        # Check if the number is within the range of a signed 32-bit integer
        if num < -2**31 or num > 2**31 - 1:
            raise ValueError("The number is out of range for a signed 32-bit integer")
        
        # Convert the integer to a 32-bit binary string
        if num >= 0:
            bitStr = format(num, '032b')
        else:
            # Handle negative numbers using two's complement
            bitStr = format((1 << 32) + num, '032b')

    elif precision == 'int16':
        num = int(num)
        if num < -2**15 or num > 2**15 - 1:
            raise ValueError("The number is out of range for a signed 16-bit integer")

        if num >= 0:
            bitStr = format(num, '016b')
        else:
            bitStr = format((1 << 16) + num, '016b')

    elif precision == 'int8':
        num = int(num)
        if num < -2**7 or num > 2**7 - 1:
            raise ValueError("The number is out of range for a signed 8-bit integer")

        if num >= 0:
            bitStr = format(num, '08b')
        else:
            bitStr = format((1 << 8) + num, '08b')

    print(f'Converted {num} to Bitstring: {bitStr}')
    return bitStr
         
def bitStrToNum(bitStr, precision):
    if len(bitStr) < 8:
        raise ValueError("The bit string must be over 8 bits")

    if 'fp' in precision or 'bf' in precision:
        if precision == 'fp64':
            # Extract the parts of the bit string
            sign = int(bitStr[0], 2)
            exponent = int(bitStr[1:12], 2)
            significand = bitStr[12:]
            # Calculate the actual exponent value
            if exponent == 0:
                # Subnormal numbers
                exponentValue = -1022
            else:
                # Normalized numbers
                exponentValue = exponent - 1023
        
        elif precision == 'fp32':
            # Extract the parts of the bit string
            sign = int(bitStr[0], 2)
            exponent = int(bitStr[1:9], 2)
            significand = bitStr[9:]
            # Calculate the actual exponent value
            if exponent == 0:
                # Subnormal numbers
                exponentValue = -126
            else:
                # Normalized numbers
                exponentValue = exponent - 127

        elif precision == 'fp16':
            sign = int(bitStr[0], 2)
            exponent = int(bitStr[1:6], 2)
            significand = bitStr[6:]
            if exponent == 0:
                # Subnormal numbers
                exponentValue = -14
            else:
                # Normalized numbers
                exponentValue = exponent - 15

        elif precision == 'fp8':
            # Extract the parts of the bit string
            sign = int(bitStr[0], 2)
            exponent = int(bitStr[1:5], 2)
            significand = bitStr[5:]
            if exponent == 0:
                # Subnormal numbers
                exponentValue = -6
            else:
                # Normalized numbers
                exponentValue = exponent - 7

        elif precision == 'bf16':
            # Extract the parts of the bit string
            sign = int(bitStr[0], 2)
            exponent = int(bitStr[1:9], 2)
            significand = bitStr[9:]
            if exponent == 0:
                # Subnormal numbers
                exponentValue = -126
            else:
                # Normalized numbers
                exponentValue = exponent - 127

        # Calculate the actual significand value
        significandValue = 1.0 if exponent != 0 else 0.0
        for i in range(len(significand)):
            significandValue += int(significand[i]) * 2**(-(i + 1))

        # Combine to get the final float value
        result = (-1)**sign * significandValue * 2**exponentValue
        return result

    elif precision == 'int32' or precision == 'int16' or precision == 'int8':
            # Check if the number is negative
        if bitStr[0] == '1':
            # Compute the two's complement
            invertedBits = ''.join('1' if bit == '0' else '0' for bit in bitStr)
            intValue = int(invertedBits, 2) + 1
            intValue = -intValue
        else:
            # Positive number, convert directly
            intValue = int(bitStr, 2)

        return intValue

    else:
        raise TypeError(f"{precision} is not supported to be converted to a number")

    