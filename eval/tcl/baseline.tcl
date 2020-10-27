set xdc_file [lindex $argv 0]
set dir [lindex $argv 1]
set filename [lindex $argv 2]
set name [lindex $argv 3]

set part_name "xczu3eg-sbva484-1-e"

set verilog_file "${dir}/${filename}.v"
set netlist_file "${dir}/${filename}_netlist.v"
set timing_file "${dir}/${filename}_timing.txt"
set timing_summary_file "${dir}/${filename}_timing_sum.txt"
set utilization_file "${dir}/${filename}_utilization.txt"

read_verilog -sv $verilog_file
read_xdc -mode out_of_context $xdc_file
synth_design -mode "out_of_context" -flatten_hierarchy "rebuilt" -top $name -part $part_name
opt_design
place_design -directive Default
route_design -directive Default
write_verilog -file $netlist_file
report_timing -file $timing_file
report_timing_summary -file $timing_summary_file
report_utilization -file $utilization_file
