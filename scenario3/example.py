from ctypes import cdll, c_int, c_ubyte, POINTER, c_char_p, pointer, byref
from numba import cfunc, types, carray, jit
import numpy as np
import math


@jit
def create_gaussian_kernel(kernel):
    # set standard deviation to 1.0
    sigma = 1.0
    r = 0.0
    s = 2.0 * sigma * sigma
    x = y = i = j = 0
    # sum is for normalization
    sum_ = 0.0
    # generate 5x5 kernel
    for x in range(-2, 3):
        for y in range(-2, 3):
            r = math.sqrt(x*x + y*y)
            kernel[x + 2][y + 2] = (math.exp(-(r*r)/s))/(math.pi * s)
            sum_ += kernel[x + 2][y + 2]
    # normalize the Kernel
    for i in range(5):
        for j in range(5):
            kernel[i][j] /= sum_


gKernel = np.zeros((5, 5))
create_gaussian_kernel(gKernel)

c_sig = types.void(types.CPointer(types.uchar),
                    types.CPointer(types.uchar),
                    types.intc, types.intc, types.intc, types.intc)


@cfunc(c_sig)
def gaussian_filter(in_, out, y, x, width, height):
    in_array = carray(in_, (height, width, 3))
    out_array = carray(out, (height, width, 3))
    for k in range(3):
        sum_ = 0.
        for p in range(-2, 3):
            for q in range(-2, 3):
                sum_ += gKernel[p+2, q+2] * in_array[y+p,x+q,k]
        out_array[y, x, k] = sum_

ifilter = cdll.LoadLibrary("libifilter.dylib")

# Create integers to pass in to C function
int_p = POINTER(c_int)
i1 = c_int()
i2 = c_int()
i3 = c_int()
widthp = pointer(i1)
heightp = pointer(i2)
bpp = pointer(i3)

# Get the read_png function from the shared library and set arg/result types
read_png = ifilter.read_png
read_png.restype = POINTER(c_ubyte)
read_png.argtypes = [c_char_p, int_p, int_p, int_p]

# Read the file
pic = read_png(b"landscape1.png", widthp, heightp, bpp)

# Create array type to hold raw memory for filtered image
array_type = c_ubyte * heightp[0] * widthp[0] * 3

# Create a new empty array
arg2 = array_type()

# pass the numba-jitted "cfunc" to the C function
ifilter.apply_any_filter(pic, byref(arg2), widthp[0], heightp[0],
                         gaussian_filter.ctypes)
# Write the resulting file
#ifilter.write_png(byref(arg2), 848, 500)
ifilter.write_png(b"landscape_out_python.png", byref(arg2), widthp[0],
                  heightp[0])
