# In-built packages/libraries

import numpy as np
import pandas as pd
import os
from PIL import Image
import anndata
from anndata import AnnData
import base64
import mimetypes
from pathlib import Path
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource, BoxSelectTool, PanTool, LassoSelectTool
from bokeh.models import Div, WheelZoomTool, CustomJS, Slider, Spinner, Label
from bokeh.models import LabelSet, Range1d, Arrow, OpenHead, Button, Toggle, SaveTool, MultiChoice
from bokeh.models.widgets import Panel, Tabs
from bokeh.layouts import column, row
from bokeh.events import ButtonClick, Pan, MouseEnter, RangesUpdate
from bokeh.plotting import figure, show
from bokeh.io import push_notebook, output_notebook

# for organizing input spatio-molecular data 

def dictionary_for_data(filename, x_coordinates, y_coordinates, clusters='none'):

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


def creating_required_number_of_input_dictionaries(file_names, x_coordinate_column_names,
                                                  y_coordinate_column_names, clusters_column_names, total_tabs):

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
                                                                                                              clusters_column_names[i])

        list_for_all_data_types.append(dictionary_for_each_DATA)
        list_for_storing_total_clusters_info_in_each_file.append(total_clus)
        list_for_storing_max_x_coordinate_of_each_file.append(max_x_data)
        list_for_storing_max_y_coordinate_of_each_file.append(max_y_data)
        list_for_storing_average_of_x_coordinated_of_each_file.append(avg_xcoord)
        list_for_storing_average_of_y_coordinated_of_each_file.append(avg_ycoord)

    return list_for_all_data_types, list_for_storing_total_clusters_info_in_each_file, list_for_storing_max_x_coordinate_of_each_file, list_for_storing_max_y_coordinate_of_each_file, list_for_storing_average_of_x_coordinated_of_each_file, list_for_storing_average_of_y_coordinated_of_each_file 


# work space for the manual alignment tool

