from django.contrib.auth.models import User
from contracts.models import Contract, Bank, Payment
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    contracts = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Contract.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'contracts']


class BankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = [
            'id', 'name', 'address', 'email', 'phone'
        ]


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            'id', 'contract_id', 'payment_date', 'payment_amount'
        ]

    def validate(self, attrs):
        msg = ''
        user = self.context['request'].user
        contract = attrs.get('contract_id')
        if contract.customer_id != user:
            msg += 'You have no contract with the code(contract_id) %s' \
                   % contract.id
            if msg:
                raise serializers.ValidationError(msg)
        payment_date = attrs.get('payment_date')
        payment_amount = attrs.get('payment_amount')
        payments = contract.payments.all()
        for payment in payments:
            payment_amount += payment.payment_amount
        if payment_date < contract.submission_date:
            msg += 'The payment date cannot be earlier than ' \
                   'the contract submission date.'
        if payment_amount > contract.amount_total:
            msg += 'The payment amount(%s) cannot be greater ' \
                   'than the due amount(%s) of the contract.' \
                   % (payment_amount, contract.amount_total)
        if msg:
            raise serializers.ValidationError(msg)
        return attrs


class PaymentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            'payment_date', 'payment_amount'
        ]


class ContractSerializer(serializers.ModelSerializer):
    customer_id = serializers.ReadOnlyField(source='customer_id.username')
    submission_date = serializers.DateField(allow_null=True, required=False)
    ip_remote_address = serializers.IPAddressField(read_only=True)
    payments = PaymentDetailSerializer(many=True, read_only=True)
    is_paid = serializers.SerializerMethodField()
    amount_due = serializers.SerializerMethodField()
    amount_total = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = [
            'id', 'customer_id', 'bank_id', 'amount', 'interest_rate',
            'ip_remote_address', 'submission_date', 'amount_total',
            'payments', 'is_paid', 'amount_paid', 'amount_due'
        ]

    def get_is_paid(self, obj):
        return obj.is_paid

    def get_amount_due(self, obj):
        return obj.amount_due

    def get_amount_total(self, obj):
        return obj.amount_total

