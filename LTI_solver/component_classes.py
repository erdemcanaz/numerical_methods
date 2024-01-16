# Description: This file contains the classes for the components of the circuit
# time -> seconds 
# voltage -> volts
# current -> amperes
# resistance -> ohms
# capacitance -> farads
# inductance -> henrys
# temperature -> celcius
# heat capacity -> joules/kelvin
# modified heat transfer coefficient -> watts/kelvin (surface area is assumed to be 1 m^2)

import math

class voltageSourceModel:
    def __init__(self, name, node_p= None, node_n = None , type = "", type_dict = {}):
        #name : name of the voltage source
        #node1 : positive node according to passive sign convention
        #node2 : negative node according to passive sign convention
        #type : type of the voltage source (dc, sine, pulse)
        #type_dict : dictionary containing the corresponding parameters of the voltage source type                 
        self.NAME = name
        self.NODE_P = node_p
        self.NODE_N = node_n
        self.TYPE = None
        self.TYPE_DICT = None

        self.ALLOWED_TYPES = ["dc", "sine", "pulse"]
        self.TYPE_REQUIREMENTS = {
            "dc":["dc_voltage"],
            "sine":["dc_offset", "amplitude", "frequency", "phase_shift_angle"],
            "pulse":["dc_offset", "amplitude", "normalized_duty", "period"]
        }
        if type not in self.ALLOWED_TYPES:
            raise ValueError(f"Type of the voltage source {name} is not supported. Supported types are {self.ALLOWED_TYPES}")
        for key in self.TYPE_REQUIREMENTS[type]:
            if key not in type_dict.keys():
                raise ValueError(f"'{key}' is not given for the voltage source {name}.")
        self.TYPE = type
        self.TYPE_DICT = type_dict
       
    def get_component_category(self):
        return "VOLTAGE-SOURCE"
    
    def get_voltage(self, t):
        if self.TYPE == "dc":
            return self.TYPE_DICT["dc_voltage"]
        elif self.TYPE == "sine":
            dc_offset = self.TYPE_DICT["dc_offset"]
            amplitude = self.TYPE_DICT["amplitude"]
            frequency = self.TYPE_DICT["frequency"]
            phase_shift_radian = self.TYPE_DICT["phase_shift_angle"]*0.0174532925 #degree to radian
            dc_offset = self.TYPE_DICT["dc_offset"]
            return dc_offset + amplitude*math.sin(2*math.pi*frequency*t + phase_shift_radian)
        elif self.TYPE == "pulse":
            dc_offset = self.TYPE_DICT["dc_offset"]
            amplitude = self.TYPE_DICT["amplitude"]
            normalized_duty = self.TYPE_DICT["normalized_duty"]
            period = self.TYPE_DICT["period"]
            is_on = (t % period) < (normalized_duty*period)
            return  dc_offset + amplitude*is_on
        else:
            raise ValueError(f"Type of the voltage source {self.NAME} is not supported. Supported types are {self.ALLOWED_TYPES}")

