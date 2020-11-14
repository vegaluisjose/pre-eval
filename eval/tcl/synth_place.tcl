set xdc_file [lindex $argv 0]
set dir [lindex $argv 1]
set filename [lindex $argv 2]
set name [lindex $argv 3]

set part_name "xczu3eg-sbva484-1-e"

set verilog_file "${dir}/${filename}.v"
set netlist_file "${dir}/${filename}_netlist.v"

read_verilog -sv $verilog_file
read_xdc -mode out_of_context $xdc_file
synth_design -mode "out_of_context" -flatten_hierarchy "rebuilt" -top $name -part $part_name
opt_design
place_design -directive Default
write_verilog -file $netlist_file
