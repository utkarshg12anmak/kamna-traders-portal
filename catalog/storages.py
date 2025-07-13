# catalog/storages.py

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    location = f"{settings.FOLDER_PREFIX}/product_images"
    default_acl = 'public-read'
    file_overwrite = False




