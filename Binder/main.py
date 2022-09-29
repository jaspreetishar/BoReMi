import Functions_for_MAT

# Enter the address of the .csv / .xlsx / .h5ad file as the 1st parameter
# (in case of ".h5ad" file, the "x-y coordinates" and "clusters" containing dataframe 
# should be stored in the ".obs" parameter of the anndata object), followed by
# the names of the "column" containing "X coordinates", "Y coordinates" and "Clusters".

# If your file does not contain a column containing "Clusters", please write "none" 
# in the list "clusters_column_names" below.
# In the above mentioned case, all the coordinates will be stored in the "C_nan" checkbox of the tool.

# In case, some coordinates have not been grouped into any of the clusters, 
# they will also be stored in the "C_nan" checkbox of the tool.
# Also, make sure the 1st row of the file only contains "column names" and not some other information/sentences.

# If you want to test multiple data-types together, enter the different files addresses in the "file_names" list separated
# by commas. The same applies to all the other lists made for different column names.

file_names = ["/home/jovyan/Sample_Input/Spatio_molecular_Data/mf_obs.csv"]
x_coordinate_column_names = ["center_x"]
y_coordinate_column_names = ["center_y"]
clusters_column_names = ["leiden"]

# Type in the name of the data type in the list "title", e.g., slide seq, merfish, etc.

title = ["MERFISH"]
total_tabs = title

# Enter the addresses or URLs of H&E images for alignment (either absolute addresses or relative addresses).

imgs = ["/home/jovyan/Sample_Input/HE_Images/1.jpg", 
        "/home/jovyan/Sample_Input/HE_Images/2.jpg", 
        "/home/jovyan/Sample_Input/HE_Images/3.jpg", 
        "/home/jovyan/Sample_Input/HE_Images/4.jpg"]

# Enter your current localhost port number.

# your_current_localhost_port_number = "localhost:8891"

# Manual Alignment Tool

# Ignore this warning if it shows up -
# UserWarning: Cannot find a last shown plot to update. 
# Call output_notebook() and show(..., notebook_handle=True) before push_notebook()

# Everything downloaded via the Manual Alignment Tool (i.e., the updated x-y coordinates & the updated image)
# will get saved in the "Downloads" folder. The image however will get downloaded without showing a success prompt.

#def manual_alignment_tool(doc):

list_for_all_data_types, list_for_storing_total_clusters_info_in_each_file, list_for_storing_max_x_coordinate_of_each_file, list_for_storing_max_y_coordinate_of_each_file, list_for_storing_average_of_x_coordinated_of_each_file, list_for_storing_average_of_y_coordinated_of_each_file = creating_required_number_of_input_dictionaries(file_names, x_coordinate_column_names, y_coordinate_column_names, clusters_column_names, total_tabs)

layout_for_display = manual_alignment_tool_work_space(total_tabs, list_for_all_data_types, 
                                 list_for_storing_total_clusters_info_in_each_file, 
                                 list_for_storing_max_x_coordinate_of_each_file, 
                                 list_for_storing_max_y_coordinate_of_each_file, 
                                 list_for_storing_average_of_x_coordinated_of_each_file, 
                                 list_for_storing_average_of_y_coordinated_of_each_file, 
                                 imgs, title)
    
#doc.add_root(layout_for_display)
curdoc().add_root(layout_for_display)
curdoc().title = "Manual Alignment Tool"
#output_notebook()
#show(Application(FunctionHandler(manual_alignment_tool)), notebook_url=your_current_localhost_port_number, notebook_handle=True)
#push_notebook()