class currentSourceModel:
    def __init__(self, name, node_p= None, node_n = None , type = "", type_dict = {}):
        #name : name of the voltage source
        #node1 : positive node according to passive sign convention
        #node2 : negative node according to passive sign convention
        #type : type of the voltage source (dc, sine, pulse)
        #type_dict : dictionary containing the corresponding parameters of the voltage source type                 
        self.NAME = name
        self.NODE_P = node_p
        self.NODE_N = node_n
        self.TYPE = None
        self.TYPE_DICT = None

        self.ALLOWED_TYPES = ["dc", "sine", "pulse"]
        self.TYPE_REQUIREMENTS = {
            "dc":["dc_current"],
            "sine":["dc_offset", "amplitude", "frequency", "phase_shift_angle"],
            "pulse":["dc_offset", "amplitude", "normalized_duty", "period"]
        }
        if type not in self.ALLOWED_TYPES:
            raise ValueError(f"Type of the current source '{name}' is not supported. Supported types are {self.ALLOWED_TYPES}")
        for key in self.TYPE_REQUIREMENTS[type]:
            if key not in type_dict.keys():
                raise ValueError(f"'{key}' is not given for the current source {name}.")
        self.TYPE = type
        self.TYPE_DICT = type_dict
    
    def get_component_category(self):
        return "CURRENT-SOURCE"

    def get_current(self, t):
        if self.TYPE == "dc":
            return self.TYPE_DICT["dc_current"]
        elif self.TYPE == "sine":
            dc_offset = self.TYPE_DICT["dc_offset"]
            amplitude = self.TYPE_DICT["amplitude"]
            frequency = self.TYPE_DICT["frequency"]
            phase_shift_radian = self.TYPE_DICT["phase_shift_angle"]*0.0174532925 #degree to radian
            dc_offset = self.TYPE_DICT["dc_offset"]
            return dc_offset + amplitude*math.sin(2*math.pi*frequency*t + phase_shift_radian)
        elif self.TYPE == "pulse":
            dc_offset = self.TYPE_DICT["dc_offset"]
            amplitude = self.TYPE_DICT["amplitude"]
            normalized_duty = self.TYPE_DICT["normalized_duty"]
            period = self.TYPE_DICT["period"]
            is_on = (t % period) < (normalized_duty*period)
            return  dc_offset + amplitude*is_on
        else:
            raise ValueError(f"Type of the voltage source {self.NAME} is not supported. Supported types are {self.ALLOWED_TYPES}")
        
class resistorModel:
    def __init__(self, name, node_p= None, node_n = None , resistance_function = None, heat_capacity = None, heat_transfer_coefficient = None, resistor_temperature = None):
        #name : name of the resistor
        #node1 : positive node according to passive sign convention
        #node2 : negative node according to passive sign convention
        #resistance_function: function that returns the resistance of the resistor at a given temperature
        #heat_capacity: heat capacity of the resistor (joules/kelvin)
        #heat_transfer_coefficient: heat transfer coefficient of the resistor (watts/kelvin)
        #resistor_temperature: current temperature of the resistor (celcius)

        self.NAME = name
        self.NODE_P = node_p
        self.NODE_N = node_n
        self.RESISTANCE_FUNCTION = resistance_function
        self.HEAT_CAPACITY = heat_capacity
        self.HEAT_TRANSFER_COEFFICIENT = heat_transfer_coefficient
        self.RESISTOR_TEMPERATURE = resistor_temperature
    
    def get_component_category(self):
        return "RESISTOR"
    
    def get_resistance(self):
        return self.RESISTANCE_FUNCTION(self.RESISTOR_TEMPERATURE)

    def update_resistor_temperature(self, current, ambient_temperature, time_step):
        resistance = self.get_resistance()
        electrical_power = (current**2)*resistance # how much electrical power is dissipated in the resistor
        temperature_difference = self.RESISTOR_TEMPERATURE-ambient_temperature # how much hotter the resistor is compared to the ambient
        heat_transfer_power =  self.HEAT_TRANSFER_COEFFICIENT*temperature_difference # how much heat is transferred from the resistor to the ambient
        total_heat_energy_gained = (electrical_power-heat_transfer_power)*time_step
        total_resistor_temperature_change = total_heat_energy_gained/self.HEAT_CAPACITY
        self.RESISTOR_TEMPERATURE += total_resistor_temperature_change

class capacitorModel:
    def __init__(self, name, node_p= None, node_n = None , capacitance_function = None, initial_voltage = None):
        #name : name of the capacitor
        #node1 : positive node according to passive sign convention
        #node2 : negative node according to passive sign convention
        #capacitance_function: function that returns the capacitance of the capacitor at a given voltage
        #initial_voltage: initial voltage of the capacitor (volts)
        self.NAME = name
        self.NODE_P = node_p
        self.NODE_N = node_n
        self.CAPACITANCE_FUNCTION = capacitance_function
        self.VOLTAGE = initial_voltage

    def get_component_category(self):
        return "CAPACITOR"
    
    def get_capacitance(self):
        return self.CAPACITANCE_FUNCTION(self.VOLTAGE)
    
    def get_voltage(self):
        return self.VOLTAGE
    
    def get_voltage_change(self, current, time_step):
        capacitance = self.get_capacitance()
        return (current*time_step)/capacitance
    
    def update_voltage(self, current, time_step):
        self.VOLTAGE += self.get_voltage_change(current, time_step)
        


    

    



