import logging

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from shapely.geometry import Polygon

from fd.scripts.tiffs_to_eopatches import convert_tiff_to_eopatches

logging.getLogger().setLevel(logging.ERROR)

# !! Local folder where project related  files are/will be stored !!  
PROJECT_DATA_ROOT = 'C:/Users/s166909/surfdrive/Documents/3.Werk/0.TUe_Research/0.STELAR/STELAR_VISTA_task3.3/data/AI4BOUNDARIES/sentinel2' 
INPUT_AOI_FILEPATH = os.path.join(PROJECT_DATA_ROOT, 'aoi.geojson') 
GRID_PATH = os.path.join(PROJECT_DATA_ROOT, 'grid.gpkg')

TIME_INTERVAL = ['2022-01-01', '2023-01-01'] # Set the time interval for which the data will be downloaded  

TIFFS_FOLDER = PROJECT_DATA_ROOT + "/images/tiff_files" # Location on the bucket where downloaded TIFF images will be stored
EOPATCHES_FOLDER = PROJECT_DATA_ROOT + "/eopatches" # Location on the bucket to which EOPatches will be saved.
MASKS_FOLDER = PROJECT_DATA_ROOT # Location on the bucket to which EOPatches will be saved.

tiffs_to_eop_config = {
    "grid_filename": GRID_PATH,
    "tiffs_folder": TIFFS_FOLDER,
    "eopatches_folder": EOPATCHES_FOLDER,
    "masks_folder": MASKS_FOLDER,
    "band_names": ["B2", "B3", "B4", "B8"],
    "mask_name": "masks",
    "data_name": "BANDS",
    "is_data_mask": "IS_DATA",
    "clp_name": "CLP",
    "clm_name": "CLM",
    "max_workers": 6
}

convert_tiff_to_eopatches(tiffs_to_eop_config)

# Test
# from eolearn.io import ImportFromTiff
# from eolearn.core import EOPatch, EOTask, FeatureType, EOWorkflow, SaveTask, MergeFeatureTask, RemoveFeature, \
#     RenameFeature, OverwritePermission, LinearWorkflow
# from eolearn.core.fs_utils import get_base_filesystem_and_path
# from sentinelhub import SHConfig, CRS
# from fd.local_io import ImportFromTiff

# band="B2"

# Set up credentials in sh config
# sh_config = SHConfig()

# task = ImportFromTiff((FeatureType.DATA, band),
#                                     folder=TIFFS_FOLDER,
#                                     config=sh_config)

# task.execute()
