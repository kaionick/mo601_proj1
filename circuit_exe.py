# ----------------------------------------------------------
# Import files
# ----------------------------------------------------------
# General Python imports
import os
import sys
import argparse

# Project imports
from Circuit import Circuit

# ----------------------------------------------------------
# Command line arguments setup
# ----------------------------------------------------------

parser = argparse.ArgumentParser(prog='Super Basic HDL Simulator (SBHDL_SIM)',
                                 description='It simulates super basics HDL \
                                              circuits using a dedicated VCD \
                                              stimulus file. ');

parser.add_argument('-t', '--test_name', action = 'store', 
                    default = 'all', required = False);

args = parser.parse_args();

# ----------------------------------------------------------
# Simulation run
# ----------------------------------------------------------
exe_path = os.getcwd();

circuit_file = "circuito.hdl";
stim_file = "estimulos.txt";

if (args.test_name == all):
    print("All execution is not implemented yet, run test by test, please");
else:
    print(f'# ----------------------------------------------');
    print (f'# Running circuit from test/{args.test_name}');
    print(f'# ----------------------------------------------');
    # Directory setup
    test_path = exe_path + f'/test/{args.test_name}';
    
    # ----------------------------
    # Zero delay circuit
    # ----------------------------
    
    zdc = Circuit (test_path, circuit_file, stim_file);
    
    # Evaluate the circuit in zero delay
    zdc.run_zero_delay();

    print (f'Finished Zero Delay: test/{args.test_name}');
    
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

    print (f'Finished SDF: test/{args.test_name}');
    print("");
    
    sdfc.print_out_hist();
