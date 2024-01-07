#!/usr/bin/env python3

#imports
import os
import numpy as np
import zipfile as zf
import io

def main():

    #params
    jump_lengths = [12,32,44]
    sequence_lengths = [10,20]
    
    with zf.ZipFile('NapierOne-tiny.zip', mode='a') as dataset: #open NapierOne archive in append mode

        archive_list = dataset.namelist() #get names of files
        for archive_name in archive_list: #iterate through names

            if ('RANSOMWARE' in archive_name): #if ransomware zip files founded

                with dataset.open(archive_name) as archive: #open specific ransom archive (ex. Netwalker)

                    archive_filedata = io.BytesIO(archive.read()) #read bytes of archive
                    with zf.ZipFile(archive_filedata, mode='a') as nested_zip: #open in append mode

                        for jump_length in jump_lengths: #iterate trough params
                            for sequence_length in sequence_lengths: #iterate trough params

                                random_values = io.BytesIO(np.random.bytes(sequence_length)) #gerentate random bytes
                                new_zip_file_name = archive_name.replace('.zip', '-JL' + str(jump_length) + '-SL' + str(sequence_length) + '.zip') #name of new archive
                                print('Writing ' + new_zip_file_name + ' ... ') #output for context

                                with zf.ZipFile(new_zip_file_name, mode='a') as low_entropy_archive: #create new archive or append if already created

                                    for file_name in nested_zip.namelist(): #iterate trough original files

                                        new_file_name = file_name.replace(file_name[-4:], '-JL' + str(jump_length) + '-SL' + str(sequence_length) + file_name[-4:]) #name of new file
                                        
                                        with nested_zip.open(file_name) as file: #open files original archive
                                            file_data = file.read() #read bytes
                                            modified_file = [] #create modified file
                                            for i in range(0,len(file_data),jump_length):
                                                modified_file += file_data[i:i+jump_length] + random_values.getbuffer()
                                            low_entropy_archive.writestr(new_file_name, bytes(modified_file)) #write modified file into new archive
                                    
                                    low_entropy_archive.close() #close new archive
                                
                                dataset.write(new_zip_file_name) #write new archive into NapierOne
                                print('Wrote: '+ new_zip_file_name) #output for context
                                os.remove(new_zip_file_name) #delete temporary new archive                          
                        
                        nested_zip.close() #close selected ransomware archive
                    
                    archive.close() #close selected ransomware archive
        
        dataset.close() #close NapierOne dataset
    print('Finished')

    return

if __name__ == "__main__":
    main()