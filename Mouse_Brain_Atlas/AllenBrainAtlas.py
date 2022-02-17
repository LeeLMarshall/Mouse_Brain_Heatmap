#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 11:52:45 2021

@author: Lee.Marshall
"""

#---------- Packages
from allensdk.api.queries.image_download_api import ImageDownloadApi
from allensdk.api.queries.svg_api import SvgApi
from allensdk.config.manifest import Manifest
import matplotlib.pyplot as plt
from skimage.io import imread
import pandas as pd
import logging
import os
from base64 import b64encode
from IPython.display import HTML, display

#---------- CWD
os.getcwd()
os.chdir('/Volumes/projects_secondary-1/bras/Lee/Image_analysis/Henderson')
os.getcwd()

#---------- Functions
def verify_image(file_path, figsize=(18, 22)):
    image = imread(file_path)
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(image)
    
    
def verify_svg(file_path, width_scale, height_scale):
    # we're using this function to display scaled svg in the rendered notebook.
    # we suggest that in your own work you use a tool such as inkscape or illustrator to view svg
    with open(file_path, 'rb') as svg_file: 
        svg = svg_file.read()
    encoded_svg = b64encode(svg)
    decoded_svg = encoded_svg.decode('ascii')
    st = r'<img class="figure" src="data:image/svg+xml;base64,{}" width={}% height={}%></img>'.format(decoded_svg, width_scale, height_scale)
    display(HTML(st))

#---------- Instance
image_api = ImageDownloadApi()
svg_api = SvgApi()

#---------- Downloading a single Mouse Brain Section image
image_api.download_section_image(section_image_id=70945123, 
                                 file_path='70945123.jpg', 
                                 downsample=3)
verify_image(file_path='70945123.jpg')

#---------- Downloading a single Mouse Connectivity image
ranges = image_api.get_section_image_ranges([297225716])[0]
image_api.download_projection_image(projection_image_id=297225716, 
                                    file_path='297225716_connectivity.jpg', 
                                    downsample=3, 
                                    range=ranges)
verify_image(file_path='297225716_connectivity.jpg')
image_api.download_projection_image(projection_image_id=297225716, 
                                    file_path='297225716_projection.jpg', 
                                    downsample=3, 
                                    projection=True)
verify_image('297225716_projection.jpg')





#---------- Downloading a single atlas image
image_api.download_atlas_image(atlas_image_id=100960037, 
                               file_path='100960037_nissl.jpg', 
                               annotation=False, 
                               downsample=0)
verify_image(file_path='100960037_nissl.jpg')
image_api.download_atlas_image(atlas_image_id=100960037, 
                               file_path='100960037_annotation.jpg', 
                               annotation=True, 
                               downsample=0)
verify_image(file_path='100960037_annotation.jpg')

#---------- Downloading a single atlas svg
svg_api.download_svg(section_image_id=100960037, 
                     file_path='100960037.svg')
verify_svg(file_path='100960037.svg', 
           width_scale=35, 
           height_scale=35)

#---------- Listing images from an atlas (or section data set)
# image_api.section_image_query(section_data_set_id) is the analogous method for section data sets
atlas_image_records = image_api.atlas_image_query(138322605)
# this returns a list of dictionaries. Let's convert it to a pandas dataframe
atlas_image_dataframe = pd.DataFrame(atlas_image_records)
atlas_image_dataframe.head()
atlas_image_dataframe['id'].head()




















