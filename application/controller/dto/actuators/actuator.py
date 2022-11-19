class Actuator:
    def __init__(self, id, type, description, value, options=None, min=None, max=None, step=None, unit=None):
        self.id = id
        self.type = type
        self.description = description
        self.value = value
        self.options = options
        self.min = min
        self.max = max
        self.step = step
        self.unit = unit