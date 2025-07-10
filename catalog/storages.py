# catalog/storages.py

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = f"{settings.FOLDER_PREFIX}/static"
    default_acl = settings.AWS_DEFAULT_ACL
    file_overwrite = True

class MediaStorage(S3Boto3Storage):
    location = f"{settings.FOLDER_PREFIX}/media"
    default_acl = settings.AWS_DEFAULT_ACL
    file_overwrite = False
