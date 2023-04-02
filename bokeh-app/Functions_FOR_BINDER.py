#!/usr/bin/env python
# coding: utf-8

# In[1]:


# In-built packages/libraries

import numpy as np
import pandas as pd
import os
from PIL import Image
import anndata
from anndata import AnnData
import base64
import mimetypes
import math
from pathlib import Path
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource, BoxSelectTool, PanTool, LassoSelectTool
from bokeh.models import Div, WheelZoomTool, CustomJS, Slider, Spinner, Label
from bokeh.models import LabelSet, Range1d, Arrow, OpenHead, Button, Toggle, SaveTool, MultiChoice
from bokeh.models.widgets import Panel, Tabs
from bokeh.layouts import column, row
#from bokeh.events import ButtonClick, Pan, MouseEnter, RangesUpdate
from bokeh.plotting import figure, show
from bokeh.io import push_notebook, output_notebook, curdoc


# In[2]:


# for organizing input spatio-molecular data 

def dictionary_for_data(filename, x_coordinates, y_coordinates, scale_for_sm_data, clusters='none'):

    name, extension = os.path.splitext(filename)

    if extension == '.csv' or extension == '.xlsx':
        if extension == '.csv':
            data = pd.read_csv(filename) 
        if extension == '.xlsx':
            data = pd.read_excel(filename) 

        if clusters == 'none':
            clusters = [np.nan] * len(data[x_coordinates])
            data['Clusters'] = clusters
            clusters = 'Clusters'

        c = data[clusters].to_list()

        data[x_coordinates] = data[x_coordinates] / scale_for_sm_data 
        data[y_coordinates] = data[y_coordinates] / scale_for_sm_data 

        max_x_data = max(data[x_coordinates])
        max_y_data = max(data[y_coordinates])

        avg_xcoord=[]
        avg_ycoord=[]
        avg_xcoord.append(sum(data[x_coordinates])/len(data[x_coordinates]))
        avg_ycoord.append(sum(data[y_coordinates])/len(data[y_coordinates]))

        total_clus = list()
        for i in c:
            if i not in total_clus:
                total_clus.append(i)

        dict_of_data = {}
        for i in total_clus:
            if type(i) == int or type(i) == float:
                dict_of_data["C_{}".format(i)] = {}
                dict_of_data["C_{}".format(i)]['x']=[]
                dict_of_data["C_{}".format(i)]['y']=[]
            if type(i) == str:
                dict_of_data[i] = {}
                dict_of_data[i]['x']=[]
                dict_of_data[i]['y']=[]

        neg_count = len(list(filter(lambda x: (x < 0), data[x_coordinates])))
        pos_count = len(data[x_coordinates]) - neg_count

        if pos_count >= neg_count:
            for index, value in enumerate(data[clusters]):
                if type(value) == int or type(value) == float:
                    for key in dict_of_data:
                        if "C_{}".format(value) == key:
                            dict_of_data[key]['x'].append(data[x_coordinates][index])
                            dict_of_data[key]['y'].append(data[y_coordinates][index])
                if type(value) == str:
                    for key in dict_of_data:
                        if value == key:
                            dict_of_data[key]['x'].append(data[x_coordinates][index])
                            dict_of_data[key]['y'].append(data[y_coordinates][index])

        if neg_count > pos_count:
            for index, value in enumerate(data[clusters]):
                if type(value) == int or type(value) == float:
                    for key in dict_of_data:
                        if "C_{}".format(value) == key:
                            dict_of_data[key]['x'].append((data[x_coordinates][index]-min(data[x_coordinates])))
                            dict_of_data[key]['y'].append((data[y_coordinates][index]-min(data[y_coordinates])))
                if type(value) == str:
                    for key in dict_of_data:
                        if value == key:
                            dict_of_data[key]['x'].append((data[x_coordinates][index]-min(data[x_coordinates])))
                            dict_of_data[key]['y'].append((data[y_coordinates][index]-min(data[y_coordinates])))


    if extension == '.h5ad':
        data = anndata.read_h5ad(filename)   

        if clusters == 'none':
            clusters = [np.nan] * len(data.obs[x_coordinates])
            data.obs['Clusters'] = clusters
            clusters = 'Clusters'

        c = data.obs[clusters].to_list()

        data.obs[x_coordinates] = data.obs[x_coordinates] / scale_for_sm_data 
        data.obs[y_coordinates] = data.obs[y_coordinates] / scale_for_sm_data 

        max_x_data = max(data.obs[x_coordinates])
        max_y_data = max(data.obs[y_coordinates])

        avg_xcoord=[]
        avg_ycoord=[]
        avg_xcoord.append(sum(data.obs[x_coordinates])/len(data.obs[x_coordinates]))
        avg_ycoord.append(sum(data.obs[y_coordinates])/len(data.obs[y_coordinates]))

        total_clus = list()
        for i in c:
            if i not in total_clus:
                total_clus.append(i)

        dict_of_data = {}
        for i in total_clus:
            if type(i) == int or type(i) == float:
                dict_of_data["C_{}".format(i)] = {}
                dict_of_data["C_{}".format(i)]['x']=[]
                dict_of_data["C_{}".format(i)]['y']=[]
            if type(i) == str:
                dict_of_data[i] = {}
                dict_of_data[i]['x']=[]
                dict_of_data[i]['y']=[]

        neg_count = len(list(filter(lambda x: (x < 0), data.obs[x_coordinates])))
        pos_count = len(data.obs[x_coordinates]) - neg_count

        if pos_count >= neg_count:
            for index, value in enumerate(data.obs[clusters]):
                if type(value) == int or type(value) == float:
                    for key in dict_of_data:
                        if "C_{}".format(value) == key:
                            dict_of_data[key]['x'].append(data.obs[x_coordinates][index])
                            dict_of_data[key]['y'].append(data.obs[y_coordinates][index])
                if type(value) == str:
                    for key in dict_of_data:
                        if value == key:
                            dict_of_data[key]['x'].append(data.obs[x_coordinates][index])
                            dict_of_data[key]['y'].append(data.obs[y_coordinates][index])

        if neg_count > pos_count:
            for index, value in enumerate(data.obs[clusters]):
                if type(value) == int or type(value) == float:
                    for key in dict_of_data:
                        if "C_{}".format(value) == key:
                            dict_of_data[key]['x'].append((data.obs[x_coordinates][index]-min(data.obs[x_coordinates])))
                            dict_of_data[key]['y'].append((data.obs[y_coordinates][index]-min(data.obs[y_coordinates])))
                if type(value) == str:
                    for key in dict_of_data:
                        if value == key:
                            dict_of_data[key]['x'].append((data.obs[x_coordinates][index]-min(data.obs[x_coordinates])))
                            dict_of_data[key]['y'].append((data.obs[y_coordinates][index]-min(data.obs[y_coordinates])))

    list_of_keys = []
    for key in dict_of_data.keys():
        list_of_keys.append(key)

    return dict_of_data, list_of_keys, max_x_data, max_y_data, avg_xcoord, avg_ycoord


