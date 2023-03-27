# ----------------------------------------------------------
# Import files
# ----------------------------------------------------------
# General Python imports
import os
import sys
#import argparser

# Project imports
from Circuit import Circuit

# ----------------------------------------------------------
# Command line arguments setup
# ----------------------------------------------------------
# Directory setup
exe_path = os.getcwd();
test_path = exe_path + '/test/test0';

circuit_file = "circuito.hdl";
stim_file = "estimulos.txt";

# ----------------------------
# Zero delay circuit
# ----------------------------

zdc = Circuit (test_path, circuit_file, stim_file);

# Evaluate the circuit in zero delay
zdc.run_zero_delay();

# Print the output
zdc.print_out_hist();
print("");

# ----------------------------
# Zero delay circuit
# ----------------------------

# Evalu
sdfc = Circuit (test_path, circuit_file, stim_file);

# Evaluate the circuit using the delay of the cells's
sdfc.run_sdf();

sdfc.print_out_hist();
