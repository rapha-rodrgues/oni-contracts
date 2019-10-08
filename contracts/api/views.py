from contracts.api.serializers import \
    ContractSerializer, BankSerializer, PaymentSerializer
from contracts.models import Contract, Bank, Payment
from rest_framework import viewsets, mixins
from contracts.api.permissions import IsOwner
from rest_framework import permissions, status
from rest_framework.response import Response


class BankViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

    def list(self, request, *args, **kwargs):
        return super(BankViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(BankViewSet, self).create(request, *args, **kwargs)


class ContractViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(customer_id=user)

    def list(self, request, *args, **kwargs):
        return super(ContractViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(ContractViewSet, self).create(request, *args, **kwargs)

    def get_ip_address(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def perform_create(self, serializer):
        serializer.save(
            customer_id=self.request.user,
            ip_remote_address=self.get_ip_address(self.request),
        )


class PaymentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(contract_id__customer_id=user)

    def list(self, request, *args, **kwargs):
        return super(PaymentViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        context = {'request': self.request}
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
