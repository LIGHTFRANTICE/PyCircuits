# Set Up

## Environment

### JUST make sure you have installed Python3 and NUMPY

## USAGE

usage: main.py [-h] -p {fp64,fp32,fp16,fp8,bf16,int8,int16,int32} -c {add,mult} data0 data1

Set precision and calculate mode.

positional arguments:
  data0                 The first data to be calculated.
  data1                 The second data to be calculated.

optional arguments:
  -h, --help            show this help message and exit
  -p {fp64,fp32,fp16,fp8,bf16,int8,int16,int32}, --precision {fp64,fp32,fp16,fp8,bf16,int8,int16,int32}
                        Choose a precision
  -c {add,mult}, --calmode {add,mult}
                        Choose a calculating mode, add or mult.

**The Output will be like:**

```terminal

$ python .\main.py -p bf16 -c mult -9.3 2.1235345
Converted -9.3 to Bitstring: 1100000100010100
Converted 2.1235345 to Bitstring: 0100000000000111
Binary Result: 1100000110011100
Decimal Result: -2.0e+01
True Result: -2.0e+01
True

```