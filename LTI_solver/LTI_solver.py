import component_classes
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import math

ambient_temperature = 25 #celcius, 25 is the room temperature

max_time_step = 5e-3 #seconds
min_time_step = 1e-9 #seconds
time_step_multiplier = 1.1
time_step_now = min_time_step #seconds
simulation_end_time = 5 #seconds
sample_record_interval = [4.5,5]

MAX_RESISTOR_TEMPERATURE_CHANGE = 25 #celcius
MAX_CAPACITOR_VOLTAGE_CHANGE = 0.010 #volts
MAX_INDUCTOR_CURRENT_CHANGE = 0.05 #amperes

interested_unknowns = {
    "node_voltage": {
        "node_names":["V_1"], #for node x, add "V_x"
    },
   "inductor_current": {
        "inductor_names":["L1"], #for inductor x, add "L_x"
    },
   "capacitor_voltage": {
        "capacitor_names":[""], #for capacitor x, add "C_x"
   },
   "resistor_temperature": {
        "resistor_names":["R1"], #for resistor x, add "R_x"
   } 
   
}

#=============================DEFINE THE CIRCUIT==============================
ground_node = 0
components = []

# DEFINE VOLTAGE SOURCES 
V1_dict = {
    "dc_offset":0,
    "amplitude":10,
    "frequency":25,
    "phase_shift_angle":225
}
V1 = component_classes.voltageSourceModel(name = "V1", node_p = 1, node_n = 0, type = "sine", type_dict = V1_dict)
components.append(V1)

# V2 = component_classes.voltageSourceModel(name = "V2", node_p = 2, node_n = 1, type = "dc", type_dict = {"dc_voltage": 5})
# components.append(V2)

# DEFINE CURRENT SOURCES
# I1 = component_classes.currentSourceModel(name = "I1", node_p = 3, node_n = 0, type = "dc", type_dict = {"dc_current": -1})
# components.append(I1)

# DEFINE RESISTORS
#if heat_transfer_coefficient is set to 2.5e-3, quarter-watt resistor reaches 125 celcius at 25 celcius ambient temperature
# X watt resistor -> heat_transfer_coefficient = X*e-2

resistor_25_mohm_v1 = lambda resistor_tempetature: 0.025+max(0.00*(resistor_tempetature-25),0)
resistor_50_mohm_v1 = lambda resistor_tempetature: 0.05+max(0.00*(resistor_tempetature-25),0)
resistor_1_ohm_v1 = lambda resistor_tempetature: 1+max(0.00*(resistor_tempetature-25),0)
resistor_3_ohm_v1 = lambda resistor_tempetature: 3+max(0.00*(resistor_tempetature-25),0)
resistor_5_ohm_v1 = lambda resistor_tempetature: 5+max(0.05*(resistor_tempetature-25),0)
resistor_10_ohm_v1 = lambda resistor_tempetature: 10+max(0.05*(resistor_tempetature-25),0)

R1 = component_classes.resistorModel(name = "R1", node_p = 1, node_n = 2, resistance_function = resistor_50_mohm_v1, heat_capacity = 0.1, heat_transfer_coefficient = 10e-2, resistor_temperature = 25)
components.append(R1)


# DEFINE INDUCTORS
inductor_10mH_v1 = lambda inductor_current: 1e-2
inductor_10mH_saturation_v1 = lambda inductor_current: 0.001 + 0.02*(math.pow(math.e, -(abs(inductor_current/2))))

L1 = component_classes.inductorModel(name = "L1", node_p = 2, node_n = 0, inductance_function = inductor_10mH_saturation_v1, initial_current = 0)
components.append(L1)

# DEFINE CAPCACITORS
capacitor_10uF_v1 = lambda capacitor_voltage: 10e-6

# C1 = component_classes.capacitorModel(name = "C1", node_p = 4, node_n = 0, capacitance_function = capacitor_10uF_v1, initial_voltage = 0)
# components.append(C1)

#define unknowns
unknowns = {}
unknown_index_counter = 0
all_nodes = []
for component in components:
  all_nodes.append(component.NODE_P)
  all_nodes.append(component.NODE_N)
all_nodes = set(all_nodes)
all_nodes = list(all_nodes)
for node in all_nodes:
    unknowns[f"V_{node}"] = unknown_index_counter
    unknown_index_counter += 1

for component in components:
    if component.get_component_category() == "VOLTAGE-SOURCE" or component.get_component_category() == "CAPACITOR":
        unknowns[f"I_{component.NAME}"] = unknown_index_counter
        unknown_index_counter += 1

number_of_unknowns = len(unknowns)


#=========================CHECK IF THE CIRCUIT IS VALID=============================     
# inductor and current source related checks are not implemented yet
 
#check if the component names are unique
for component_index, component in enumerate(components):
  for other_component_index, other_component in enumerate(components):
    if component.NAME == other_component.NAME and component_index != other_component_index:
      raise Exception(f"Component names {component.NAME} are not unique.")    
