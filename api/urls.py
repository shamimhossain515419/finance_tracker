
from rest_framework.routers import DefaultRouter
from django.urls import path , include
router = DefaultRouter()
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('users.urls')),
]