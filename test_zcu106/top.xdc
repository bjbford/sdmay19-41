 ## user_led:0
set_property LOC AL11 [get_ports user_led]
set_property IOSTANDARD LVCMOS12 [get_ports user_led]
 ## clk125:0.p
set_property LOC H9 [get_ports clk125_p]
set_property IOSTANDARD LVDS [get_ports clk125_p]
 ## clk125:0.n
set_property LOC G9 [get_ports clk125_n]
set_property IOSTANDARD LVDS [get_ports clk125_n]

create_clock -name clk125_p -period 8.0 [get_nets clk125_p]

set_false_path -quiet -to [get_nets -filter {mr_ff == TRUE}]

set_false_path -quiet -to [get_pins -filter {REF_PIN_NAME == PRE} -of [get_cells -filter {ars_ff1 == TRUE || ars_ff2 == TRUE}]]

set_max_delay 2 -quiet -from [get_pins -filter {REF_PIN_NAME == Q} -of [get_cells -filter {ars_ff1 == TRUE}]] -to [get_pins -filter {REF_PIN_NAME == D} -of [get_cells -filter {ars_ff2 == TRUE}]]