#check if voltage sources are short circuited
for component_index, component in enumerate(components):
  if component.get_component_category() == "VOLTAGE-SOURCE":
    if component.NODE_P == component.NODE_N:
      raise Exception(f"Voltage source {component.NAME} is short circuited.")
#check if two voltage sources are connected in parallel
for component_index, component in enumerate(components):
  if component.get_component_category() == "VOLTAGE-SOURCE":
    for other_component_index, other_component in enumerate(components):
      if other_component.get_component_category() == "VOLTAGE-SOURCE":
        nodes = set([component.NODE_P, component.NODE_N])
        other_nodes = set([other_component.NODE_P, other_component.NODE_N])

        if nodes == other_nodes and component_index != other_component_index:
          raise Exception(f"Voltage sources {component.NAME} and {other_component.NAME} are connected in parallel.")        
#check if any node is left floating (i.e it should be connected to atleast two components)
for node in all_nodes:
    is_connected = False
    connection_count = 0
    for component in components:
        if component.NODE_P == node or component.NODE_N == node:
            connection_count += 1
        if connection_count >= 2:
            is_connected = True
            break
    if is_connected == False:
        raise Exception(f"Node {node} is left floating.")
    

#=========================START SIMULATION=============================   

samples = [] #list of lists, each list contains the values of the interested unknowns at a certain time
time_now = 0 #seconds
last_percent_printed = 0
while time_now < simulation_end_time:
    if(time_now/simulation_end_time*100 - last_percent_printed > 1):
        print(f"Simulation progress: {time_now/simulation_end_time*100:.1f}%  Time step (us): {time_step_now*(1e6):.0f}")
        last_percent_printed = time_now/simulation_end_time*100

    #append ground node information 
    info_matrix = np.zeros((1, number_of_unknowns))
    info_matrix[0,unknowns[f"V_{ground_node}"]] = 1
    result_vector = np.zeros((1,1))

    #append node voltage constraints due to voltage sources and capacitors
    for component in components:
        if component.get_component_category() == "VOLTAGE-SOURCE" or component.get_component_category() == "CAPACITOR":   
            positive_node = component.NODE_P
            negative_node = component.NODE_N
            voltage_difference = component.get_voltage(t=time_now) if component.get_component_category() == "VOLTAGE-SOURCE" else component.get_voltage()
            unknown_p_index = unknowns[f"V_{positive_node}"]
            unknown_n_index = unknowns[f"V_{negative_node}"]

            A = np.zeros((1, number_of_unknowns))
            B = np.zeros((1,1))

            A[0, unknown_p_index] = 1
            A[0, unknown_n_index] = -1
            B[0,0] = voltage_difference

            info_matrix = np.append(info_matrix, A, axis=0)
            result_vector = np.append(result_vector, B, axis=0)

    #append node equations (KCL: leaving currents is equal to zero)
    for node in all_nodes:
        node_voltage_index = unknowns[f"V_{node}"]
      
        A = np.zeros((1, number_of_unknowns))
        B = np.zeros((1,1))
        for component in components:     

            component_p = component.NODE_P
            component_n = component.NODE_N
            component_category = component.get_component_category()

            if component_p != node and component_n != node:
               continue

            matching_node = component_p if component_p == node else component_n
            matching_node_index = unknowns[f"V_{matching_node}"]
            not_matching_node_index = unknowns[f"V_{component_p if component_p != node else component_n}"]

            if (component_category == "RESISTOR"):
                resistance = component.get_resistance()
                A[0, node_voltage_index] += 1/resistance
                A[0, not_matching_node_index] = -1/resistance
            elif(component_category == "VOLTAGE-SOURCE"):
                matching_voltage_source_current_index = unknowns[f"I_{component.NAME}"]
                if matching_node == component_p: #positive terminal is connected to the node, current is leaving
                    A[0, matching_voltage_source_current_index] = 1
                else: #negative terminal is connected to the node, current is entering
                    A[0, matching_voltage_source_current_index] = -1
            elif(component_category == "CURRENT-SOURCE"):
                current = component.get_current(t=time_now)
                if matching_node == component_p: #positive terminal is connected to the node, current is leaving
                    B[0,0] += -current
                else:
                    B[0,0] += current
            elif(component_category == "CAPACITOR"):
                matching_capacitor_current_index = unknowns[f"I_{component.NAME}"]
                if matching_node == component_p: #positive terminal is connected to the node, current is leaving
                    A[0, matching_capacitor_current_index] = 1
                else: #negative terminal is connected to the node, current is entering
                    A[0, matching_capacitor_current_index] = -1
            elif(component_category == "INDUCTOR"):
                current = component.get_current()
                if matching_node == component_p: #positive terminal is connected to the node, current is leaving
                    B[0,0] += -current
                else:
                    B[0,0] += current
                   
                   
        info_matrix = np.append(info_matrix, A, axis=0)
        result_vector = np.append(result_vector, B, axis=0)
    
    #solve the system of equations (approximated by least squares method)
    approximated_solution, residuals, rank, s = np.linalg.lstsq(info_matrix, result_vector, rcond=None)
   
    #=====================================================================================================
    # #prints the solution to the terminal
    # for solution_index, solution in enumerate(approximated_solution):       
    #     val = solution[0]
    #     for unknown, unknown_index in unknowns.items():
    #         if solution_index == unknown_index:
    #             print(unknown, val)
    #=====================================================================================================

    #update component states
    should_increase_time_step = True
    for component in components:
        component_p = component.NODE_P
        component_n = component.NODE_N

        if component.get_component_category() == "RESISTOR":
            #TODO: check if the temperature change is too high, if so decrease the time step
            positive_node_voltage = approximated_solution[unknowns[f"V_{component_p}"]][0]
            negative_node_voltage = approximated_solution[unknowns[f"V_{component_n}"]][0]
            voltage_difference = positive_node_voltage - negative_node_voltage
            b, del_T = component.update_resistor_temperature(voltage_difference, ambient_temperature, time_step_now, MAX_RESISTOR_TEMPERATURE_CHANGE)
            should_increase_time_step = should_increase_time_step and b
            #print(f"Resistor temperature: {component.get_temperature()}, temperature change: {del_T}")

        elif component.get_component_category() == "CAPACITOR":
            capacitor_current = approximated_solution[unknowns[f"I_{component.NAME}"]][0]
            b, del_V = component.update_voltage(capacitor_current, time_step_now, MAX_CAPACITOR_VOLTAGE_CHANGE)
            should_increase_time_step = should_increase_time_step and b
            #print(f"Capacitor voltage: {component.get_voltage()}, voltage change: {del_V}")
            
        elif component.get_component_category() == "INDUCTOR":
            positive_node_voltage = approximated_solution[unknowns[f"V_{component_p}"]][0]
            negative_node_voltage = approximated_solution[unknowns[f"V_{component_n}"]][0]
            voltage_difference = positive_node_voltage - negative_node_voltage
            b, del_I= component.update_current(voltage_difference, time_step_now, MAX_INDUCTOR_CURRENT_CHANGE)
            should_increase_time_step = should_increase_time_step and b    
            #print(f"Inductor current: {component.get_current()}, del_I: {del_I}")

    #update states if the state changes are small enough, otherwise decrease the time step   
    if should_increase_time_step:
        time_step_now = min(max_time_step, time_step_now*time_step_multiplier)
    else:
        time_step_now = max(min_time_step, time_step_now/time_step_multiplier)

    time_now = time_now + time_step_now

    #append the values of the interested unknowns to the samples list
    if(time_now >= sample_record_interval[0] and time_now <= sample_record_interval[1]):
        sample_now = {"time": time_now}
        for node_name in interested_unknowns["node_voltage"]["node_names"]:  
            sample_now[node_name] = approximated_solution[unknowns[node_name]][0]          
        for capacitor_name in interested_unknowns["capacitor_voltage"]["capacitor_names"]:
            for component in components:
                if component.NAME == capacitor_name:
                    sample_now[f"V_{capacitor_name}"] = component.get_voltage()
                    break
        for inductor_name in interested_unknowns["inductor_current"]["inductor_names"]:
            for component in components:
                if component.NAME == inductor_name:
                    sample_now[f"I_{inductor_name}"] = component.get_current()
                    break
        for resistor_name in interested_unknowns["resistor_temperature"]["resistor_names"]:
            for component in components:
                if component.NAME == resistor_name:
                    sample_now[f"T_{resistor_name}"] = component.get_temperature()
                    break
        
        samples.append(sample_now)

# Extract the variable names (keys) from the first dictionary, excluding 'time'
variable_names = [key for key in samples[0].keys() if key != 'time']
# Create a dictionary to store the values for each variable
data = {var_name: [] for var_name in variable_names}
times = []

# Extract the data from the dictionaries
for sample in samples:
    times.append(sample['time'])
    for var_name in variable_names:
        data[var_name].append(sample[var_name])

# Create a plot for each variable
num_vars = len(variable_names)
plt.figure(figsize=(10, num_vars * 3))

for i, var_name in enumerate(variable_names, 1):
    plt.subplot(num_vars, 1, i)
    plt.plot(times, data[var_name], label=var_name)
    # Set y-axis scale to 1
    y_max = max(data[var_name])+5
    y_min = min(data[var_name])-5
    plt.ylim(y_min, y_max)

    plt.xlabel('Time')
    plt.ylabel(var_name)
    plt.title(f'{var_name} vs Time')
    plt.grid(True)
    plt.legend()

# Adjust layout and show the plots

plt.tight_layout()
plt.show()

