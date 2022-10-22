class SharedAirActuators:
    def __init__(self, rotary_valve_1, rotary_valve_2, rotary_valve_3, discrete_valve_1,
        discrete_valve_2, discrete_valve_3, flap_valve_1, flap_valve_2, flap_valve_3, blower_on, 
        o3_generator, blower_strength):
        self.rotary_valve_1 = rotary_valve_1
        self.rotary_valve_2 = rotary_valve_2
        self.rotary_valve_3 = rotary_valve_3
        self.discrete_valve_1 = discrete_valve_1
        self.discrete_valve_2 = discrete_valve_2
        self.discrete_valve_3 = discrete_valve_3
        self.flap_valve_1 = flap_valve_1
        self.flap_valve_2 = flap_valve_2
        self.flap_valve_3 = flap_valve_3
        self.blower_on = blower_on
        self.o3_generator = o3_generator
        self.blower_strength = blower_strength