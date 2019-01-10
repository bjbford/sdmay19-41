from migen import *

"""
ZCU106 Clock and Reset Generator
"""
class CRG(Module):
    def __init__(self, platform):
        self.clock_domains.cd_sys = ClockDomain()
        self.clock_domains.cd_sys4x = ClockDomain(reset_less=True)
        self.clock_domains.cd_clk200 = ClockDomain()
        self.clock_domains.cd_ic = ClockDomain()

        clk125 = platform.request("clk125")
        clk125_ibufds = Signal()
        clk125_buffered = Signal()
        pll_locked = Signal()
        pll_fb = Signal()
        pll_sys4x = Signal()
        pll_clk200 = Signal()
        self.specials += [
            Instance("IBUFDS", i_I=clk125.p, i_IB=clk125.n, o_O=clk125_ibufds),
            Instance("BUFG", i_I=clk125_ibufds, o_O=clk125_buffered),
            Instance("PLLE2_BASE", name="crg_main_mmcm",
                i_RST=platform.request("cpu_reset"),
                p_STARTUP_WAIT="FALSE", o_LOCKED=pll_locked,

                # VCO @ 1GHz
                p_REF_JITTER1=0.01, p_CLKIN1_PERIOD=8.0,
                p_CLKFBOUT_MULT=8, p_DIVCLK_DIVIDE=1,
                i_CLKIN1=clk125_buffered, i_CLKFBIN=pll_fb, o_CLKFBOUT=pll_fb,

                # 500MHz
                p_CLKOUT0_DIVIDE=2, p_CLKOUT0_PHASE=0.0, o_CLKOUT0=pll_sys4x,

                # 200MHz
                p_CLKOUT1_DIVIDE=5, p_CLKOUT1_PHASE=0.0, o_CLKOUT1=pll_clk200,
            ),
            Instance("BUFGCE_DIV", name="main_bufgce_div",
                p_BUFGCE_DIVIDE=4,
                i_CE=1, i_I=pll_sys4x, o_O=self.cd_sys.clk),
            Instance("BUFGCE", name="main_bufgce",
                i_CE=1, i_I=pll_sys4x, o_O=self.cd_sys4x.clk),
            Instance("BUFG", i_I=pll_clk200, o_O=self.cd_clk200.clk),
            AsyncResetSynchronizer(self.cd_clk200, ~pll_locked),
        ]

        ic_reset_counter = Signal(max=64, reset=63)
        ic_reset = Signal(reset=1)
        self.sync.clk200 += \
            If(ic_reset_counter != 0,
                ic_reset_counter.eq(ic_reset_counter - 1)
            ).Else(
                ic_reset.eq(0)
            )
        ic_rdy = Signal()
        ic_rdy_counter = Signal(max=64, reset=63)
        self.cd_sys.rst.reset = 1
        self.comb += self.cd_ic.clk.eq(self.cd_sys.clk)
        self.sync.ic += [
            If(ic_rdy,
                If(ic_rdy_counter != 0,
                    ic_rdy_counter.eq(ic_rdy_counter - 1)
                ).Else(
                    self.cd_sys.rst.eq(0)
                )
            )
        ]
        self.specials += [
            Instance("IDELAYCTRL", p_SIM_DEVICE="ULTRASCALE",
                     i_REFCLK=ClockSignal("clk200"), i_RST=ic_reset,
                     o_RDY=ic_rdy),
            AsyncResetSynchronizer(self.cd_ic, ic_reset)
        ]