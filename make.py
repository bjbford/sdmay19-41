from migen import *
from migen.build.platforms import zcu106
import application_top

if __name__ == "__main__":
    platform = zcu106.Platform()
    apptop = application_top(platform)

    # fil = open("test/csrmap.py", "w")
    # py_csrconstants(redpid.pid.csrbanks.constants, fil)
    # csr = get_csrmap(redpid.pid.csrbanks.banks)
    # py_csrmap(csr, fil)
    # fil.write("states = {}\n".format(repr(redpid.pid.state_names)))
    # fil.write("signals = {}\n".format(repr(redpid.pid.signal_names)))
    # fil.close()

    platform.add_source_dir("verilog")
    platform.build(apptop)