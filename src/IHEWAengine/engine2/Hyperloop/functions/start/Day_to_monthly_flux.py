# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
         UNESCO-IHE 2018
Contact: t.hessels@unesco-ihe.org
Repository: https://github.com/wateraccounting/watools
Module: Function/Start
"""
# Builtins
from __future__ import print_function

import os
import glob
import calendar
# Math
import numpy as np
import pandas as pd
# GIS
try:
    import gdal
except ImportError:
    from osgeo import gdal
# Self
try:
    from ...general import data_conversions as DC
    from ...general import raster_conversions as RC
except ImportError:
    from IHEWAengine.engine2.Hyperloop.general import data_conversions as DC
    from IHEWAengine.engine2.Hyperloop.general import raster_conversions as RC


def Nearest_Interpolate(Dir_in, Startdate, Enddate, Dir_out=None):
    """
    This functions calculates monthly tiff files based on the daily tiff files.
    (will calculate the total sum)

    Parameters
    ----------
    Dir_in : str
        Path to the input data
    Startdate : str
        Contains the start date of the model 'yyyy-mm-dd'
    Enddate : str
        Contains the end date of the model 'yyyy-mm-dd'
    Dir_out : str
        Path to the output data, default is same as Dir_in

    """
    # Change working directory
    os.chdir(Dir_in)

    # Define end and start date
    Dates = pd.date_range(Startdate, Enddate, freq='MS')

    # Find all monthly files
    files = glob.glob('*daily*.tif')

    # Get array information and define projection
    geo_out, proj, size_X, size_Y = RC.Open_array_info(files[0])
    if int(proj.split('"')[-2]) == 4326:
        proj = "WGS84"

    # Get the No Data Value
    dest = gdal.Open(files[0])
    NDV = dest.GetRasterBand(1).GetNoDataValue()

    # Define output directory
    if Dir_out is None:
        Dir_out = Dir_in

    if not os.path.exists(Dir_out):
        os.makedirs(Dir_out)

    # loop over the months and sum the days
    for date in Dates:
        Year = date.year
        Month = date.month
        files_one_year = glob.glob('*daily*%d.%02d*.tif' % (Year, Month))

        # Create empty arrays
        Month_data = np.zeros([size_Y, size_X])

        # Get amount of days in month
        Amount_days_in_month = int(calendar.monthrange(Year, Month)[1])

        if len(files_one_year) is not Amount_days_in_month:
            print("One day is missing!!! month %s year %s" % (Month, Year))

        for file_one_year in files_one_year:
            file_path = os.path.join(Dir_in, file_one_year)

            Day_data = RC.Open_tiff_array(file_path)
            Day_data[np.isnan(Day_data)] = 0.0
            Day_data[Day_data == -9999] = 0.0
            Month_data += Day_data

        # Define output name
        output_name = os.path.join(Dir_out, file_one_year
                                   .replace('daily', 'monthly')
                                   .replace('day', 'month'))

        output_name = output_name[:-14] + '%d.%02d.01.tif' % (date.year, date.month)

        # Save tiff file
        DC.Save_as_tiff(output_name, Month_data, geo_out, proj)

    return
