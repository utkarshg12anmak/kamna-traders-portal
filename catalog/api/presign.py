import uuid
import boto3
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def presign_upload(request):
    content_type = request.data.get('content_type')
    item_id = request.data.get('item_id')
    if not content_type or not item_id:
        return Response({'detail': 'content_type and item_id required'}, status=400)
    if content_type not in ('image/png','image/jpeg','image/webp'):
        return Response({'detail': 'Invalid content type'}, status=400)
    key = f"items/{item_id}/{uuid.uuid4().hex}"
    s3 = boto3.client('s3', region_name=getattr(settings, 'AWS_S3_REGION_NAME', None))
    url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': key, 'ContentType': content_type},
        ExpiresIn=600
    )
    public_base = getattr(settings, 'PUBLIC_CDN_BASE', f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com")
    return Response({'put_url': url, 'public_url': f"{public_base}/{key}"})
