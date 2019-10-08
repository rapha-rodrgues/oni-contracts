from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from contracts.models import Bank, Payment, Contract


class BankModelTestCase(TestCase):
    def setUp(self):
        Bank.objects.create(
            name='My Bank',
            address='445 Mount Eden Road, Mount Eden, Auckland',
            email='mybank@mybank.com',
            phone='9988776655'
        )

    def test_bank_object(self):
        banks = Bank.objects.count()
        self.assertEqual(banks, 1)


class ContractModelTestCase(TestCase):
    def setUp(self):
        now = datetime.now()
        user = User.objects.create(
            username='foo',
            email='foobarbaz@example.com',
            password='foobar'
        )
        bank = Bank.objects.create(
            name='My Bank',
            address='445 Mount Eden Road, Mount Eden, Auckland',
            email='mybank@mybank.com',
            phone='9988776655'
        )
        Contract.objects.create(
            customer_id=user,
            bank_id=bank,
            amount='500',
            interest_rate='20',
            ip_remote_address='192.168.0.1',
            submission_date=now
        )

    def test_contract_object(self):
        contracts = Contract.objects.count()
        self.assertEqual(contracts, 1)
