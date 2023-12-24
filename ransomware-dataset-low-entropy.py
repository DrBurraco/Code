#!/usr/bin/env python3

import os
import numpy as np
import zipfile as zf
import io

def main():

    jump_lengths = [12,32,44]
    sequence_lengths = [10,20]
    
    with zf.ZipFile('NapierOne-tiny.zip', mode='a') as dataset:
        archive_list = dataset.namelist()
        for archive_name in archive_list:
            if ('RANSOMWARE' in archive_name):
                with dataset.open(archive_name) as archive:
                    archive_filedata = io.BytesIO(archive.read())
                    with zf.ZipFile(archive_filedata, mode='a') as nested_zip:
                        for jump_length in jump_lengths:
                            for sequence_length in sequence_lengths:
                                random_values = io.BytesIO(np.random.bytes(sequence_length))
                                new_zip_file_name = archive_name.replace('.zip', '-JL' + str(jump_length) + '-SL' + str(sequence_length) + '.zip')
                                print('Writing ' + new_zip_file_name + ' ... ')
                                with zf.ZipFile(new_zip_file_name, mode='a') as low_entropy_archive:
                                    for file_name in nested_zip.namelist():
                                        new_file_name = file_name.replace(file_name[-4:], '-JL' + str(jump_length) + '-SL' + str(sequence_length) + file_name[-4:])
                                        with nested_zip.open(file_name) as file:
                                            file_data = file.read()
                                            modified_file = []
                                            for i in range(0,len(file_data),jump_length):
                                                modified_file += file_data[i:i+jump_length] + random_values.getbuffer()
                                            low_entropy_archive.writestr(new_file_name, bytes(modified_file))
                                    low_entropy_archive.close()
                                dataset.write(new_zip_file_name)
                                print('Wrote: '+ new_zip_file_name)
                                os.remove(new_zip_file_name)                                     
                        nested_zip.close()
                    archive.close()
        dataset.close()
    print('Finished')

    return

if __name__ == "__main__":
    main()