# In[ ]:





# In[3]:


def creating_required_number_of_input_dictionaries(file_names, x_coordinate_column_names,
                                                  y_coordinate_column_names, clusters_column_names, scale_for_sm_data, total_tabs):

    list_for_all_data_types = []
    list_for_storing_total_clusters_info_in_each_file = []
    list_for_storing_max_x_coordinate_of_each_file = []
    list_for_storing_max_y_coordinate_of_each_file = []
    list_for_storing_average_of_x_coordinated_of_each_file = []
    list_for_storing_average_of_y_coordinated_of_each_file = []

    for i in range(len(total_tabs)):
        dictionary_for_each_DATA, total_clus, max_x_data, max_y_data, avg_xcoord, avg_ycoord = dictionary_for_data(file_names[i],
                                                                                                              x_coordinate_column_names[i],
                                                                                                              y_coordinate_column_names[i],
                                                                                                              scale_for_sm_data[i],
                                                                                                              clusters_column_names[i])

        list_for_all_data_types.append(dictionary_for_each_DATA)
        list_for_storing_total_clusters_info_in_each_file.append(total_clus)
        list_for_storing_max_x_coordinate_of_each_file.append(max_x_data)
        list_for_storing_max_y_coordinate_of_each_file.append(max_y_data)
        list_for_storing_average_of_x_coordinated_of_each_file.append(avg_xcoord)
        list_for_storing_average_of_y_coordinated_of_each_file.append(avg_ycoord)

    return list_for_all_data_types, list_for_storing_total_clusters_info_in_each_file, list_for_storing_max_x_coordinate_of_each_file, list_for_storing_max_y_coordinate_of_each_file, list_for_storing_average_of_x_coordinated_of_each_file, list_for_storing_average_of_y_coordinated_of_each_file 


# In[ ]:





# In[4]:


# work space for boremi

