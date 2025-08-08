from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, active_choices
from .presign import presign_upload

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),
    path('choices/active/', active_choices, name='active-choices'),
    path('uploads/presign/', presign_upload, name='presign-upload')
]
