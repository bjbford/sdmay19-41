create_project -force -name top -part xczu28dr-ffvg1517-2-e
set_property XPM_LIBRARIES {XPM_CDC XPM_MEMORY} [current_project]
add_files {top.v}
set_property library work [get_files {top.v}]
read_xdc top.xdc
synth_design -top top -part xczu28dr-ffvg1517-2-e
report_timing_summary -file top_timing_synth.rpt
report_utilization -hierarchical -file top_utilization_hierarchical_synth.rpt
report_utilization -file top_utilization_synth.rpt
opt_design
place_design
report_utilization -hierarchical -file top_utilization_hierarchical_place.rpt
report_utilization -file top_utilization_place.rpt
report_io -file top_io.rpt
report_control_sets -verbose -file top_control_sets.rpt
report_clock_utilization -file top_clock_utilization.rpt
route_design
phys_opt_design
report_timing_summary -no_header -no_detailed_paths
write_checkpoint -force top_route.dcp
report_route_status -file top_route_status.rpt
report_drc -file top_drc.rpt
report_timing_summary -datasheet -max_paths 10 -file top_timing.rpt
report_power -file top_power.rpt
write_bitstream -force top.bit 
quit