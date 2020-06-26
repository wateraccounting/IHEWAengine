# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
         UNESCO-IHE 2016
Contact: t.hessels@unesco-ihe.org
Repository: https://github.com/wateraccounting/watools
Module: General

Description:
This module consists of the general functions that are used in the WA+ toolbox
"""
from . import data_conversions
from . import raster_conversions
from . import files

from . import parameters

__all__ = ['files', 'parameters', 'data_conversions', 'raster_conversions', ]
