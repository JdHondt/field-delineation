#
# Copyright (c) Sinergise, 2019 -- 2021.
#
# This file belongs to subproject "field-delineation" of project NIVA (www.niva4cap.eu).
# All rights reserved.
#
# This source code is licensed under the MIT license found in the LICENSE
# file in the root directory of this source tree.
#

import sys
import json
import logging
import argparse
import glob
import re
import os

import geopandas as gpd

# from eolearn.core import EOExecutor
from fd.eoexecution import EOExecutor

from fd.tiffs_to_eopatch import (
    TiffsToEopatchConfig,
    get_tiffs_to_eopatches_workflow,
    get_exec_args)
from fd.utils import LogFileFilter


stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.addFilter(LogFileFilter())
handlers = [stdout_handler]

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s", handlers=handlers
)
LOGGER = logging.getLogger(__name__)


def convert_tiff_to_eopatches(config: dict):
    """ Convert tiffs downloaded through the batch Processing API to EOPatches

    Args:
        config (dict): Configuration dictionary with convertion options
    """

    tiffs_to_eops_config = TiffsToEopatchConfig(
        tiffs_folder=config['tiffs_folder'],
        eopatches_folder=config['eopatches_folder'],
        masks_folder=config['masks_folder'],
        band_names=config['band_names'],
        data_name=config['data_name'],
        mask_name=config['mask_name'],
        is_data_mask=config['is_data_mask'],
        clp_name=config['clp_name'],
        clm_name=config['clm_name']
    )

    # LOGGER.info(f'Read grid definition file {config["grid_filename"]}')
    # grid_definition = gpd.read_file(config['grid_filename'])

    workflow = get_tiffs_to_eopatches_workflow(tiffs_to_eops_config, delete_tiffs=False)

    # eopatch_list = grid_definition.name.values
    # eopatch_list = [str(a) for a in range(100)]
    tiffnames = os.listdir(tiffs_to_eops_config.masks_folder + "/masks")
    eopatch_list = set([re.sub(".tiff", "", name) for name in tiffnames])

    exec_args = get_exec_args(workflow, eopatch_list)

    executor = EOExecutor(workflow, exec_args, save_logs=True, logs_folder='.')

    LOGGER.info('Execute conversion')
    # executor.run(workers=config['max_workers'])
    executor.run(multiprocess=False)

    executor.make_report()
    LOGGER.info(f'Report was saved to location: {executor.get_report_filename()}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert downloaded tiff files into EOPatches.\n")
    parser.add_argument(
        "--config", 
        type=str, 
        help="Path to config file with conversion parameters", 
        required=True
    )
    args = parser.parse_args()

    LOGGER.info(f'Reading configuration from {args.config}')
    with open(args.config, 'r') as jfile:
        cfg_dict = json.load(jfile)

    convert_tiff_to_eopatches(cfg_dict)
