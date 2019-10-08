import datetime
from django.db import models
from django.core import validators


class Bank(models.Model):
    name = models.CharField(
        max_length=30
    )
    address = models.CharField(
        max_length=50
    )
    email = models.EmailField()
    phone = models.CharField(
        max_length=15
    )

    def __str__(self):
        return '{id} - {name} Bank'.format(
            id=self.id,
            name=self.name
        )


class Contract(models.Model):
    customer_id = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name="contracts"
    )
    bank_id = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="contracts"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(0.0),
            validators.MaxValueValidator(100.0)
        ],
    )
    ip_remote_address = models.GenericIPAddressField()
    submission_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return '{id} - Contract / {bank}'.format(
            id=self.id,
            bank=self.bank_id.name
        )

    @property
    def amount_due(self):
        return self.amount_total - self.amount_paid

    @property
    def amount_paid(self):
        amount_paid = 0
        payments = self.payments.all()
        if payments:
            for payment in payments:
                amount_paid += payment.payment_amount
        return amount_paid

    @property
    def is_paid(self):
        # If the account has been settled
        if self.amount_due == 0:
            return True
        else:
            return False

    @property
    def amount_total(self):
        # Total contract value
        return self.amount + (self.amount * (self.interest_rate / 100))


class Payment(models.Model):
    contract_id = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    payment_date = models.DateField()
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        contract = self.contract_id
        payments = contract.payments.all()
        payment_amount = self.payment_amount
        for payment in payments:
            payment_amount += payment.payment_amount
        if payment_amount > contract.amount_total:
            msg = "The payment amount cannot be greater than the amount due."
            raise validators.ValidationError(msg)
        super(Payment, self).save(*args, **kwargs)
