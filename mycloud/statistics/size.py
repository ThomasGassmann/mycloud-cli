import sys
import os
from hurry.filesize import size
from mycloud.helper import get_all_files_recursively
from mycloud.mycloudapi import MyCloudRequestExecutor, MetadataRequest
from mycloud.logger import log


def calculate_size(request_executor: MyCloudRequestExecutor, directory: str):
    original_out = sys.stdout
    sys.stdout = None
    summed_up = 0
    longest_string = 0
    file_count = 0
    for file in get_all_files_recursively(request_executor, directory):
        file_count += 1
        original_out.write(str(' ' * longest_string) + '\r')
        to_print = f'Bytes: {summed_up} | Size (readable): {size(summed_up)} | Count: {file_count}'
        if len(to_print) > longest_string:
            longest_string = len(to_print)

        original_out.write(to_print)
        summed_up += int(file['Length'])

    sys.stdout = original_out