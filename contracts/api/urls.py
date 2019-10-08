from rest_framework.routers import DefaultRouter
from contracts.api.views import BankViewSet, ContractViewSet, PaymentViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'contract', ContractViewSet, base_name='contract')
router.register(r'bank', BankViewSet, base_name='bank')
router.register(r'payment', PaymentViewSet, base_name='payment')

urlpatterns = router.urls
