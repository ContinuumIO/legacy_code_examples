from numpy.distutils.core import setup, Extension

wrapper = Extension('fwrapper', sources=['dft.f90'], libraries=['my_module'])

setup(
    name='fortranwrap',
    version='0.4',
    libraries = [('my_module', dict(sources=['dft.f90']))],
    ext_modules = [wrapper]
)

