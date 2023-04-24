from pyqtgraph.parametertree import Parameter,registerParameterType


interpolation_settings = [
    {"name": "Interpolation", "type": "group", "children": [
        {
        "name": "Method", 
         "type": "list", 
         "values": ["linear", "cubic", "spline"]
         },
        {
        "name": "Order (only used in spline interpolation)", 
         "type": "int", 
         "value":3, 
         "step":1
         }
    ]}
]

filter_settings = [
        {"name": "Filtering", "type": "group", "children": [
        {"name": "Filter Type", "type": "list", "values": ["Butterworth Low Pass"]},
        {"name": "Order", "type":"int","value":4, "step":.1},
        {"name": "Cutoff Frequency", "type": "float", "value": 6.0, "step": 0.1},
        {"name": "Sampling Rate", "type": "float", "value": 30.0, "step": 0.1},
    ]}
]

interpolation_params = Parameter.create(name='interp_params', type='group', children=interpolation_settings)
filter_params = Parameter.create(name='filter_params',type='group', children=filter_settings )

class CustomRotationParam(Parameter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rotate_data_param = self.child("Rotation").child("Rotate Data")
        self.auto_find_good_frame_param = self.child("Rotation").child('Auto-find Good Frame')
        self.good_frame_param = self.child("Rotation").child("Good Frame")

        self.rotate_data_param.sigValueChanged.connect(self.rotate_data_changed)
        self.auto_find_good_frame_param.sigValueChanged.connect(self.auto_find_good_frame_changed)

    def rotate_data_changed(self, value):
        enabled = value.value()
        self.auto_find_good_frame_param.setOpts(enabled=enabled)
        self.good_frame_param.setOpts(enabled=enabled)

    def auto_find_good_frame_changed(self, value):
        if value.value():
            self.good_frame_param.setValue("")
            self.good_frame_param.setOpts(readonly=True)
        else:
            if not self.good_frame_param.value():
                self.good_frame_param.setValue("0")
            self.good_frame_param.setOpts(readonly=False)


rotation_settings = [
    {"name": "Rotation", "type": "group", "children": [
        {"name": "Rotate Data", "type": "bool", "value": True},
        {"name": "Instructions", "type": "str", "value": "Uncheck 'Auto-find Good Frame' to type in the good frame manually.", "readonly": True},
        {"name": "Auto-find Good Frame", "type": "bool", "value": True},
        {"name": "Good Frame", "type": "str", "value": "", "step": 1},
    ]}
]

registerParameterType('CustomRotationParam',CustomRotationParam)
rotation_params = Parameter.create(name='rotation_params', type='CustomRotationParam', children=rotation_settings) #the 'type' here refers to the parameter type we made the line above



if __name__ == "__main__":

    def get_all_parameter_values(parameter_object):
        values = {}
        for child in parameter_object.children(): #using this just to access the second level of the parameter tree
            if child.hasChildren():
                for grandchild in child.children():
                    values[grandchild.name()] = grandchild.value()
            else:
                values[child.name()] = child.value()
        return values

    values = get_all_parameter_values(filter_params)
    f =2 