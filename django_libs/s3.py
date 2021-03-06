"""Custom S3 storage backends to store files in subfolders."""
from django.core.files.storage import get_storage_class

from storages.backends.s3boto import S3BotoStorage


class CachedS3BotoStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            'compressor.storage.CompressorFileStorage')()

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name

    def url(self, name):
        url = super(CachedS3BotoStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url


CompressorS3BotoStorage = lambda: CachedS3BotoStorage(location='compressor')
MediaRootS3BotoStorage = lambda: S3BotoStorage(location='media')
