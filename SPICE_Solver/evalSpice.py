import numpy as np


def make_list_of_nodes(filename):
    try:
        with open(filename, "r") as file:
            while True:
                line = file.readline()
                if not line:
                    raise ValueError("Malformed circuit file")
                if ".circuit" in line.split():
                    break  # Circuit found
    except FileNotFoundError:
        raise FileNotFoundError('Please give the name of a valid SPICE file as input')

    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())

    start_marker = ".circuit"
    end_marker = ".end"
    collected_lines = []

    collecting = False  # a flag to indicate when to start collecting lines

    for line in lines:
        if line == end_marker:
            collecting = False  # first check if flag is false.
        # If .end is encountered, flag is set to false and collection is stopped.
        if collecting:
            collected_lines.append(line)  # collect the line if the flag is set
        if line == start_marker:
            collecting = True  # set flag to true at .circuit

    list_of_lines = [line.split() for line in collected_lines]  # Splits individual lines into lists.

    node_label = list_of_lines[0][1]   # Extracting the label of nodes in given file to use in final Dictionary.
    if node_label == 'GND':
        node_label = list_of_lines[0][2]

    extracted_list = [[] for i in range(len(list_of_lines))]

    for i in range(len(list_of_lines)):  # Removing comments from every line; if present.
        for j in range(len(list_of_lines[i])):
            if list_of_lines[i][j] == '#':
                break
            extracted_list[i].append(list_of_lines[i][j].strip())

    for line in extracted_list:   # Converting all nodes to numeric values.
        if ".end" in line:
            break
        if len(line) > 1:
            if line[1] == 'GND':
                line[1] = str(0)
            if line[2] == 'GND':
                line[2] = str(0)
            if line[1] != 'GND' and line[2] != 'GND':
                line[1] = line[1][-1]
                line[2] = line[2][-1]
    return extracted_list, node_label


def R_values(line, ind1, ind2, Admittance):
    if ind1 == -1:
        Admittance[ind2][ind2] += 1 / float(line[-1])
    elif ind2 == -1:
        Admittance[ind1][ind1] += 1 / float(line[-1])
    else:
        Admittance[ind1][ind1] += 1 / float(line[-1])
        Admittance[ind2][ind2] += 1 / float(line[-1])
        Admittance[ind2][ind1] += -1 * (1 / float(line[-1]))
        Admittance[ind1][ind2] += -1 * (1 / float(line[-1]))
    return Admittance

def mat_forming(elem_list):
    nodes_list = []
    vol_source_cntr = 0
    vol_source = []   # Collects name of each voltage source and stores it as a list.
    for line in elem_list:
        if ".end" not in line:
            nodes = line[1:3]
            for node in nodes:
                if node not in nodes_list:
                    nodes_list.append(node)  # Unique list of nodes.
            first_word = line[0:1]
            if first_word[0][0] == 'V':
                vol_source.append(first_word[0])
                vol_source_cntr += 1 # Counting no. of voltage sources for matrix declaration purposes.

            if first_word[0][0] != 'V' and first_word[0][0] != 'I' and first_word[0][0] != 'R':
                raise ValueError("Only V, I, R elements are permitted")

    n = len(nodes_list) - 1 # Removing zero / GND node
    l = (n + vol_source_cntr) # Size of matrix
    v = 0   # A sort of counter variable for no. of voltage sources

    Admittance = np.zeros((l, l), float)  # Declaration of matrices initialised with 0.0 .
    b = np.zeros((l, 1), float)

    for line in elem_list:   # Making the matrix.
        if ".end" in line:
            break
        if len(line) > 1:
            ind1 = int(line[1]) - 1
            ind2 = int(line[2]) - 1
            if line[0][0] == 'R':
                if float(line[-1]) > 0.0:
                    Admittance = R_values(line, ind1, ind2, Admittance)
                elif float(line[-1]) == 0.0:
                    line[-1] = 1e-10
                    Admittance = R_values(line, ind1, ind2, Admittance)
                else:
                    raise ValueError('Malformed circuit file')

            if line[0][0] == 'I' and ind1 != -1:
                b[ind1] += -1*float(line[-1])

            if line[0][0] == 'V':
                if v>=vol_source_cntr:
                    continue
                elif ind1 != -1 and ind2 != -1:
                    Admittance[n+v][ind1] = 1
                    Admittance[n+v][ind2] = -1
                    Admittance[ind1][n+v] = 1
                    Admittance[ind2][n+v] = -1
                    b[n+v] += float(line[-1])
                    v+=1
                elif ind1 == -1:
                    Admittance[n+v][ind2] = -1
                    Admittance[ind2][n+v] = -1
                    b[n+v] += float(line[-1])
                    v+=1
                elif ind2 == -1:
                    Admittance[n+v][ind1] = 1
                    Admittance[ind1][n+v] = 1
                    b[n+v] += float(line[-1])
                    v+=1
    return Admittance, b, n, vol_source_cntr, vol_source
def evalSpice(filename):
    nodes, node_label = make_list_of_nodes(filename)
    m, b, n, v, v_label = mat_forming(nodes)

    try:
        x = np.linalg.solve(m, b)
    except ValueError:
        raise ValueError('Circuit error: no solution')

    Node_V = {}
    node_label = node_label[:-1]
    for i in range(1,n+1):
        j = str(i)
        Node_V[node_label+j] = x[i-1][0]
    Node_V['GND'] = 0.0

    Currents_In_V = {}
    for i in range(v):
        Currents_In_V[v_label[i]] = x[n+i][0]

    return Node_V, Currents_In_V
