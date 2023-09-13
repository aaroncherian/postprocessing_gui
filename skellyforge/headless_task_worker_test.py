from skellyforge.freemocap_utils.postprocessing_widgets.task_worker_thread import TaskWorkerThread
import numpy as np
from skellyforge.freemocap_utils.config import default_settings


def handle_task_completed(task_name, result):
    print(f"Task {task_name} completed. Result:")
    # print(result)

freemocap_raw_data = np.load(r'D:\ValidationStudy2022\FreeMocap_Data\sesh_2022-05-24_16_10_46_JSM_T1_WalkRun\DataArrays\mediaPipeSkel_3d.npy')
freemocap_raw_data = freemocap_raw_data[:,0:33,:]



task_list = ['interpolation', 'filtering', 'finding good frame','skeleton rotation']
worker_thread = TaskWorkerThread(raw_skeleton_data=freemocap_raw_data, task_list=task_list, settings=default_settings,task_completed_callback=handle_task_completed)

worker_thread.start()
