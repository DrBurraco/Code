#!/usr/bin/env python3
import os
from random import randbytes
import zipfile as zf
import io

def read_params():

    file = open('jump_lengths.txt','r')
    jump_lengths = file.read().split(',')
    file.close()

    file = open('sequence_lengths.txt','r')
    sequence_lengths = file.read().split(',')
    file.close()

    return jump_lengths,sequence_lengths

def main():

    """dataset_folder = './dataset_prova'
    file_list = os.listdir(dataset_folder)
    for file in file_list:
        file_path = dataset_folder + '/' + file
        path_to_save = './dataset_low_entropy/'
        jump_length = int(input('Insert jump length: '))"""
    jump_lengths,sequence_lengths = read_params()

    print(jump_lengths,sequence_lengths)
    
    """with zf.ZipFile('NapierOne-tiny.zip', mode='a') as dataset:
        for archive_name in dataset.namelist():
            if ('RANSOMWARE' in archive_name):
                with dataset.open(archive_name) as archive:
                    archive_filedata = io.BytesIO(archive.read())
                    with zf.ZipFile(archive_filedata) as nested_zip:
                        for file_name in nested_zip.namelist():
                            with nested_zip.open(file_name) as file:
                                filedata = file.read()
                                print(filedata)
                        nested_zip.close()
                    archive.close()
        dataset.close() """

    return

if __name__ == "__main__":
    main()