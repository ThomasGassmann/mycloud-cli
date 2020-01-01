import logging

import inject

from mycloud.constants import CHUNK_SIZE
from mycloud.drive.exceptions import DriveNotFoundException, DriveFailedToDeleteException
from mycloud.mycloudapi import (MyCloudRequestExecutor, MyCloudResponse,
                                ObjectResourceBuilder)
from mycloud.mycloudapi.requests.drive import (DeleteObjectRequest,
                                               GetObjectRequest,
                                               MetadataRequest,
                                               PutObjectRequest)


class DriveClient:

    request_executor: MyCloudRequestExecutor = inject.attr(
        MyCloudRequestExecutor)

    async def list_files(self, remote: str):
        (directories, fetched_files) = await self.get_directory_metadata(remote)
        for file in fetched_files:
            yield file

        for sub_directory in directories:
            async for file in self.list_files(sub_directory['Path']):
                yield file

    def is_directory(self, remote: str):
        return remote.endswith('/')

    async def get_directory_metadata(self, path: str):
        req = MetadataRequest(path)
        resp = await self.request_executor.execute(req)
        DriveClient._raise_404(resp)

        return await resp.formatted()

    async def download_each(self, directory_path: str, stream_factory):
        async for file in self.list_files(directory_path):
            with stream_factory(file) as stream:
                await self.download(file['Path'], stream)

    async def download(self, path: str, stream_factory):
        get_request = GetObjectRequest(path)
        resp: MyCloudResponse = await self.request_executor.execute(get_request)
        DriveClient._raise_404(resp)

        stream = stream_factory()
        while True:
            logging.debug(f'Reading download content...')
            chunk = await resp.result.content.read(CHUNK_SIZE)
            logging.debug(f'Got {len(chunk)} bytes')
            if not chunk:
                break
            logging.debug(f'Writing to output stream...')
            stream.write(chunk)
        stream.close()

    async def upload(self, path: str, stream):
        def _read():
            while True:
                chunk = stream.read(CHUNK_SIZE)
                if not chunk:
                    break
                yield chunk

        put_request = PutObjectRequest(path, _read())
        await self.request_executor.execute(put_request)

    async def delete(self, path: str):
        delete_request = DeleteObjectRequest(path)
        resp = await self.request_executor.execute(delete_request)
        DriveClient._raise_404(resp)
        if not resp.success:
            logging.info(f'Failed to delete {path}')
            raise DriveFailedToDeleteException

    @staticmethod
    def _raise_404(response: MyCloudResponse):
        if response.result.status == 404:
            raise DriveNotFoundException
