import argparse
import glob
import os
import shutil
import random

import numpy as np
import utils


def split(data_dir):
    """
    Create three splits from the processed records. The files should be moved to new folders in the 
    same directory. This folder should be named train, val and test.

    args:
        - data_dir [str]: data directory, /mnt/data
    """
    # TODO: Implement function
    #As suggested in the lesson, I will pick 75% for training, 15% for validation and 10% for test. Each file is a record, each record must exclusively belong
    #to one for the 3 categories
    list_files = os.listdir(data_dir)
    num_files = len(list_files)
    random.shuffle(list_files)

    #training dataset
    train_path = os.path.join(data_dir,'train')
    os.makedirs(train_path, exist_ok=True)
    for file in list_files[0:int(round(0.75*num_files,0))]:
        shutil.move(os.path.join(data_dir, file), train_path)
    #validation dataset
    val_path = os.path.join(data_dir,'val')
    os.makedirs(val_path, exist_ok=True)   
    for file in list_files[int(round(0.75*num_files,0)):int(round(0.90*num_files,0))]:
        shutil.move(os.path.join(data_dir, file), os.path.join(data_dir,'val', file))
    #create test set
    test_path = os.path.join(data_dir,'test')
    os.makedirs(test_path, exist_ok=True)
    for file in list_files[int(round(0.90*num_files,0)):]:
        shutil.move(os.path.join(data_dir, file), os.path.join(data_dir,'test', file))


if __name__ == "__main__":
    split("/app/project/data/processed")
#     parser = argparse.ArgumentParser(description='Split data into training / validation / testing')
#     parser.add_argument('--data_dir', required=True,
#                         help='data directory')
#     args = parser.parse_args()

#     logger = utils.get_module_logger(__name__)
#     logger.info('Creating splits...')
#     split(args.data_dir)