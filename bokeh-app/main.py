#!/usr/bin/env python
# coding: utf-8

# In[8]:


# This cell imports all the required modules and functions.

#get_ipython().run_line_magic('run', 'Functions_FOR_BINDER.ipynb')
import Functions_FOR_BINDER as BINDER


# In[9]:


file_names = ["/Sample Input/Spatio-molecular data/subsampled_mf_obs.csv"]
#file_names = [r"C:\Users\NPS\Downloads\MAT_1_DATA_TYPE\mf_obs.csv"]
x_coordinate_column_names = ["center_x"]
y_coordinate_column_names = ["center_y"]
clusters_column_names = ["leiden"]

scale_for_sm_data = [1]


# In[10]:


# Name for this session.

title = ["MERFISH"]


# In[11]:


# Addresses of the "HE image" files along with their pixel size.

imgs = ["/Sample Input/HE images/1.jpg", 
        "/Sample Input/HE images/2.jpg", 
        "/Sample Input/HE images/3.jpg", 
        "/Sample Input/HE images/4.jpg"]

scale_for_he_image = 0.14


# In[12]:


# Type in the preferred display scale (in micrometer/pixel) for the plot

scale_bar = 1


# In[13]:


# Enter your current localhost port number.

#your_current_localhost_port_number = "localhost:8888"


# # BoReMi workspace
# 
# ### Ignore this warning if it shows up -
# #### UserWarning: Cannot find a last shown plot to update. Call output_notebook() and show(..., notebook_handle=True) before push_notebook() 

# In[14]:


## Ignore this warning if it shows up -
# UserWarning: Cannot find a last shown plot to update. 
# Call output_notebook() and show(..., notebook_handle=True) before push_notebook() 

# Everything downloaded via BoReMi (i.e., the updated x-y coordinates & the updated image)
# will get saved in the "Downloads" folder without showing a success prompt.

#def _boremi_(doc):

list_for_all_data_types, list_for_storing_total_clusters_info_in_each_file, list_for_storing_max_x_coordinate_of_each_file, list_for_storing_max_y_coordinate_of_each_file, list_for_storing_average_of_x_coordinated_of_each_file, list_for_storing_average_of_y_coordinated_of_each_file = BINDER.creating_required_number_of_input_dictionaries(file_names, x_coordinate_column_names, y_coordinate_column_names, clusters_column_names, scale_for_sm_data, title)

layout_for_display = BINDER.boremi(title, list_for_all_data_types, 
                                     list_for_storing_total_clusters_info_in_each_file, 
                                     list_for_storing_max_x_coordinate_of_each_file, 
                                     list_for_storing_max_y_coordinate_of_each_file, 
                                     list_for_storing_average_of_x_coordinated_of_each_file, 
                                     list_for_storing_average_of_y_coordinated_of_each_file, 
                                     imgs, title, scale_for_he_image, scale_for_sm_data, scale_bar)
    
#doc.add_root(layout_for_display)

curdoc().add_root(layout_for_display)
#output_notebook()
#show(Application(FunctionHandler(_boremi_)), notebook_url=your_current_localhost_port_number, notebook_handle=True)
#push_notebook()


# In[ ]:




