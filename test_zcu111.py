from migen import *
from migen.build.platforms import zcu111
from litex.soc.cores.gpio import Blinker


if __name__ == "__main__":
	# Creates an instance of the zcu111 platform.
	platform = zcu111.Platform()
	# Fetches an unused GPIO LED onboard the zcu111.
	led = platform.request("user_led")
	# Creates a litex LED blinker module that ties to the passed
	# in led object.
	led_blinker = Blinker(led)
	# Builds the migen project and places into build_dir.
	platform.build(led_blinker, build_dir="test_zcu111")
	# Flashes newly created bitstream to the ZCU111 board.
	platform.create_programmer().flash(0, "test_zcu111/top.bit")
