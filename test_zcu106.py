from migen import *
from migen.build.platforms import zcu106
from litex.soc.cores.gpio import Blinker

# Initialize ZCU106 platform
platform = zcu106.Platform()

# Get GPIO LED 0
led = platform.request("user_led")

# Connect LED to Blinker Module
blinker = Blinker(led)

# Build application
platform.build(blinker, build_dir="test_zcu106")
#platform.create_programmer.flash(0, "test_zcu106/top.bit");
