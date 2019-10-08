from rest_framework.routers import DefaultRouter
from core.api.views import UserCreate
from django.urls import path
from rest_auth.views import LoginView

router = DefaultRouter(trailing_slash=False)
router.register(r'auth/signup', UserCreate, base_name='signup')

urlpatterns = router.urls
urlpatterns += [path(r'auth/login', LoginView.as_view())]  # get token
