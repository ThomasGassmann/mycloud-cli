from encryption import Encryptor
from progress import ProgressTracker
from io import TextIOWrapper


my_cloud_max_file_size = 3000000000
my_cloud_big_file_chunk_size = 1000000000


class StreamTransformer:
    def __init__(self, encryptor: Encryptor, tracker: ProgressTracker, chunk_size, split_into_chunks=False):
        self.encryptor = encryptor
        self.tracker = tracker


    def upload_generator(self, file_stream: TextIOWrapper):
        def generator():
            pass
        return generator


    def download_generator(self):
        pass