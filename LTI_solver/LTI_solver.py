import component_classes
import numpy as np

ambient_temperature = 25 #celcius, 25 is the room temperature

# =============================DEFINE THE CIRCUIT==============================
ground_node = 0
components = []

# DEFINE VOLTAGE SOURCES 
V2 = component_classes.voltageSourceModel(name = "V2", node_p = 2, node_n = 1, type = "dc", type_dict = {"dc_voltage": 5})
components.append(V2)
V1 = component_classes.voltageSourceModel(name = "V1", node_p = 1, node_n = 0, type = "dc", type_dict = {"dc_voltage": 5})
components.append(V1)

# DEFINE CURRENT SOURCES
I1 = component_classes.currentSourceModel(name = "I1", node_p = 3, node_n = 0, type = "dc", type_dict = {"dc_current": -10})
components.append(I1)

# DEFINE RESISTORS
resistor_5_ohm_v1 = lambda resistor_tempetature: 5+max(0.1*(resistor_tempetature-25),0)
resistor_10_ohm_v1 = lambda resistor_tempetature: 10+max(0.2*(resistor_tempetature-25),0)

R1 = component_classes.resistorModel(name = "R1", node_p = 2, node_n = 3, resistance_function = resistor_10_ohm_v1, heat_capacity = 0.1, heat_transfer_coefficient = 0.1, resistor_temperature = 25)
components.append(R1)

R2 = component_classes.resistorModel(name = "R2", node_p = 3, node_n = 0, resistance_function =resistor_5_ohm_v1 , heat_capacity = 0.1, heat_transfer_coefficient = 0.1, resistor_temperature = 25)
components.append(R2)

R3 = component_classes.resistorModel(name = "R3", node_p = 4, node_n = 1, resistance_function =resistor_5_ohm_v1 , heat_capacity = 0.1, heat_transfer_coefficient = 0.1, resistor_temperature = 25)
components.append(R3)

# DEFINE INDUCTORS

# DEFINE CAPCACITORS
capacitor_10uF_v1 = lambda capacitor_voltage: 10e-6
C1 = component_classes.capacitorModel(name = "C1", node_p = 4, node_n = 0, capacitance_function = capacitor_10uF_v1, initial_voltage = 0)
components.append(C1)

#define unknowns
unknowns = {
   
}
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
     

#start simulation ===============================================================
max_time_step = 0.01 #seconds
time_step_now = max_time_step #seconds
simulation_time = max_time_step-0.0001 #seconds
print(unknowns)
time_now = 0 #seconds
while time_now < simulation_time:
    
    #append ground node information 
    info_matrix = np.zeros((1, number_of_unknowns))
    info_matrix[0,unknowns[f"V_{ground_node}"]] = 1
    result_vector = np.zeros((1,1))

    #append node voltage constraints due to voltage sources and capacitors
    for component in components:
        if component.get_component_category() == "VOLTAGE-SOURCE" or component.get_component_category() == "CAPACITOR":   
            positive_node = component.NODE_P
            negative_node = component.NODE_N
            voltage_difference = component.get_voltage(t=0) if component.get_component_category() == "VOLTAGE-SOURCE" else component.get_voltage()
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
                   
                   
        info_matrix = np.append(info_matrix, A, axis=0)
        result_vector = np.append(result_vector, B, axis=0)
    
    approximated_solution, residuals, rank, s = np.linalg.lstsq(info_matrix, result_vector, rcond=None)
    print(f"approximated_solution: {approximated_solution}")                  

                
                    
                 


        

    #update states if the state changes are small enough, otherwise decrease the time step
    time_now = time_now + time_step_now