def boremi(total_tabs, list_for_all_data_types, 
           list_for_storing_total_clusters_info_in_each_file, 
           list_for_storing_max_x_coordinate_of_each_file, 
           list_for_storing_max_y_coordinate_of_each_file, 
           list_for_storing_average_of_x_coordinated_of_each_file, 
           list_for_storing_average_of_y_coordinated_of_each_file, 
           imgs, title, scale_for_he_image, scale_for_sm_data, scale_bar):
    
    TABS = []
    
    list_for_multichoice = []
    list_for_img_number = []
    list_for_data_rot_angle = []
    list_for_data_pixel_size = []
    list_for_he_rot_angle = []
    list_for_toggle_vert = []
    list_for_toggle_hori = []
    list_for_image_save_button = []
    list_for_data_save_button = []
    list_for_data_point_size = []    
    list_for_scale_bar_pixel_size = []
    list_for_he_pixel_size = []

    dict_of_coordinates_for_source_final = {}
    dict_of_coordinates_for_source_final["xcoord"] = {}
    dict_of_coordinates_for_source_final["ycoord"] = {}

    dict_of_factors_for_data_resize = {}
    dict_of_factors_for_data_resize["numerators"] = {}
    dict_of_factors_for_data_resize["denominators"] = {}

    dict_for_active_array = {}
    dict_for_renderers = {}
    dict_of_sources = {}

    list_for_columndatasource_of_data_resize = []
    list_for_rotation_values = []
    list_for_data_table = []
    list_for_draw_tool = []
    list_of_source_final = []
    
    div_cluster_heading = []
    div_preview_imgs = []
    div_table_heading = []
    div_orientation = []
    div_px_size = []
    div_rot_angle = []
    
    uris = []
    divs_of_imgs = []

    div4space1 = [] 
    div4space2 = []
    div4space3 = [] 
    div4space4 = []
    div4space5 = []
    div4space6 = []

    for i in imgs:
        file_extension = os.path.splitext(i)[1]
        mimetypes.init()
        if file_extension in mimetypes.types_map:
            with open(i, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            encoded_string = 'data:' + mimetypes.types_map[file_extension] + ';base64,' + encoded_string

        else:
            raise ValueError(f'Unknown file extension {file_extension!r} of file {i!r}!')

        image = Image.open(i)
        width, height = image.size
        aspectratio = width/height
        uris.append(encoded_string)
        divs_of_imgs.append(Div(text = r'<img src= ' + encoded_string + r' style="width:100px;aspect_ratio:{};opacity:1" ></img>'. 
                               format(aspectratio), visible = True))

    for number_of_tab in range(len(total_tabs)):

        dict_of_factors_for_data_resize["numerators"][number_of_tab]=[]
        dict_of_factors_for_data_resize["numerators"][number_of_tab].append(scale_for_sm_data[number_of_tab])
        dict_of_factors_for_data_resize["denominators"][number_of_tab]=[]
        dict_of_factors_for_data_resize["denominators"][number_of_tab].append(1)
        list_for_columndatasource_of_data_resize.append(ColumnDataSource(data=dict(x=dict_of_factors_for_data_resize["numerators"][number_of_tab], 
                                                                y=dict_of_factors_for_data_resize["denominators"][number_of_tab])))

        list_for_rotation_values.append(ColumnDataSource(data=dict(x=list_for_storing_average_of_x_coordinated_of_each_file[number_of_tab], 
                                                     y=list_for_storing_average_of_y_coordinated_of_each_file[number_of_tab], 
                                                     rotval=[0])))

        num=[]       
        den=[]       
        for i in range(len(imgs)):
            num.append(scale_for_he_image)
            den.append(1)
        division_factor_for_resize_he = ColumnDataSource(data=dict(x=num, y=den))

        division_factor_for_resize_scale_bar = ColumnDataSource(data=dict(x=[1], y=[scale_bar]))

        width_of_images=[]
        height_of_images=[]
        for i in imgs:
            image = Image.open(i)
            width, height = image.size
            width_of_images.append(width/scale_for_he_image)
            height_of_images.append(height/scale_for_he_image)

        xmax_overall = max(width_of_images)
        ymax_overall = max(height_of_images)

        if number_of_tab == 0:
            visibility = True
        else:
            visibility = False

        df = pd.DataFrame(uris, columns=['imgs'])
        source_img = ColumnDataSource(df)
        
        df2 = pd.DataFrame(imgs, columns=['imgs'])
        source_img2 = ColumnDataSource(df2)

        max_value = max(list_for_storing_max_x_coordinate_of_each_file[number_of_tab], 
                        list_for_storing_max_y_coordinate_of_each_file[number_of_tab], 
                        xmax_overall, ymax_overall)
        p = figure(x_range=(0, max_value), y_range=(0, max_value), tools=[], title='BoReMi')
        im = p.image_url(url=[source_img.data['imgs'][0]], 
                         x=width_of_images[0]/2, 
                         y=height_of_images[0]/2, 
                         w=width_of_images[0], 
                         h=height_of_images[0], 
                         anchor='center', angle_units='rad', angle=0)
        p.add_tools(WheelZoomTool(), BoxSelectTool(dimensions="both"), 
                    PanTool(dimensions="both"), LassoSelectTool(), SaveTool())

        my_arrow = Arrow(end=OpenHead(size=10), start=OpenHead(size=10), line_color="black", visible=True,
                         x_start=max_value-1500, y_start=600, x_end=max_value-500, y_end=600, line_alpha=1,line_width=2)
        p.add_layout(my_arrow)

        labels = Label(x=max_value-1500, y=600, x_offset=15, y_offset=-30, x_units='data', y_units='data', 
                       text='1 mm', render_mode='css',
                       border_line_color='black', border_line_alpha=1.0,
                       background_fill_color='white', background_fill_alpha=1.0,
                       text_font_size='10px', visible=True)

        p.add_layout(labels)
        dict_of_sources[number_of_tab] = {}
        dict_for_renderers[number_of_tab] = []

        ordered = pd.DataFrame()
        clusters_ordered = []
        ascii_ = []
        if type(list_for_storing_total_clusters_info_in_each_file[number_of_tab][0]) == str:
            for i in list_for_storing_total_clusters_info_in_each_file[number_of_tab]:
                sum_ascii = 0
                for j in i:
                    sum_ascii = sum_ascii + ord(j)
                ascii_.append(sum_ascii)
                clusters_ordered.append(i)
            ordered['Clusters']=clusters_ordered
            ordered['ASCII values']=ascii_
            ordered = ordered.sort_values('ASCII values')
            ordered.head(40)
            list_for_storing_total_clusters_info_in_each_file[number_of_tab] = ordered['Clusters'].to_list()

        if type(list_for_storing_total_clusters_info_in_each_file[number_of_tab][0]) == int or type(list_for_storing_total_clusters_info_in_each_file[number_of_tab][0]) == float:
            list_for_storing_total_clusters_info_in_each_file[number_of_tab].sort()

        for i in list_for_storing_total_clusters_info_in_each_file[number_of_tab]:
            if type(i) == int or type(i) == float:
                dict_of_sources[number_of_tab]["C{}".format(i)] = ColumnDataSource(data=dict(x=list_for_all_data_types[number_of_tab]["C_{}".format(i)]['x'], 
                                                                      y=list_for_all_data_types[number_of_tab]["C_{}".format(i)]['y']))
                dict_for_renderers[number_of_tab].append(p.scatter(x='x', y='y', source=dict_of_sources[number_of_tab]["C{}".format(i)], color='red', size=0.09, 
                                           selection_color='blue',
                                           nonselection_alpha=0))
            if type(i) == str:
                dict_of_sources[number_of_tab][i] = ColumnDataSource(data=dict(x=list_for_all_data_types[number_of_tab][i]['x'], 
                                                        y=list_for_all_data_types[number_of_tab][i]['y']))
                dict_for_renderers[number_of_tab].append(p.scatter(x='x', y='y', source=dict_of_sources[number_of_tab][i], color='red', size=0.09, 
                                           selection_color='blue',
                                           nonselection_alpha=0))

        dict_of_coordinates_for_source_final["xcoord"][number_of_tab] = []
        dict_of_coordinates_for_source_final["ycoord"][number_of_tab] = []
        for key, value in dict_of_sources[number_of_tab].items():
            dict_of_coordinates_for_source_final["xcoord"][number_of_tab].append(value.data['x'])
            dict_of_coordinates_for_source_final["ycoord"][number_of_tab].append(value.data['y'])
        dict_of_coordinates_for_source_final["xcoord"][number_of_tab] = [item for sublist in dict_of_coordinates_for_source_final["xcoord"][number_of_tab] for item in sublist]
        dict_of_coordinates_for_source_final["ycoord"][number_of_tab] = [item for sublist in dict_of_coordinates_for_source_final["ycoord"][number_of_tab] for item in sublist]    

        list_of_source_final.append(ColumnDataSource(data=dict(x=dict_of_coordinates_for_source_final["xcoord"][number_of_tab], 
                                                               y=dict_of_coordinates_for_source_final["ycoord"][number_of_tab])))
        columns = [TableColumn(field="x", title="x"),
                   TableColumn(field="y", title="y")]

        list_for_data_table.append(DataTable(source=list_of_source_final[number_of_tab], columns=columns, 
                                             editable=True, height=200, visible=visibility))
        list_for_draw_tool.append(PointDrawTool(renderers=dict_for_renderers[number_of_tab], 
                                                empty_value='red', add=False))
        p.add_tools(list_for_draw_tool[number_of_tab])

        dict_for_active_array[number_of_tab] = []
        for i in range(len(list_for_storing_total_clusters_info_in_each_file[number_of_tab])):
            dict_for_active_array[number_of_tab].append(i)    

        div_cluster_heading.append(Div(text="""Select/Unselect combinations of clusters based on whether a distinct pattern is visible: """, 
                             visible=visibility, width=1000, sizing_mode="stretch_height", height=15))

        # multichoice - for finding patterns

        list_for_multichoice.append(MultiChoice(value=list_for_storing_total_clusters_info_in_each_file[number_of_tab], 
                                                        options=list_for_storing_total_clusters_info_in_each_file[number_of_tab],
                                                        visible=visibility, default_size = 600))
        # image gallery
       
        list_for_img_number.append(Spinner(title="Image Number:", low=0, high=len(imgs)-1, 
                                   step=1, value=0, width=200, visible=visibility))
    
        # pixel size for h&e image
        
        list_for_he_pixel_size.append(Spinner(title="H&E Image:", 
                                                         low=0.01, high=3, step=0.01, value=scale_for_he_image, 
                                                          width=200, visible=visibility))

        # for modifying data point size
        list_for_data_point_size.append(Spinner(title="Data Point Size (lowest: 0.06, highest: 10):", 
                          low=0.06, high=10, step=0.001, value=0.09, width=200, visible=visibility))

        # rotation for data
        list_for_data_rot_angle.append(Spinner(title="Data:", 
                           low=-360, high=360, step=1, value=0, width=200, visible=visibility))

        # pixel size for data
        list_for_data_pixel_size.append(Spinner(title="Data:",
                                                low=0.01, high=3, step=0.01, value=scale_for_sm_data[number_of_tab],
                                                width=200
                                                ,visible=visibility))

        # pixel size for scale bar
        list_for_scale_bar_pixel_size.append(Spinner(title="Display Scale:",
                                                            low=0.01, high=3, step=0.01, value=scale_bar, width=200
                                                           ,visible=visibility))        

        # for changing orientation of data
        list_for_toggle_vert.append(Toggle(label="Flip about Vertical Plane", button_type="success",
                                                            visible=visibility))

        list_for_toggle_hori.append(Toggle(label="Flip about Horizontal Plane", button_type="success",
                                                            visible=visibility))

        # for saving modified coordinates
        list_for_data_save_button.append(Button(label="Download Updated Spatial Coordinates", 
                                                                button_type="success",width=370,visible=visibility))

        # rotation for h&e image
        list_for_he_rot_angle.append(Spinner(title="H&E Image:", 
                                    low=-360, high=360, step=1, value=0, width=200,visible=visibility))
        
        
        list_for_image_save_button.append(Button(label="Download Updated Image", button_type="success",
                                                                 width = 430, visible=visibility))
        
        
        # callbacks
        
        def multichoice_callback(attr, old, new):
            
            renderers = dict_for_renderers[number_of_tab]
            multichoice = list_for_multichoice[number_of_tab]
            table = list_for_data_table[number_of_tab]
            all_clusters = list_for_storing_total_clusters_info_in_each_file[number_of_tab]
            
            xval = table.source.data['x']
            yval = table.source.data['y']
            selected_vals = multichoice.value
            
            for i, value in enumerate(all_clusters):

                if value in selected_vals:
                    renderers[i].glyph.fill_alpha=1
                    renderers[i].glyph.line_alpha=1
                    renderers[i].selection_glyph.fill_alpha=1
                    renderers[i].selection_glyph.line_alpha=1
                
                else:
                    renderers[i].glyph.fill_alpha=0
                    renderers[i].glyph.line_alpha=0
                    renderers[i].selection_glyph.fill_alpha=0
                    renderers[i].selection_glyph.line_alpha=0

        list_for_multichoice[number_of_tab].on_change('value', multichoice_callback)
                        
        def img_number_callback(attr, old, new):
            
            px_size = list_for_he_pixel_size[number_of_tab] 
            image_number = list_for_img_number[number_of_tab]
            scale_bar_px_size = list_for_scale_bar_pixel_size[number_of_tab]
                   
            P = px_size.value
            N = image_number.value
            S = scale_bar_px_size.value

            num_fac_scale_bar = division_factor_for_resize_scale_bar.data['x']
            den_fac_scale_bar = division_factor_for_resize_scale_bar.data['y']
            resize_fac_scale_bar = num_fac_scale_bar[0]/den_fac_scale_bar[0]

            im.data_source.data['url'] = [source_img.data['imgs'][N]]
            
            num_fac = division_factor_for_resize_he.data['x']
            den_fac = division_factor_for_resize_he.data['y']
            resize_fac = num_fac[N]/den_fac[N]
            num_fac[N] = P
            den_fac[N] = 1

            width_of_images[N] = (width_of_images[N] / P) * resize_fac * resize_fac_scale_bar * S
            height_of_images[N] = (height_of_images[N] / P) * resize_fac * resize_fac_scale_bar * S

            im.glyph.x = width_of_images[N]/2
            im.glyph.y = height_of_images[N]/2
            im.glyph.w = width_of_images[N]
            im.glyph.h = height_of_images[N]
            im.glyph.anchor = 'center'
            
            division_factor_for_resize_he.data['x'] = num_fac
            division_factor_for_resize_he.data['y'] = den_fac

        list_for_img_number[number_of_tab].on_change('value', img_number_callback)    
        list_for_scale_bar_pixel_size[number_of_tab].on_change('value', img_number_callback)        
        list_for_he_pixel_size[number_of_tab].on_change('value', img_number_callback)
        
        def data_point_size(attr, old, new):
            for i in dict_for_renderers[number_of_tab]:
                i.glyph.size = list_for_data_point_size[number_of_tab].value
                
        list_for_data_point_size[number_of_tab].on_change('value', data_point_size)

        def data_rot_callback(attr, old, new):
             
            A = list_for_data_rot_angle[number_of_tab].value - list_for_rotation_values[number_of_tab].data['rotval'][0]
            list_for_rotation_values[number_of_tab].data['rotval'][0] = list_for_data_rot_angle[number_of_tab].value
            radians = (math.pi / 180) * A
            
            cos = math.cos(radians)
            sin = math.sin(radians)

            x = list_for_data_table[number_of_tab].source.data['x']
            y = list_for_data_table[number_of_tab].source.data['y']

            w = list_for_rotation_values[number_of_tab].data['x']
            h = list_for_rotation_values[number_of_tab].data['y']
            
            for i in range(len(x)):
                X = x[i]
                Y = y[i]
                x[i] = ((X-w[0])*cos) - ((Y-h[0])*sin) + w[0]
                y[i] = ((X-w[0])*sin) + ((Y-h[0])*cos) + h[0] 
                
            for i in dict_for_renderers[number_of_tab]:
                if i.selection_glyph.fill_alpha != 0:
                    xval = i.data_source.data['x']
                    yval = i.data_source.data['y']

                    for z in range(len(xval)): 
                        X = xval[z]
                        Y = yval[z]
                        xval[z] = ((X-w[0])*cos) - ((Y-h[0])*sin) + w[0]
                        yval[z] = ((X-w[0])*sin) + ((Y-h[0])*cos) + h[0]

                    i.data_source.data['x'] = xval
                    i.data_source.data['y'] = yval
                        
            list_for_data_table[number_of_tab].source.data['x'] = x
            list_for_data_table[number_of_tab].source.data['y'] = y
            
        list_for_data_rot_angle[number_of_tab].on_change('value', data_rot_callback)
        
        def data_pixel_size_callback(attr, old, new):
            
            F = list_for_data_pixel_size[number_of_tab].value
            num_fac = list_for_columndatasource_of_data_resize[number_of_tab].data['x']
            den_fac = list_for_columndatasource_of_data_resize[number_of_tab].data['y']
            N = list_for_img_number[number_of_tab].value

            resize_fac = num_fac[0] / den_fac[0]

            S = list_for_scale_bar_pixel_size[number_of_tab].value

            num_fac_scale_bar = division_factor_for_resize_scale_bar.data['x']
            den_fac_scale_bar = division_factor_for_resize_scale_bar.data['y']
            resize_fac_scale_bar = num_fac_scale_bar[0]/den_fac_scale_bar[0]
            
            x = list_for_data_table[number_of_tab].source.data['x']
            y = list_for_data_table[number_of_tab].source.data['y']

            w = list_for_rotation_values[number_of_tab].data['x']
            h = list_for_rotation_values[number_of_tab].data['y']
            x_sum = 0
            y_sum = 0

            for i in range(len(x)): 
                
                X= x[i]
                Y= y[i]
                x[i] = (X / F) * resize_fac * resize_fac_scale_bar * S
                y[i] = (Y / F) * resize_fac * resize_fac_scale_bar * S
                x_sum += x[i]
                y_sum += y[i]
                 
            list_for_data_table[number_of_tab].source.data['x'] = x
            list_for_data_table[number_of_tab].source.data['y'] = y

            w[0] = x_sum/len(x)
            h[0] = y_sum/len(y)
            
            list_for_rotation_values[number_of_tab].data['x'] = w
            list_for_rotation_values[number_of_tab].data['y'] = h

            for i in dict_for_renderers[number_of_tab]:
                
                if i.selection_glyph.fill_alpha != 0:
                    xval= i.data_source.data['x']
                    yval= i.data_source.data['y']

                    for z in range(len(xval)):
                        X = xval[z]
                        Y = yval[z]
                        xval[z] = (X / F) * resize_fac * resize_fac_scale_bar * S
                        yval[z] = (Y / F) * resize_fac * resize_fac_scale_bar * S

                    i.data_source.data['x'] = xval
                    i.data_source.data['y'] = yval

            num_fac[0] = F
            den_fac[0] = 1
            
            list_for_columndatasource_of_data_resize[number_of_tab].data['x'] = num_fac
            list_for_columndatasource_of_data_resize[number_of_tab].data['y'] = den_fac
            
            num_fac_scale_bar[0] = 1
            den_fac_scale_bar[0] = S
            
            division_factor_for_resize_scale_bar.data['x'] = num_fac_scale_bar
            division_factor_for_resize_scale_bar.data['y'] = den_fac_scale_bar
        
        list_for_data_pixel_size[number_of_tab].on_change('value', data_pixel_size_callback)
        list_for_data_rot_angle[number_of_tab].on_change('value', data_pixel_size_callback)
        list_for_scale_bar_pixel_size[number_of_tab].on_change('value', data_pixel_size_callback)
        
        def he_rot_angle_callback(attr, old, new):
            
            radians = (math.pi / 180) * list_for_he_rot_angle[number_of_tab].value
            im.glyph.angle = radians
        
        list_for_he_rot_angle[number_of_tab].on_change('value', he_rot_angle_callback)

        def toggle_vert_callback(new):

            x = list_for_data_table[number_of_tab].source.data['x']
            y = list_for_data_table[number_of_tab].source.data['y']

            w = list_for_rotation_values[number_of_tab].data['x']
            h = list_for_rotation_values[number_of_tab].data['y']
            rotval = list_for_rotation_values[number_of_tab].data['rotval']

            x_sum = 0
            y_sum = 0

            if rotval[0] == 0:
                for i in range(len(x)): 
                    x[i] = w[0] + (w[0] - x[i]);
                    x_sum += x[i]
                    y_sum += y[i]
            
            if rotval[0] > 0:
                for i in range(len(x)): 
                    x[i] = h[0] + (h[0] - y[i])
                    y[i] = w[0] + (w[0] - x[i])
                    x_sum += x[i]
                    y_sum += y[i]

            if rotval[0] < 0:
                for i in range(len(x)): 
                    x[i] = h[0] + (h[0] - y[i])
                    y[i] = w[0] + (w[0] - x[i])
                    x_sum += x[i]
                    y_sum += y[i]
                
            for i in dict_for_renderers[number_of_tab]:
                xval= i.data_source.data['x']
                yval= i.data_source.data['y']

                if rotval[0] == 0:
                    for z in range(len(xval)):
                        xval[z] = w[0] + (w[0] - xval[z])

                if rotval[0] > 0: 
                    for z in range(len(xval)):
                        X=xval[z]
                        Y=yval[z]
                        xval[z] = h[0] + (h[0] - Y)
                        yval[z] = w[0] + (w[0] - X)

                if rotval[0] < 0:
                    for z in range(len(xval)):
                        X=xval[z]
                        Y=yval[z]
                        xval[z] = h[0] + (h[0] - Y)
                        yval[z] = w[0] + (w[0] - X)
            
                i.data_source.data['x'] = xval
                i.data_source.data['y'] = yval
    
            w[0] = x_sum/len(x)
            h[0] = y_sum/len(y)
            
            list_for_rotation_values[number_of_tab].data['x'] = w
            list_for_rotation_values[number_of_tab].data['y'] = h
            
            list_for_data_table[number_of_tab].source.data['x'] = x
            list_for_data_table[number_of_tab].source.data['y'] = y
        
        list_for_toggle_vert[number_of_tab].on_click(toggle_vert_callback)
        
        def toggle_hori_callback(new):
                    
            x = list_for_data_table[number_of_tab].source.data['x']
            y = list_for_data_table[number_of_tab].source.data['y']

            w = list_for_rotation_values[number_of_tab].data['x']
            h = list_for_rotation_values[number_of_tab].data['y']
            rotval = list_for_rotation_values[number_of_tab].data['rotval']

            x_sum = 0
            y_sum = 0

            if rotval[0] == 0:
                for i in range(len(x)):
                    y[i] = h[0] + (h[0] - y[i])
                    x_sum += x[i]
                    y_sum += y[i]

            if rotval[0] > 0:
                for i in range(len(x)):
                    x[i] = w[0] + (w[0] - x[i])
                    y[i] = h[0] + (h[0] - y[i])
                    x_sum += x[i]
                    y_sum += y[i]
            
            if rotval[0] < 0:
                for i in range(len(x)):
                    x[i] = w[0] + (w[0] - x[i])
                    y[i] = h[0] + (h[0] - y[i])
                    x_sum += x[i]
                    y_sum += y[i]

            for i in dict_for_renderers[number_of_tab]:
                xval= i.data_source.data['x']
                yval= i.data_source.data['y']

                if rotval[0] == 0:
                    for z in range(len(xval)):
                        yval[z] = h[0] + (h[0] - yval[z])

                if rotval[0] > 0:
                    for z in range(len(xval)):
                        xval[z] = w[0] + (w[0] - xval[z])
                        yval[z] = h[0] + (h[0] - yval[z])

                if rotval[0] < 0:
                    for z in range(len(xval)):
                        xval[z] = w[0] + (w[0] - xval[z])
                        yval[z] = h[0] + (h[0] - yval[z])

                i.data_source.data['x'] = xval
                i.data_source.data['y'] = yval
            
            w[0] = x_sum/len(x)
            h[0] = y_sum/len(y)
            
            list_for_data_table[number_of_tab].source.data['x'] = x
            list_for_data_table[number_of_tab].source.data['y'] = y

            list_for_rotation_values[number_of_tab].data['x'] = w
            list_for_rotation_values[number_of_tab].data['y'] = h

        list_for_toggle_hori[number_of_tab].on_click(toggle_hori_callback)
        
        def data_download():
            
            data = list_for_data_table[number_of_tab].source.data
            x = data['x']
            y = data['y']

            modified_data = pd.DataFrame()
            modified_data['x'] = x
            modified_data['y'] = y
                    
            modified_data.to_csv("Updated_Spatial_Data.csv")  
        
        list_for_data_save_button[number_of_tab].on_click(data_download)

        def image_download():

            P = list_for_he_pixel_size[number_of_tab].value
            N = list_for_img_number[number_of_tab].value
            S = list_for_scale_bar_pixel_size[number_of_tab].value
            angle = list_for_he_rot_angle[number_of_tab].value

            num_fac_scale_bar = division_factor_for_resize_scale_bar.data['x']
            den_fac_scale_bar = division_factor_for_resize_scale_bar.data['y']
            resize_fac_scale_bar = num_fac_scale_bar[0]/den_fac_scale_bar[0]

            num_fac = division_factor_for_resize_he.data['x']
            den_fac = division_factor_for_resize_he.data['y']
            resize_fac = num_fac[N]/den_fac[N]

            image = Image.open(source_img2.data['imgs'][N])
            width, height = image.size

            new_width = (width_of_images[N] / P) * resize_fac * resize_fac_scale_bar * S
            new_height = (height_of_images[N] / P) * resize_fac * resize_fac_scale_bar * S
            
            image = image.resize((round(new_width), round(new_height)),
                                 Image.BICUBIC)
            image = image.rotate(angle, Image.NEAREST, expand = 1, fillcolor = (255,255,255))
            
            image.save("Updated_H&E_Image.jpg")

        list_for_image_save_button[number_of_tab].on_click(image_download)
        
        def scale_bar_callback(attr, old, new):

            Size = list_for_scale_bar_pixel_size[number_of_tab].value
            S = Size * 1000

            my_arrow.x_end = p.x_range.end - 500
            my_arrow.x_start = p.x_range.end - (500+S)
            my_arrow.y_end = p.y_range.start + 600
            my_arrow.y_start = p.y_range.start + 600
            my_arrow.visible = True

            labels.x = p.x_range.end - (500+S)
            labels.y = p.y_range.start + 600
            labels.text = f"{Size} mm"
            labels.x_offset = 15 * Size
            labels.visible = True
       
        list_for_scale_bar_pixel_size[number_of_tab].on_change('value', scale_bar_callback)
        
        #p.on_event(RangesUpdate, FOR_PLOT_scale_bar_callback)
        #p.on_event('pan', FOR_PLOT_multichoice_callback)
        #p.on_event('pan', FOR_PLOT_data_pixel_size_callback)
        #p.on_event('mouseenter', FOR_PLOT_data_pixel_size_callback)

        div_orientation.append(Div(text="""Change Orientation of Data:""", visible = visibility, height=15))
        div_table_heading.append(Div(text="""Updated Spatial Coordinates (x, y): """, visible = visibility, height=15))
        div_preview_imgs.append(Div(text="""Preview of Images: """, visible = visibility, height=15))
        div_px_size.append(Div(text="""Pixel Size (in um/px) Range: 0.01 to 3 =""", visible = visibility, height=15))
        div_rot_angle.append(Div(text="""Rotation Angle (in degrees) Range: -360 to 360 =""", visible = visibility, height=15))

        div4space1.append(Div(text="""""", visible = visibility))
        div4space2.append(Div(text="""""", visible = visibility))
        div4space3.append(Div(text="""""", visible = visibility))
        div4space4.append(Div(text="""""", visible = visibility, height=10))
        div4space5.append(Div(text="""""", visible = visibility, height=10))
        div4space6.append(Div(text="""""", visible = visibility))
                
        TABS.append(Panel(child=p, title=title[number_of_tab]))
    
    TabS = Tabs(tabs = TABS)   
    
    def callback_for_tabs(attr, old, new):
        
        for j in range(len(total_tabs)):
            
            list_for_multichoice[j].visible=False
            list_for_toggle_vert[j].visible=False
            list_for_toggle_hori[j].visible=False
            list_for_data_pixel_size[j].visible=False
            list_for_data_rot_angle[j].visible=False
            list_for_data_table[j].visible=False
            list_for_data_save_button[j].visible=False
            list_for_data_point_size[j].visible=False
            list_for_he_pixel_size[j].visible=False
            list_for_he_rot_angle[j].visible=False
            list_for_img_number[j].visible=False
            div_cluster_heading[j].visible=False
            div_preview_imgs[j].visible=False
            div_table_heading[j].visible=False
            div_px_size[j].visible=False
            div4space1[j].visible=False
            div4space2[j].visible=False
            div_rot_angle[j].visible=False
            div4space3[j].visible=False
            div4space4[j].visible=False
            div4space5[j].visible=False
            div4space6[j].visible=False
            div_orientation[j].visible=False
            list_for_scale_bar_pixel_size[j].visible=False
            list_for_image_save_button[j].visible=False  
            
        for j in range(len(total_tabs)):
         
            if TabS.active == j:

                list_for_multichoice[j].visible=True
                list_for_toggle_vert[j].visible=True
                list_for_toggle_hori[j].visible=True
                list_for_data_pixel_size[j].visible=True
                list_for_data_rot_angle[j].visible=True
                list_for_data_table[j].visible=True
                list_for_data_save_button[j].visible=True
                list_for_data_point_size[j].visible=True
                list_for_he_pixel_size[j].visible=True
                list_for_he_rot_angle[j].visible=True
                list_for_img_number[j].visible=True
                div_cluster_heading[j].visible=True
                div_preview_imgs[j].visible=True
                div_table_heading[j].visible=True
                div_px_size[j].visible=True
                div4space1[j].visible=True
                div4space2[j].visible=True
                div_rot_angle[j].visible=True
                div4space3[j].visible=True
                div4space4[j].visible=True
                div4space5[j].visible=True
                div4space6[j].visible=True
                div_orientation[j].visible=True
                list_for_scale_bar_pixel_size[j].visible=True
                list_for_image_save_button[j].visible=True
            
            else:
                
                list_for_multichoice[j].visible=False
                list_for_toggle_vert[j].visible=False
                list_for_toggle_hori[j].visible=False
                list_for_data_pixel_size[j].visible=False
                list_for_data_rot_angle[j].visible=False
                list_for_data_table[j].visible=False
                list_for_data_save_button[j].visible=False
                list_for_data_point_size[j].visible=False
                list_for_he_pixel_size[j].visible=False
                list_for_he_rot_angle[j].visible=False
                list_for_img_number[j].visible=False
                div_cluster_heading[j].visible=False
                div_preview_imgs[j].visible=False
                div_table_heading[j].visible=False
                div_px_size[j].visible=False
                div4space1[j].visible=False
                div4space2[j].visible=False
                div_rot_angle[j].visible=False
                div4space3[j].visible=False
                div4space4[j].visible=False
                div4space5[j].visible=False
                div4space6[j].visible=False
                div_orientation[j].visible=False
                list_for_scale_bar_pixel_size[j].visible=False
                list_for_image_save_button[j].visible=False  
                
    TabS.on_change('active', callback_for_tabs)
    
    layout_for_display = row(column(TabS, row(div4space1), 
         row(row(div_table_heading), row(div4space2), row(list_for_data_save_button)), 
         row(list_for_data_table)), column(row(div_cluster_heading), 
         row(list_for_multichoice), row(div_orientation), 
         row(row(list_for_toggle_vert), row(list_for_toggle_hori)), 
         row(div4space3), row(list_for_data_point_size), 
         row(div4space4),       
         row(div_px_size),
         row(row(list_for_data_pixel_size), row(list_for_he_pixel_size), row(list_for_scale_bar_pixel_size)), 
         row(div4space5), 
         row(div_rot_angle),
         row(row(list_for_data_rot_angle), row(list_for_he_rot_angle)), 
         row(div4space6),
         row(list_for_img_number), 
         row(div_preview_imgs), row(divs_of_imgs), row(list_for_image_save_button)))
    
    return layout_for_display


# In[ ]:





# In[ ]:


#print("All required Modules and Packages have been imported")

