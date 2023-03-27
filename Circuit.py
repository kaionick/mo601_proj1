from Node import Node

class Circuit:
    def __init__(self, test_dir, circuit_file, stim_file):
        self.circuit_pwd = test_dir;

        with open(f'{test_dir}/{circuit_file}') as f:
            file_lines = f.read().splitlines();
            self.inputs, self.gate_nodes = self.setup_circuit(file_lines);

        with open(f'{test_dir}/{stim_file}') as f:
            file_lines = f.read().splitlines();
            self.stim, self.cycles = self.arrange_stim(file_lines);

        self.stim_packet = 0;

        # Create the output history by adding the inputs and gate nodes to the table
        self.output_hist = list();
        self.output_hist.append([node for node in dict(self.inputs, **self.gate_nodes)]);


    # Setup circuit: create inputs nodes and gate nodes
    def setup_circuit (self, file_list):
        gate_nodes = list();

        nodes_name = list();
        eval_names = list();
        for line in file_list:
            line_split = line.split(' ');
            nodes_name.append(line_split[0].upper());
            eval_names.append([a.upper() for a in line_split[3:]]);
            gate_nodes.append(Node(line_split[0].upper(),
                              [a.upper() for a in line_split[3:]],
                              line_split[2]));

        # Create dictionary: gate nodes
        gate_nodes = dict(zip([k.name for k in gate_nodes], gate_nodes));


        input_nodes = list();
        for i in range(len(eval_names)):
            for node in eval_names[i]:
                if node not in nodes_name:
                    if node not in [input_node.name for input_node in input_nodes]:
                        input_nodes.append(Node(node.upper(),
                                                node.upper(),
                                                'in'));

        # Create dictionary: input nodes
        input_nodes = dict(zip([k.name for k in input_nodes], input_nodes));
                    
        return input_nodes, gate_nodes;


    # Arramge the stimulus: one mult-dim array for the values and one for the time
    def arrange_stim(self, file_lines):
        stim_list = [list(), list()];
        cycle_list = list();

        stim_list_name_tmp = list();
        stim_list_value_tmp = list();
        for line in file_lines:
            line_split = line.split(' ');
            if (line_split[0][0] == '+'):
                cycle_list.append(int(line_split[0][1:]));
                if (stim_list_name_tmp and stim_list_value_tmp):
                    stim_list[0].append(stim_list_name_tmp);
                    stim_list[1].append(stim_list_value_tmp);
                    stim_list_name_tmp = list();
                    stim_list_value_tmp = list();
            else:
                stim_list_name_tmp.append(line_split[0]);
                stim_list_value_tmp.append(int(line_split[2]));

        if (stim_list_name_tmp and stim_list_value_tmp):
            stim_list[0].append(stim_list_name_tmp);
            stim_list[1].append(stim_list_value_tmp);

        ## Append one extra cycle for simulation to allow circuito convergence
        #cycle_list.append(0);

        return stim_list, cycle_list;

    
    # Update the input values
    def update_inputs (self):
        for i in range(len(self.stim[0][self.stim_packet])):
            for inp in self.inputs:
                if (inp == self.stim[0][self.stim_packet][i]):
                    self.inputs[inp].value_hist = self.inputs[inp].value;
                    self.inputs[inp].value = self.stim[1][self.stim_packet][i];


    def search_node_value (self, node_name):
        if node_name in self.inputs:
            return self.inputs[node_name].value;
        else:
            return self.gate_nodes[node_name].value;
                

    def check_node_conv (self, node):
        if (node.value == node.value_hist):
            return True;
        else:
            return False;


    def set_node_value (self, name, value):
        self.gate_nodes[name].value_hist = self.gate_nodes[name].value;
        self.gate_nodes[name].value = value;


    def eval_nodes (self, full_propagation = True, db=0):
        db_print = 0;
        count_stable = 0;
        stable = False;
        if (full_propagation):
            while(not(stable) or count_stable < 26):
                #if (db_print == 0):
                #    print(f'{db_print}: {count_stable}');
                #if (count_stable == 25):
                #    print("Debug brabo");
                #    db_print = 1;
                if (stable):
                    count_stable = count_stable + 1;
                stable = True;
                for node in self.gate_nodes:
                    if (self.gate_nodes[node].op == 'NOT'):
                        if self.gate_nodes[node].inputs[0] in self.inputs:
                            self.gate_nodes[node].value_hist = self.gate_nodes[node].value_hist;
                            self.gate_nodes[node].value = int(not(self.inputs[self.gate_nodes[node].inputs[0]].value));
                        else:
                            self.gate_nodes[node].value_hist = self.gate_nodes[node].value_hist;
                            self.gate_nodes[node].value = int(not(self.gate_nodes[self.gate_nodes[node].inputs[0]].value));
                    else:
                        op0 = int(self.search_node_value(self.gate_nodes[node].inputs[0]));
                        op1 = int(self.search_node_value(self.gate_nodes[node].inputs[1]));
                        if (self.gate_nodes[node].op == 'AND'):
                            self.set_node_value(node, op0 and op1);
                        elif (self.gate_nodes[node].op == 'OR'):
                            self.set_node_value(node, op0 or op1);
                        elif (self.gate_nodes[node].op == 'NAND'):
                            self.set_node_value(node, int(not(op0 and op1)));
                        elif (self.gate_nodes[node].op == 'NOR'):
                            self.set_node_value(node, int(not(op0 or op1)));
                        elif (self.gate_nodes[node].op == 'XOR'):
                            self.set_node_value(node, int(op0 ^ op1));

                    stable = self.check_node_conv(self.gate_nodes[node]);
        else:
            tmp_nodes = {k: 0 for k in self.gate_nodes};
            for node in self.gate_nodes:
                if (self.gate_nodes[node].op == 'NOT'):
                    if self.gate_nodes[node].inputs[0] in self.inputs:
                        tmp_nodes[node] = int(not(self.inputs[self.gate_nodes[node].inputs[0]].value));
                        #self.gate_nodes[node].value_hist = self.gate_nodes[node].value;
                        #self.gate_nodes[node].value = int(not(self.inputs[self.gate_nodes[node].inputs[0]].value));
                    else:
                        tmp_nodes[node] = int(not(self.gate_nodes[self.gate_nodes[node].inputs[0]].value));
                        #self.gate_nodes[node].value_hist = self.gate_nodes[node].value;
                        #self.gate_nodes[node].value = int(not(self.gate_nodes[self.gate_nodes[node].inputs[0]].value));
                else:
                    op0 = int(self.search_node_value(self.gate_nodes[node].inputs[0]));
                    op1 = int(self.search_node_value(self.gate_nodes[node].inputs[1]));
                    if (self.gate_nodes[node].op == 'AND'):
                        tmp_nodes[node] = op0 and op1;
                        #self.set_node_value(node, op0 and op1);
                    elif (self.gate_nodes[node].op == 'OR'):
                        tmp_nodes[node] = op0 or op1;
                        #self.set_node_value(node, op0 or op1);
                    elif (self.gate_nodes[node].op == 'NAND'):
                        tmp_nodes[node] = int(not(op0 and op1)); 
                        #self.set_node_value(node, int(not(op0 and op1)));
                    elif (self.gate_nodes[node].op == 'NOR'):
                        tmp_nodes[node] = int(not(op0 or op1)); 
                        #self.set_node_value(node, int(not(op0 or op1)));
                    elif (self.gate_nodes[node].op == 'XOR'):
                        tmp_nodes[node] = int(op0 ^ op1); 
                        #self.set_node_value(node, int(op0 ^ op1));

            # Passes the tmp_nodes to the node values
            for node in self.gate_nodes:
                self.set_node_value(node, tmp_nodes[node]);

        if (db):
            print(count_stable);
            for node in self.gate_nodes:
                if (self.gate_nodes[node].op != 'NOT'):
                    print(f'{node}: {self.search_node_value(self.gate_nodes[node].inputs[0])} {self.gate_nodes[node].op} {self.search_node_value(self.gate_nodes[node].inputs[1])} = {self.gate_nodes[node].value}');

       
    def time_ctrl (self):
        # Update stimulus: no other action required in zero delay
        self.stim_packet = self.stim_packet + 1;


    def build_output (self):
        tmp = list();
        for i in self.inputs:
            tmp.append(self.inputs[i].value);
        for i in self.gate_nodes:
            tmp.append(self.gate_nodes[i].value);
        
        self.output_hist.append(tmp);


    def sort_output (self):
        sorted_indexes = list(range(self.output_hist[0].__len__()));
        sorted_indexes.sort(key=self.output_hist[0].__getitem__);
        for i in range(0, self.output_hist.__len__()):
            self.output_hist[i] = [self.output_hist[i][k] for k in sorted_indexes];

        # Include table labels (tempo and tempo index)
        self.output_hist[0].insert(0, 'Tempo');
        for i in range(1, self.output_hist.__len__()):
            self.output_hist[i].insert(0,i-1);


    def write_to_file (self, sdf = False):
        if (sdf):
            filename = 'saida1.csv';
        else:
            filename = 'saida0.csv';
        with open(f'{self.circuit_pwd}/{filename}', 'w+') as f:
            for trow in self.output_hist:
                tmp_row = '';
                for tcol_idx in range(trow.__len__()-1):
                    tmp_row = tmp_row + f'{trow[tcol_idx]},';
                tmp_row = tmp_row + f'{trow[-1]}\n';

                f.write(tmp_row);


    def run_zero_delay (self):

        while (self.stim_packet < self.stim[0].__len__()):
            self.update_inputs();
            self.eval_nodes();
            self.time_ctrl();
            self.build_output();
        
        # Last convergence run: it is really necessary?
        self.time_ctrl();
        self.build_output();

        self.sort_output();

        self.write_to_file();

    def check_stable (self):
        stable = True;
        for node in self.gate_nodes:
            if (self.gate_nodes[node].value != self.gate_nodes[node].value_hist):
                stable = False;

        return stable;
            

    def run_sdf (self):

        self.update_inputs();
        self.build_output();
        while(self.stim_packet < self.cycles.__len__()):
            if (self.cycles[self.stim_packet] > 0):
                while(self.cycles[self.stim_packet] > 0):
                    self.eval_nodes(full_propagation = False); # Update functionalty to run one cycle only
                    self.cycles[self.stim_packet] = self.cycles[self.stim_packet] - 1;
                self.time_ctrl();
                self.update_inputs();
                self.build_output();

        while(not(self.check_stable())):
            self.eval_nodes(full_propagation = False, db = 1);
            self.build_output();

        self.sort_output();

        self.write_to_file(sdf=True);

        
    def get_node_list(self, node_dict):
        return [node_dict[k].name for k in node_dict]


    def print_node_names(self, node_list):
        for node in node_list:
            print(node_list[node].name);

    def print_node_values(self, node_list):
        for node in node_list:
            print(f'{node_list[node].name}: {node_list[node].value}');

    def print_out_hist(self):
        for hist in self.output_hist:
            print(hist);