def manual_alignment_tool_work_space(total_tabs, list_for_all_data_types, 
                                         list_for_storing_total_clusters_info_in_each_file, 
                                         list_for_storing_max_x_coordinate_of_each_file, 
                                         list_for_storing_max_y_coordinate_of_each_file, 
                                         list_for_storing_average_of_x_coordinated_of_each_file, 
                                         list_for_storing_average_of_y_coordinated_of_each_file, 
                                         imgs, title):

    tabs = []
    dict_for_multichoice = {}
    dict_for_multichoice["multichoice"] = []

    dict_for_toggle_vert = {}
    dict_for_toggle_vert["toggle_buttons"] = []

    dict_for_toggle_hori = {}
    dict_for_toggle_hori["toggle_buttons"] = []

    dict_for_image_save_button = {}
    dict_for_image_save_button["save_buttons"] = []
    
    dict_for_point_size = {}
    dict_for_point_size["sliders"] = []
    dict_for_point_size["spinners"] = []

    dict_for_data_pixel_size = {}
    dict_for_data_pixel_size["sliders"] = []
    dict_for_data_pixel_size["spinners"] = []

    dict_for_he_pixel_size = {}
    dict_for_he_pixel_size["sliders"] = []
    dict_for_he_pixel_size["spinners"] = []

    dict_for_he_rot_angle = {}
    dict_for_he_rot_angle["sliders"] = []
    dict_for_he_rot_angle["spinners"] = []

    dict_for_img_number = {}
    dict_for_img_number["sliders"] = []
    dict_for_img_number["spinners"] = []

    dict_for_data_rot_angle = {}
    dict_for_data_rot_angle["sliders"] = []
    dict_for_data_rot_angle["spinners"] = []

    dict_for_data_save_button = {}
    dict_for_data_save_button["save_buttons"] = []

    dict_of_coordinates_for_source_final = {}
    dict_of_coordinates_for_source_final["xcoord"] = {}
    dict_of_coordinates_for_source_final["ycoord"] = {}

    dict_of_factors_for_data_resize = {}
    dict_of_factors_for_data_resize["numerators"] = {}
    dict_of_factors_for_data_resize["denominators"] = {}

    dict_for_scale_bar_pixel_size = {}
    dict_for_scale_bar_pixel_size["sliders"] = []
    dict_for_scale_bar_pixel_size["spinners"] = []

    dict_for_active_array = {}
    dict_for_renderers = {}
    dict_of_sources = {}

    list_for_columndatasource_of_data_resize = []
    list_for_rotation_values = []
    list_for_data_table = []
    list_for_draw_tool = []
    list_of_source_final = []
    spinners_for_all_data_point_size = []
    spinners_for_all = []

    div_cluster_heading = []
    div_preview_imgs = []
    div_table_heading = []
    div_orientation = []
    div_px_size = []
    div_rot_angle = []

    div4space1 = [] 
    div4space2 = []
    div4space3 = [] 
    div4space4 = []
    div4space5 = []
    div4space6 = []

    uris = []
    divs_of_imgs = []

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
        dict_of_factors_for_data_resize["numerators"][number_of_tab].append(1)
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
            num.append(1)
            den.append(1)
        division_factor_for_resize_he = ColumnDataSource(data=dict(x=num, y=den))

        division_factor_for_resize_scale_bar = ColumnDataSource(data=dict(x=[1], y=[1]))

        width_of_images=[]
        height_of_images=[]
        for i in imgs:
            image = Image.open(i)
            width, height = image.size
            width_of_images.append(width)
            height_of_images.append(height)

        xmax_overall = max(width_of_images)
        ymax_overall = max(height_of_images)

        if number_of_tab == 0:
            visibility = True
        else:
            visibility = False

        df = pd.DataFrame(uris, columns=['imgs'])
        source_img = ColumnDataSource(df)
        
        df_2 = pd.DataFrame(imgs, columns=['imgs'])
        source_img_2 = ColumnDataSource(df_2)

        max_value = max(list_for_storing_max_x_coordinate_of_each_file[number_of_tab], 
                        list_for_storing_max_y_coordinate_of_each_file[number_of_tab], 
                        xmax_overall, ymax_overall)
        p = figure(x_range=(0, max_value), y_range=(0, max_value), tools=[], title='Manual Alignment Tool')
        im = p.image_url(url=[source_img.data['imgs'][0]], 
                         x=width_of_images[0]/2, 
                         y=height_of_images[0]/2, 
                         w=width_of_images[0], 
                         h=height_of_images[0], 
                         anchor='center', angle_units='rad', angle=0)
        p.add_tools(WheelZoomTool(), BoxSelectTool(dimensions="both"), 
                    PanTool(dimensions="both"), LassoSelectTool(), SaveTool())

        my_arrow = Arrow(end=OpenHead(size=10), start=OpenHead(size=10), line_color="black", visible=False,
                         x_start=max_value-1500, y_start=600, x_end=max_value-500, y_end=600, line_alpha=1,line_width=2)
        p.add_layout(my_arrow)

        labels = Label(x=max_value-1500, y=600, x_offset=15, y_offset=-30, x_units='data', y_units='data', 
                       text='1 mm', render_mode='css',
                       border_line_color='black', border_line_alpha=1.0,
                       background_fill_color='white', background_fill_alpha=1.0,
                       text_font_size='10px', visible=False)

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

        dict_for_multichoice["multichoice"].append(MultiChoice(value=list_for_storing_total_clusters_info_in_each_file[number_of_tab], 
                                                        options=list_for_storing_total_clusters_info_in_each_file[number_of_tab],
                                                        visible=visibility, default_size = 600))

        # image gallery
        dict_for_img_number["sliders"].append(Slider(start=0, end=10, value=0, step=1, title="Image-Number",
                                                     visible=False))
        dict_for_img_number["spinners"].append(Spinner(title="Image Number:", low=0, high=len(imgs)-1, 
                                                      step=1, value=0, width=200, visible=visibility))

        # pixel size for h&e image
        dict_for_he_pixel_size["sliders"].append(Slider(start=0.01, end=3, value=1, step=0.01, 
                                                        title="Pixel Size (in microns/pixel) for H&E image (lowest: 0.01, highest: 3):",
                                                        visible=False))
        dict_for_he_pixel_size["spinners"].append(Spinner(title="H&E Image:", 
                                                         low=0.01, high=3, step=0.01, value=1, 
                                                          width=200, visible=visibility))

        # for modifying data point size
        spinners_for_all_data_point_size.append(Spinner(title="Data Point Size (lowest: 0.06, highest: 10):", 
                          low=0.06, high=10, step=0.001, value=0.09, width=200, visible=visibility))

        # rotation for data
        dict_for_data_rot_angle["sliders"].append(Slider(start=-360, end=360, value=0, 
                                                         step=1, title="Rotation Angle for Data (in degrees) (lowest: -360, highest: 360):",
                                                        visible=False))
        dict_for_data_rot_angle["spinners"].append(Spinner(title="Data:", 
                           low=-360, high=360, step=1, value=0, width=200, visible=visibility))

        # pixel size for data
        dict_for_data_pixel_size["sliders"].append(Slider(start=0.01, end=3, value=1, step=0.01, 
                                                          title="Pixel Size for Data (in um/px) (lowest: 0.01, highest: 3):",visible=False))
        dict_for_data_pixel_size["spinners"].append(Spinner(title="Data:",
                                                            low=0.01, high=3, step=0.01, value=1, width=200
                                                           ,visible=visibility))

        # pixel size for scale bar
        dict_for_scale_bar_pixel_size["sliders"].append(Slider(start=0.01, end=3, value=1, step=0.01, 
                                                          title="Pixel Size for Scale Bar (in um/px) (lowest: 0.01, highest: 3):",visible=False))
        dict_for_scale_bar_pixel_size["spinners"].append(Spinner(title="Display Scale:",
                                                            low=0.01, high=3, step=0.01, value=1, width=200
                                                           ,visible=visibility))        

        # for changing orientation of data
        dict_for_toggle_vert["toggle_buttons"].append(Toggle(label="Flip around Vertical Plane", button_type="success",
                                                            visible=visibility))

        dict_for_toggle_hori["toggle_buttons"].append(Toggle(label="Flip around Horizontal Plane", button_type="success",
                                                            visible=visibility))

        # for saving modified coordinates
        dict_for_data_save_button["save_buttons"].append(Button(label="Download Updated X-Y Coordinates", 
                                                                button_type="success",width=430,visible=visibility))

        # rotation for h&e image
        dict_for_he_rot_angle["sliders"].append(Slider(start=-360, end=360, 
                                                       value=0, step=1, title="Image-Rotation in degrees (lowest: -360, highest: 360)",visible=False))
        dict_for_he_rot_angle["spinners"].append(Spinner(title="H&E Image:", 
                                                         low=-360, high=360, step=1, value=0, width=200,visible=visibility))
        
        
        dict_for_image_save_button["save_buttons"].append(Button(label="Download Updated Image", button_type="success",
                                                                 width = 430, visible=visibility))
        
        
        # callbacks
        dict_for_multichoice["callback"] = CustomJS(args=dict(renderers=dict_for_renderers[number_of_tab],
                                                             multichoice=dict_for_multichoice["multichoice"][number_of_tab], 
                                                             table=list_for_data_table[number_of_tab],
                                                             all_clusters = list_for_storing_total_clusters_info_in_each_file[number_of_tab]),
                            code=""" 

            var xval = table.source.data['x'];
            var yval = table.source.data['y'];
            var selected_vals = multichoice.value;

            for (var i = 0; i < renderers.length; i++){
                renderers[i].glyph.fill_alpha=0;
                renderers[i].glyph.line_alpha=0;
                renderers[i].selection_glyph.fill_alpha=0;
                renderers[i].selection_glyph.line_alpha=0;}

            var j=0;
            for (var i = 0; i < selected_vals.length; i++){
            for (var h = 0; h < all_clusters.length; h++){
             if (all_clusters[h] == selected_vals[i]){

             renderers[h].glyph.fill_alpha=1;
             renderers[h].glyph.line_alpha=1;
             renderers[h].selection_glyph.fill_alpha=1;
             renderers[h].selection_glyph.line_alpha=1;

              for (var z = 0; z < renderers[h].data_source.data['x'].length; z++){
                  xval[j] = renderers[h].data_source.data['x'][z];
                  yval[j] = renderers[h].data_source.data['y'][z];
                  j++;

             }}}}

             if (j < xval.length){
             for (j; j < xval.length; j++){
             xval[j] = 'NaN';
             yval[j] = 'NaN';}
             }

             table.change.emit();
        """)
        dict_for_multichoice["multichoice"][number_of_tab].js_on_change('value', dict_for_multichoice["callback"])

        dict_for_img_number["callback"] = CustomJS(args=dict(width_of_images=width_of_images,
                                       height_of_images=height_of_images, 
                                       px_size=dict_for_he_pixel_size["sliders"][number_of_tab], 
                                       source=source_img,
                                       im=im, 
                                       image_number = dict_for_img_number["sliders"][number_of_tab], 
                                       division_factor_for_resize_he=division_factor_for_resize_he,
                                       division_factor_for_resize_scale_bar=division_factor_for_resize_scale_bar,
                                       scale_bar_px_size = dict_for_scale_bar_pixel_size["sliders"][number_of_tab]),
                            code="""
                            const P = px_size.value;
                            const N = image_number.value;
                            const S = scale_bar_px_size.value;

                            var num_fac_scale_bar = division_factor_for_resize_scale_bar.data['x'];
                            var den_fac_scale_bar = division_factor_for_resize_scale_bar.data['y'];
                            var resize_fac_scale_bar = num_fac_scale_bar[0]/den_fac_scale_bar[0];
                            //num_fac_scale_bar[0] = 1;
                            //den_fac_scale_bar[0] = S;

                            im.data_source.data['url'] = [source.data['imgs'][N]];
                            im.data_source.change.emit();

                            var num_fac = division_factor_for_resize_he.data['x'];
                            var den_fac = division_factor_for_resize_he.data['y'];
                            var resize_fac = num_fac[N]/den_fac[N];
                            num_fac[N] = P;
                            den_fac[N] = 1;

                            width_of_images[N] = (width_of_images[N] / P) * resize_fac * resize_fac_scale_bar * S;
                            height_of_images[N] = (height_of_images[N] / P) * resize_fac * resize_fac_scale_bar * S;

                            im.glyph.x = width_of_images[N]/2;
                            im.glyph.y = height_of_images[N]/2;
                            im.glyph.w = width_of_images[N];
                            im.glyph.h = height_of_images[N];
                            im.glyph.anchor = 'center';

                            im.glyph.change.emit();
                            division_factor_for_resize_he.change.emit();
                            division_factor_for_resize_scale_bar.change.emit();
        """)

        dict_for_scale_bar_pixel_size["spinners"][number_of_tab].js_link('value', dict_for_scale_bar_pixel_size["sliders"][number_of_tab], 'value')
        dict_for_scale_bar_pixel_size["sliders"][number_of_tab].js_link('value', dict_for_scale_bar_pixel_size["spinners"][number_of_tab], 'value')
        dict_for_scale_bar_pixel_size["sliders"][number_of_tab].js_on_change('value', dict_for_img_number["callback"])

        dict_for_img_number["spinners"][number_of_tab].js_link('value', dict_for_img_number["sliders"][number_of_tab], 'value')
        dict_for_img_number["sliders"][number_of_tab].js_link('value', dict_for_img_number["spinners"][number_of_tab], 'value')
        dict_for_img_number["sliders"][number_of_tab].js_on_change('value', dict_for_img_number["callback"])

        dict_for_he_pixel_size["spinners"][number_of_tab].js_link('value', dict_for_he_pixel_size["sliders"][number_of_tab], 'value')
        dict_for_he_pixel_size["sliders"][number_of_tab].js_link('value', dict_for_he_pixel_size["spinners"][number_of_tab], 'value')
        dict_for_he_pixel_size["sliders"][number_of_tab].js_on_change('value', dict_for_img_number["callback"])

        for i in dict_for_renderers[number_of_tab]:
            spinners_for_all.append(spinners_for_all_data_point_size[number_of_tab].js_link('value', i.glyph, 'size'))

        dict_for_data_rot_angle["callback"] = CustomJS(args=dict(table=list_for_data_table[number_of_tab], 
                                            renderers=dict_for_renderers[number_of_tab], 
                                      rot=dict_for_data_rot_angle["sliders"][number_of_tab],
                                     rotation_values=list_for_rotation_values[number_of_tab]),
                            code="""
            const V = rot.value;
            var rotval = rotation_values.data['rotval'];
            const A = V - rotval[0];
            const radians = (Math.PI / 180) * A;

            const cos = Math.cos(radians);
            const sin = Math.sin(radians);

            var x = table.source.data['x'];
            var y = table.source.data['y'];
            var x_clean = [];
            var y_clean = [];

            for (var i = 0; i < x.length; i++){
            if (x[i] != 'NaN'){
            x_clean[i]=x[i];
            y_clean[i]=y[i]; }}

            var w = rotation_values.data['x'];
            var h = rotation_values.data['y'];

            var X=0;
            var Y=0;
            var x_rot = [];
            var y_rot = [];
            for (var i = 0; i < x_clean.length; i++) {
                X= x_clean[i];
                Y= y_clean[i];
                x[i] = ((X-w[0])*cos) - ((Y-h[0])*sin) + w[0];
                y[i] = ((X-w[0])*sin) + ((Y-h[0])*cos) + h[0]; 
                x_rot[i] = x[i];
                y_rot[i] = y[i];
                }

            for (const i of renderers){
            var xval= i.data_source.data['x'];
            var yval= i.data_source.data['y'];

            var X=0;
            var Y=0;
            for (var z = 0; z < xval.length; z++){
                  X= xval[z];
                  Y= yval[z];
                  xval[z] = ((X-w[0])*cos) - ((Y-h[0])*sin) + w[0];
                  yval[z] = ((X-w[0])*sin) + ((Y-h[0])*cos) + h[0];}

            i.data_source.change.emit();}

            let x_sum = 0;
            let y_sum = 0;
            for (let i = 0; i < x_rot.length; i++) {
                x_sum += x_rot[i];
                y_sum += y_rot[i];
            }
            table.change.emit();
            rotval[0] = V;    
        """)

        dict_for_data_pixel_size["callback"] = CustomJS(args=dict(renderers=dict_for_renderers[number_of_tab], 
                                            table=list_for_data_table[number_of_tab], 
                                            size=dict_for_data_pixel_size["sliders"][number_of_tab], 
                                            division_factor_for_resize=list_for_columndatasource_of_data_resize[number_of_tab],
                                            rotation_values=list_for_rotation_values[number_of_tab],
                                            division_factor_for_resize_scale_bar=division_factor_for_resize_scale_bar,
                                            scale_bar_px_size = dict_for_scale_bar_pixel_size["sliders"][number_of_tab],
                                            image_number = dict_for_img_number["sliders"][number_of_tab]),
                            code="""
            const F = size.value;
            var num_fac = division_factor_for_resize.data['x'];
            var den_fac = division_factor_for_resize.data['y'];
            const N = image_number.value;

            var resize_fac = num_fac[0] / den_fac[0];

            const S = scale_bar_px_size.value;

            var num_fac_scale_bar = division_factor_for_resize_scale_bar.data['x'];
            var den_fac_scale_bar = division_factor_for_resize_scale_bar.data['y'];
            var resize_fac_scale_bar = num_fac_scale_bar[0]/den_fac_scale_bar[0];

            var x = table.source.data['x'];
            var y = table.source.data['y'];

            var x_clean = [];
            var y_clean = [];

            for (var i = 0; i < x.length; i++){
            if (x[i] != 'NaN'){
            x_clean[i]=x[i];
            y_clean[i]=y[i];}}

            var w = rotation_values.data['x'];
            var h = rotation_values.data['y'];
            let x_sum = 0;
            let y_sum = 0;

            var X=0;
            var Y=0;
            for (var i = 0; i < x_clean.length; i++){
                X= x_clean[i];
                Y= y_clean[i];
                x[i] = (X / F) * resize_fac * resize_fac_scale_bar * S;
                y[i] = (Y / F) * resize_fac * resize_fac_scale_bar * S;
                x_sum += x[i];
                y_sum += y[i];
                }        
            table.change.emit();

            w[0] = x_sum/x_clean.length;
            h[0] = y_sum/y_clean.length;
            rotation_values.change.emit();

            for (const i of renderers){
            var xval= i.data_source.data['x'];
            var yval= i.data_source.data['y'];

            for (var z = 0; z < xval.length; z++){
                  X= xval[z];
                  Y= yval[z];
                  xval[z] = (X / F) * resize_fac * resize_fac_scale_bar * S;
                  yval[z] = (Y / F) * resize_fac * resize_fac_scale_bar * S;}

            i.data_source.change.emit();}

            num_fac[0] = F;
            den_fac[0] = 1;

            num_fac_scale_bar[0] = 1;
            den_fac_scale_bar[0] = S;

            division_factor_for_resize.change.emit();
            division_factor_for_resize_scale_bar.change.emit();

        """)

        dict_for_he_rot_angle["callback"] = CustomJS(args=dict(im = im, rotval_for_img=dict_for_he_rot_angle["sliders"][number_of_tab]),
                            code="""
                            const radians = (Math.PI / 180) * rotval_for_img.value;
                            im.glyph.angle = radians;  
                            im.change.emit();
        """)

        dict_for_data_rot_angle["sliders"][number_of_tab].js_on_change('value', dict_for_data_pixel_size["callback"])
        dict_for_data_rot_angle["sliders"][number_of_tab].js_on_change('value', dict_for_data_rot_angle["callback"])
        dict_for_data_pixel_size["sliders"][number_of_tab].js_on_change('value', dict_for_data_pixel_size["callback"])
        dict_for_he_rot_angle["sliders"][number_of_tab].js_on_change('value', dict_for_he_rot_angle["callback"])

        dict_for_scale_bar_pixel_size["sliders"][number_of_tab].js_on_change('value', dict_for_data_pixel_size["callback"])

        dict_for_data_rot_angle["spinners"][number_of_tab].js_link('value', dict_for_data_rot_angle["sliders"][number_of_tab], 'value')
        dict_for_data_rot_angle["sliders"][number_of_tab].js_link('value', dict_for_data_rot_angle["spinners"][number_of_tab], 'value')
        dict_for_data_pixel_size["spinners"][number_of_tab].js_link('value', dict_for_data_pixel_size["sliders"][number_of_tab], 'value')
        dict_for_data_pixel_size["sliders"][number_of_tab].js_link('value', dict_for_data_pixel_size["spinners"][number_of_tab], 'value')
        dict_for_he_rot_angle["spinners"][number_of_tab].js_link('value', dict_for_he_rot_angle["sliders"][number_of_tab], 'value')
        dict_for_he_rot_angle["sliders"][number_of_tab].js_link('value', dict_for_he_rot_angle["spinners"][number_of_tab], 'value')

        dict_for_toggle_vert["toggle_buttons"][number_of_tab].js_on_click(CustomJS(args=dict(rotation_values=list_for_rotation_values[number_of_tab],
                                      renderers=dict_for_renderers[number_of_tab], 
                                        table=list_for_data_table[number_of_tab]), code="""
            var x = table.source.data['x'];
            var y = table.source.data['y'];

            var w = rotation_values.data['x'];
            var h = rotation_values.data['y'];
            var rotval = rotation_values.data['rotval'];

            var x_clean = [];
            var y_clean = [];

            for (var i = 0; i < x.length; i++){
            if (x[i] != 'NaN'){
            x_clean[i]=x[i];
            y_clean[i]=y[i];
            }}

            let x_sum = 0;
            let y_sum = 0;

            if (rotval[0] == 0){
            for (var i = 0; i < x_clean.length; i++){
            x[i] = w[0] + (w[0] - x_clean[i]);
            x_sum += x[i];
            y_sum += y[i];
            }}

            if (rotval[0] > 0){
            for (var i = 0; i < x_clean.length; i++){
            x[i] = h[0] + (h[0] - y_clean[i]);
            y[i] = w[0] + (w[0] - x_clean[i]);
            x_sum += x[i];
            y_sum += y[i];
            }}

            if (rotval[0] < 0){
            for (var i = 0; i < x_clean.length; i++){
            x[i] = h[0] + (h[0] - y_clean[i]);
            y[i] = w[0] + (w[0] - x_clean[i]);
            x_sum += x[i];
            y_sum += y[i];
            }}

            for (const i of renderers){
            var xval= i.data_source.data['x'];
            var yval= i.data_source.data['y'];

            if (rotval[0] == 0){
            for (var z = 0; z < xval.length; z++){
                  xval[z] = w[0] + (w[0] - xval[z]); 
            }}

            if (rotval[0] > 0) {
            var X=0;
            var Y=0;
            for (var z = 0; z < xval.length; z++){
            X=xval[z];
            Y=yval[z];
            xval[z] = h[0] + (h[0] - Y);
            yval[z] = w[0] + (w[0] - X);
            }}

            if (rotval[0] < 0){
            var X=0;
            var Y=0;
            for (var z = 0; z < xval.length; z++){
            X=xval[z];
            Y=yval[z];
            xval[z] = h[0] + (h[0] - Y);
            yval[z] = w[0] + (w[0] - X);
            }}

            i.data_source.change.emit();
            }

            w[0] = x_sum/x_clean.length;
            h[0] = y_sum/y_clean.length; 
            table.change.emit();
        """))

        dict_for_toggle_hori["toggle_buttons"][number_of_tab].js_on_click(CustomJS(args=dict(rotation_values=list_for_rotation_values[number_of_tab],
                                      renderers=dict_for_renderers[number_of_tab], 
                                      table=list_for_data_table[number_of_tab]), code="""
            var x = table.source.data['x'];
            var y = table.source.data['y'];

            var w = rotation_values.data['x'];
            var h = rotation_values.data['y'];
            var rotval = rotation_values.data['rotval'];

            var x_clean = [];
            var y_clean = [];

            for (var i = 0; i < x.length; i++){
            if (x[i] != 'NaN'){
            x_clean[i]=x[i];
            y_clean[i]=y[i];
            }}

            let x_sum = 0;
            let y_sum = 0;

            if (rotval[0] == 0){
            for (var i = 0; i < x_clean.length; i++){
            y[i] = h[0] + (h[0] - y_clean[i]);
            x_sum += x[i];
            y_sum += y[i];
            }}

            if (rotval[0] > 0){
            for (var i = 0; i < x_clean.length; i++){
            x[i] = w[0] + (w[0] - x_clean[i]);
            y[i] = h[0] + (h[0] - y_clean[i]);
            x_sum += x[i];
            y_sum += y[i];
            }}

            if (rotval[0] < 0){
            for (var i = 0; i < x_clean.length; i++){
            x[i] = w[0] + (w[0] - x_clean[i]);
            y[i] = h[0] + (h[0] - y_clean[i]);
            x_sum += x[i];
            y_sum += y[i];
            }}

            for (const i of renderers){
            var xval= i.data_source.data['x'];
            var yval= i.data_source.data['y'];

            if (rotval[0] == 0){
            for (var z = 0; z < xval.length; z++){
                  yval[z] = h[0] + (h[0] - yval[z]);     
            }} 

            if (rotval[0] > 0) {
            for (var z = 0; z < xval.length; z++){
            xval[z] = w[0] + (w[0] - xval[z]);
            yval[z] = h[0] + (h[0] - yval[z]);
            }}

            if (rotval[0] < 0){
            for (var z = 0; z < xval.length; z++){
            xval[z] = w[0] + (w[0] - xval[z]);
            yval[z] = h[0] + (h[0] - yval[z]);
            }}

            i.data_source.change.emit();
            }

            w[0] = x_sum/x_clean.length;
            h[0] = y_sum/y_clean.length;
            table.change.emit();
        """))

        dict_for_data_save_button["save_buttons"][number_of_tab].js_on_event(ButtonClick, CustomJS(
            args=dict(source_data=list_of_source_final[number_of_tab], 
                     angle=dict_for_he_rot_angle["sliders"][number_of_tab],
                     number=dict_for_img_number["sliders"][number_of_tab],
                    px_size=dict_for_he_pixel_size["sliders"][number_of_tab], source_img=source_img,
                     width_of_images=width_of_images, height_of_images=height_of_images),
            code="""

                // for saving a .csv file containing updated x-y coordinates

                var data = source_data.data;
                var x = data['x'];
                var y = data['y'];

                var out = "x,y\\n";

                for (var i = 0; i < x.length; i++) {
                if (data['x'][i] != 'NaN'){
                    out += data['x'][i] + "," + data['y'][i] + "\\n";
                }}
                var file = new Blob([out], {type: 'text/plain'});
                var elem = window.document.createElement('a');
                elem.href = window.URL.createObjectURL(file);
                elem.download = 'Updated_Data.csv';
                document.body.appendChild(elem);
                elem.click();
                document.body.removeChild(elem);           
                """
        ))

        def image_download(angle=dict_for_he_rot_angle["sliders"][number_of_tab],
                     number=dict_for_img_number["sliders"][number_of_tab],
                    px_size=dict_for_he_pixel_size["sliders"][number_of_tab], source_img=source_img_2,
                     width_of_images=width_of_images, height_of_images=height_of_images,
                    division_factor_for_resize_he=division_factor_for_resize_he,
                    division_factor_for_resize_scale_bar=division_factor_for_resize_scale_bar,
                    scale_bar_px_size = dict_for_scale_bar_pixel_size["sliders"][number_of_tab]):

            P = px_size.value
            N = number.value
            S = scale_bar_px_size.value

            num_fac_scale_bar = division_factor_for_resize_scale_bar.data['x']
            den_fac_scale_bar = division_factor_for_resize_scale_bar.data['y']
            resize_fac_scale_bar = num_fac_scale_bar[0]/den_fac_scale_bar[0]

            num_fac = division_factor_for_resize_he.data['x']
            den_fac = division_factor_for_resize_he.data['y']
            resize_fac = num_fac[N]/den_fac[N]

            image = Image.open(source_img.data['imgs'][number.value])
            width, height = image.size

            new_width = (width_of_images[N] / P) * resize_fac * resize_fac_scale_bar * S
            new_height = (height_of_images[N] / P) * resize_fac * resize_fac_scale_bar * S
            
            image = image.resize((round(new_width), round(new_height)),
                                 Image.Resampling.BICUBIC)
            image = image.rotate(angle.value, Image.Resampling.NEAREST, expand = 1, fillcolor = (255,255,255))
            
            image.save(os.path.join(str(Path.home() / "Downloads")+"\\"+"Updated_H&E_Image.jpg"))

        dict_for_image_save_button["save_buttons"][number_of_tab].on_click(image_download)

        callback_for_scale_bar = CustomJS(args=dict(my_arrow=my_arrow, labels=labels, p=p,
                                    scale_bar_px_size = dict_for_scale_bar_pixel_size["sliders"][number_of_tab]),
                                 code="""

                const Size = scale_bar_px_size.value;
                const S = Size * 1000; // 1000 for 1000 pixels

                my_arrow.x_end = p.x_range.end - 500;
                my_arrow.x_start = p.x_range.end - (500+S);
                my_arrow.y_end = p.y_range.start + 600;
                my_arrow.y_start = p.y_range.start + 600;
                my_arrow.visible = true;

                labels.x = p.x_range.end - (500+S);
                labels.y = p.y_range.start + 600;
                labels.text = `${Size} mm`;
                labels.x_offset = 15 * Size;
                labels.visible = true;

                my_arrow.change.emit();
                labels.change.emit();
                """)

        p.js_on_event(RangesUpdate, callback_for_scale_bar)
        p.js_on_event('pan', dict_for_multichoice["callback"])
        p.js_on_event('pan', dict_for_data_pixel_size["callback"])
        p.js_on_event('mouseenter', dict_for_data_pixel_size["callback"])

        dict_for_scale_bar_pixel_size["sliders"][number_of_tab].js_on_change('value',  callback_for_scale_bar)

        div_orientation.append(Div(text="""Change Orientation of Data:""", visible = visibility, height=15))
        div_table_heading.append(Div(text="""Updated X-Y Coordinates: """, visible = visibility, height=15))
        div_preview_imgs.append(Div(text="""Preview of Images: """, visible = visibility, height=15))
        div_px_size.append(Div(text="""Pixel Size (in um/px) Range: 0.01 to 3 =""", visible = visibility, height=15))
        div_rot_angle.append(Div(text="""Rotation Angle (in degrees) Range: -360 to 360 =""", visible = visibility, height=15))

        div4space1.append(Div(text="""""", visible = visibility))
        div4space2.append(Div(text="""""", visible = visibility))
        div4space3.append(Div(text="""""", visible = visibility))
        div4space4.append(Div(text="""""", visible = visibility, height=10))
        div4space5.append(Div(text="""""", visible = visibility, height=10))
        div4space6.append(Div(text="""""", visible = visibility))
                
        tabs.append(Panel(child=p, title=title[number_of_tab]))
    
    tabs = Tabs(tabs = tabs)   

    callback_for_tabs = CustomJS(args=dict(tabs = tabs, total_tabs = total_tabs,
                                      multichoice = dict_for_multichoice["multichoice"],
                                      vertical_toggle = dict_for_toggle_vert["toggle_buttons"],
                                      horizontal_toggle = dict_for_toggle_hori["toggle_buttons"],
                                      data_px_size = dict_for_data_pixel_size["spinners"],
                                      data_rot_angle = dict_for_data_rot_angle["spinners"],
                                      data_table = list_for_data_table,
                                      save_buttons = dict_for_data_save_button["save_buttons"],
                                      data_point_size = spinners_for_all_data_point_size,
                                      he_px_size = dict_for_he_pixel_size["spinners"],
                                      he_rot_angle = dict_for_he_rot_angle["spinners"],
                                      he_number = dict_for_img_number["spinners"],
                                      scale_bar_px_size =  dict_for_scale_bar_pixel_size["spinners"],
                                      image_save_buttons = dict_for_image_save_button["save_buttons"],
                                      div_cluster_heading = div_cluster_heading, 
                                      div_preview_imgs = div_preview_imgs, 
                                      div_table_heading = div_table_heading, 
                                      div_px_size = div_px_size,
                                      div4space1 = div4space1, div4space2 = div4space2,
                                      div_rot_angle = div_rot_angle, div4space3 = div4space3,
                                      div4space4 = div4space4,
                                      div4space5 = div4space5,
                                      div4space6 = div4space6,
                                      div_orientation = div_orientation), code="""

    for (var j=0; j < total_tabs.length; j++){

    multichoice[j].visible=false;
    vertical_toggle[j].visible=false;
    horizontal_toggle[j].visible=false;
    data_px_size[j].visible=false;
    data_rot_angle[j].visible=false;
    data_table[j].visible=false;
    save_buttons[j].visible=false;
    data_point_size[j].visible=false;
    he_px_size[j].visible=false;
    he_rot_angle[j].visible=false;
    he_number[j].visible=false;
    div_cluster_heading[j].visible=false;
    div_preview_imgs[j].visible=false;
    div_table_heading[j].visible=false;
    div_px_size[j].visible=false;
    div4space1[j].visible=false;
    div4space2[j].visible=false;
    div_rot_angle[j].visible=false;
    div4space3[j].visible=false;
    div4space4[j].visible=false;
    div4space5[j].visible=false;
    div4space6[j].visible=false;
    div_orientation[j].visible=false;
    scale_bar_px_size[j].visible=false;
    image_save_buttons[j].visible=false;
    }

    for (var j=0; j < total_tabs.length; j++){

    if (tabs.active == j){

    multichoice[j].visible=true;
    vertical_toggle[j].visible=true;
    horizontal_toggle[j].visible=true;
    data_px_size[j].visible=true;
    data_rot_angle[j].visible=true;
    data_table[j].visible=true;
    save_buttons[j].visible=true;
    data_point_size[j].visible=true;
    he_px_size[j].visible=true;
    he_rot_angle[j].visible=true;
    he_number[j].visible=true;
    div_cluster_heading[j].visible=true;
    div_preview_imgs[j].visible=true;
    div_table_heading[j].visible=true;
    div_px_size[j].visible=true;
    div4space1[j].visible=true;
    div4space2[j].visible=true;
    div_rot_angle[j].visible=true;
    div4space3[j].visible=true;
    div4space4[j].visible=true;
    div4space5[j].visible=true;
    div4space6[j].visible=true;
    div_orientation[j].visible=true;
    scale_bar_px_size[j].visible=true;
    image_save_buttons[j].visible=true;
    }
    if (tabs.active != j) {

    multichoice[j].visible=false;
    vertical_toggle[j].visible=false;
    horizontal_toggle[j].visible=false;
    data_px_size[j].visible=false;
    data_rot_angle[j].visible=false;
    data_table[j].visible=false;
    save_buttons[j].visible=false;
    data_point_size[j].visible=false;
    he_px_size[j].visible=false;
    he_rot_angle[j].visible=false;
    he_number[j].visible=false;
    div_cluster_heading[j].visible=false;
    div_preview_imgs[j].visible=false;
    div_table_heading[j].visible=false;
    div_px_size[j].visible=false;
    div4space1[j].visible=false;
    div4space2[j].visible=false;
    div_rot_angle[j].visible=false;
    div4space3[j].visible=false;
    div4space4[j].visible=false;
    div4space5[j].visible=false;
    div4space6[j].visible=false;
    div_orientation[j].visible=false;
    scale_bar_px_size[j].visible=false;
    image_save_buttons[j].visible=false;
    }
    }

    """)
    
    tabs.js_on_change('active', callback_for_tabs)
        
    layout_for_display = row(column(tabs, row(div4space1), 
         row(row(div_table_heading), row(div4space3), row(dict_for_data_save_button["save_buttons"])), 
         row(list_for_data_table)), column(row(div_cluster_heading), 
         row(dict_for_multichoice["multichoice"]), row(div_orientation), 
         row(row(dict_for_toggle_vert["toggle_buttons"]), row(dict_for_toggle_hori["toggle_buttons"])), 
         row(div4space2), row(spinners_for_all_data_point_size), 
         row(div4space5),       
         row(div_px_size),
         row(row(dict_for_data_pixel_size["spinners"]), row(dict_for_he_pixel_size["spinners"]), row(dict_for_scale_bar_pixel_size["spinners"])), 
         row(div4space4), 
         row(div_rot_angle),
         row(row(dict_for_data_rot_angle["spinners"]), row(dict_for_he_rot_angle["spinners"])), 
         row(div4space6),
         row(dict_for_img_number["spinners"]), 
         row(div_preview_imgs), row(divs_of_imgs), row(dict_for_image_save_button["save_buttons"])))
    
    return layout_for_display


print("All Modules and Packages have been imported")

