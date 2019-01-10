from migen import *
import CRG

"""
Top level application module.
"""
class application_top(Module):
    def __init__(self, platform):
        self.submodules.crg = CRG(platform)
        self.submodules.adc = adc_top()
        self.submodules.tengbe = tengbe_top()
        self.submodules.spectrometer = spectrometer_top()