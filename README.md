# postprocessing_gui

# INSTALLING the GUI
 1. Create a 3.9 or 3.10 conda environment environment 
   -have tested this successfully on 3.9.16 (latest 3.9 version) and 3.10.11 (latest 3.10 version)
 2. Navigate to this github repo and use the command `pip install -e.` to install the dependencies from the pyproject.toml

# STARTING the GUI:
 1. Open up `postprocess_GUI.py`
 2. Scroll down to the `if __name__ == '__main__'` section at the bottom
 3. Change the `path_to_data_folder` variable to the path to your recording
   -NOTE: The GUI is set up to take file paths and file names corresponding to the 
          FreeMoCap 1.0 release. If you need to change these file paths, you can do so
          from the `FileManager` class at the top of `postprocess_GUI.py`
 4. After changing the path, run the `postprocess_GUI.py` script, and the GUI will pop up

# OPERATING the GUI 
 - When the GUI pops up you'll see the main menu, from which you can alter and apply
   various postprocessing parameters (currently mostly for interpolation/filtering)
 - Press the 'Process Data and View Results' button to run the postprocessing on the skeleton,
   and the postprocessed skeleton should appear in the 'post-processed data' skeleton viewer
 - You can move between the Filtering and Interpolation tabs at the top to more closely look
   at how the different processing options affect your data 
 - When finished, press the 'Save Out Data' button on the main menu to save the post_processed data
   and a .toml file of your processing parameters into the 'output_data' folder
 - Default processed data file name is 'mediapipe_processed_xyz.npy' and the parameter summary name
   is 'postprocessing_settings.toml'