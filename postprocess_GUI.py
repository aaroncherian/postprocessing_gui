from pathlib import Path
import numpy as np

from PyQt6.QtWidgets import QMainWindow, QApplication, QTabWidget, QWidget, QVBoxLayout

from freemocap_utils.postprocessing_widgets.menus.main_menu import MainMenu
from freemocap_utils.postprocessing_widgets.menus.interpolation_menu import InterpolationMenu
from freemocap_utils.postprocessing_widgets.menus.filtering_menu import FilteringMenu
import toml

class FileManager:
    def __init__(self, path_to_recording: str):
        self.path_to_recording = path_to_recording
        #self.data_array_path = self.path_to_recording/'DataArrays'
        self.output_data_array_path = self.path_to_recording/'output_data'
        self.raw_data_array_path = self.output_data_array_path/'raw_data'

    def load_skeleton_data(self):
        # freemocap_raw_data = np.load(self.data_array_path/'mediaPipeSkel_3d.npy')
        freemocap_raw_data = np.load(self.raw_data_array_path/'mediapipe3dData_numFrames_numTrackedPoints_spatialXYZ.npy')
        freemocap_raw_data = freemocap_raw_data[:,0:33,:]
        return freemocap_raw_data

    def save_skeleton_data(self, skeleton_data:np.ndarray, skeleton_file_name:str, settings_dict:dict):
        np.save(self.output_data_array_path/skeleton_file_name,skeleton_data)

        output_toml_name = self.output_data_array_path/'postprocessing_settings.toml'
        toml_string = toml.dumps(settings_dict)

        with open(output_toml_name, 'w') as toml_file:
            toml_file.write(toml_string)


class PostProcessingGUI(QWidget):
    def __init__(self,path_to_data_folder:Path):
        super().__init__()

        layout = QVBoxLayout()

        self.file_manager = FileManager(path_to_recording=path_to_data_folder)

        self.resize(1256, 1029)

        self.setWindowTitle("Freemocap Data Post-processing")

        self.tab_widget = QTabWidget()

        freemocap_raw_data = self.file_manager.load_skeleton_data()

        self.main_menu_tab = MainMenu(freemocap_raw_data=freemocap_raw_data)
        self.tab_widget.addTab(self.main_menu_tab, 'Main Menu')

        self.interp_tab = InterpolationMenu(freemocap_raw_data = freemocap_raw_data)
        self.tab_widget.addTab(self.interp_tab, 'Interpolation')
        # layout.addWidget(self.main_menu)

        self.filter_tab = FilteringMenu(freemocap_raw_data=freemocap_raw_data)
        self.tab_widget.addTab(self.filter_tab, 'Filtering')

        layout.addWidget(self.tab_widget)

        self.main_menu_tab.save_skeleton_data_signal.connect(self.file_manager.save_skeleton_data)

        self.setLayout(layout)


        f = 2

class MainWindow(QMainWindow):
    def __init__(self,path_to_data_folder:Path):
        super().__init__()

        layout = QVBoxLayout()

        widget = QWidget()
        postprocessing_window = PostProcessingGUI(path_to_data_folder)

        layout.addWidget(postprocessing_window)

        widget.setLayout(layout)
        self.setCentralWidget(widget)


if __name__ == "__main__":
    
    # path_to_freemocap_session_folder = Path(r'D:\ValidationStudy2022\FreeMocap_Data\sesh_2022-05-24_16_10_46_JSM_T1_WalkRun')
    #path_to_freemocap_session_folder = Path(r'C:\Users\aaron\FreeMocap_Data\recording_sessions\recording_15_20_51_gmt-4__brit_half_inch')
    #path_to_freemocap_session_folder = Path(r'C:\Users\aaron\FreeMocap_Data\recording_sessions\recording_15_22_56_gmt-4__brit_one_inch')

    # path_to_freemocap_session_folder = Path(r'C:\Users\aaron\FreeMocap_Data\recording_sessions\recording_15_19_00_gmt-4__brit_baseline')
    # freemocap_raw_data = np.load(path_to_freemocap_session_folder/'output_data'/'raw_data'/'mediapipe3dData_numFrames_numTrackedPoints_spatialXYZ.npy')

    # freemocap_raw_data = np.load(path_to_freemocap_session_folder/'DataArrays'/'mediaPipeSkel_3d.npy')
    # freemocap_raw_data = freemocap_raw_data[:,0:33,:]


    path_to_data_folder = Path(r"D:\footropter_pilot_04_19_23\1.0_recordings\recordings_calib_3\sesh_2023-04-19_16_33_40_ML_fun")

    app = QApplication([])
    win = MainWindow(path_to_data_folder)
    win.show()
    app.exec()
