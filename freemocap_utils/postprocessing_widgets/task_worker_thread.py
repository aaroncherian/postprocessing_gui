
from freemocap_utils.postprocessing_widgets.parameter_widgets import rotation_params
from freemocap_utils.postprocessing_widgets.postprocessing_functions.interpolate_data import interpolate_skeleton_data
from freemocap_utils.postprocessing_widgets.postprocessing_functions.filter_data import filter_skeleton_data
from freemocap_utils.postprocessing_widgets.postprocessing_functions.good_frame_finder import find_good_frame
from freemocap_utils.postprocessing_widgets.postprocessing_functions.rotate_skeleton import align_skeleton_with_origin

from freemocap_utils.postprocessing_widgets.visualization_widgets.mediapipe_skeleton_builder import mediapipe_indices


import numpy as np

import threading

class TaskWorkerThread(threading.Thread):
    def __init__(self, raw_skeleton_data:np.ndarray, task_list:list, settings:dict, task_running_callback=None, task_completed_callback=None, all_tasks_finished_callback=None):
        super().__init__()

        self.raw_skeleton_data = raw_skeleton_data
        self.available_tasks = {
            'interpolation': self.interpolate_task,
            'filtering': self.filter_task,
            'finding good frame': self.find_good_frame_task,
            'skeleton rotation': self.rotate_skeleton_task,
            'results visualization': None,
            'data saved': None
        }
        self.tasks = {task_name: {'function': self.available_tasks[task_name], 'result': None} for task_name in task_list}

        self.settings = settings
        results_dictionary = {}

        self.task_running_callback = task_running_callback
        self.task_completed_callback = task_completed_callback
        self.all_tasks_finished_callback = all_tasks_finished_callback



    def run(self):
        for task_info in self.tasks.values(): #clear any previous results 
            task_info['result'] = None

        for task_name, task_info in self.tasks.items():
            if task_info['function'] is not None:
                if self.task_running_callback is not None:
                    self.task_running_callback(task_name)
                
                is_completed, result = task_info['function']()
                
                task_info['result'] = result
                if is_completed:
                    if self.task_completed_callback is not None:
                        self.task_completed_callback(task_name, result)
                else:
                    if self.task_completed_callback is not None:
                        self.task_completed_callback(task_name, None)

        if self.all_tasks_finished_callback is not None:
            self.all_tasks_finished_callback(self.tasks)

    def interpolate_task(self):
        interpolation_values_dict = self.settings['Interpolation']
        interpolated_skeleton = interpolate_skeleton_data(self.raw_skeleton_data, method_to_use=interpolation_values_dict['Method'], order=interpolation_values_dict["Order"])
        return True,interpolated_skeleton

    def filter_task(self):
        filter_values_dict = self.settings['Filtering']
        filtered_skeleton = filter_skeleton_data(self.tasks['interpolation']['result'], order=filter_values_dict['Order'], cutoff=filter_values_dict['Cutoff Frequency'], sampling_rate=filter_values_dict['Sampling Rate'])
        return True,filtered_skeleton

    def find_good_frame_task(self):
        good_frame_values_dict = self.settings['Rotation']
        
        if good_frame_values_dict['Rotate Data']:
            #if auto find is selected
            if good_frame_values_dict['Auto-find Good Frame']:
                self.good_frame = find_good_frame(self.tasks['filtering']['result'], skeleton_indices=mediapipe_indices, initial_velocity_guess=.5)
                rotation_params.auto_find_good_frame_param.setValue(False)
                rotation_params.good_frame_param.setValue(str(self.good_frame))
            #if auto find is not, get the user entered good frame
            else:
                self.good_frame = int(good_frame_values_dict['Good Frame'])
            return True, self.good_frame
        else:
            #if no rotation is needed, we don't need to run the good frame finder
            self.good_frame = 0
            return False, self.good_frame


    def rotate_skeleton_task(self):
        rotate_values_dict = self.settings['Rotation']
        if rotate_values_dict['Rotate Data']:
            origin_aligned_skeleton = align_skeleton_with_origin(self.tasks['filtering']['result'], mediapipe_indices, self.good_frame)[0]
            return True, origin_aligned_skeleton
        else:
            origin_aligned_skeleton = None
            return False, origin_aligned_skeleton


    def get_all_parameter_values(self,parameter_object):
        values = {}
        for child in parameter_object.children(): #using this just to access the second level of the parameter tree
            if child.hasChildren():
                for grandchild in child.children():
                    values[grandchild.name()] = grandchild.value()
            else:
                values[child.name()] = child.value()
        return values