import datetime
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from contracts.models import Contract, Bank, Payment
from rest_framework.test import APIClient


class ContractsTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            'testuser', 'test@example.com', 'testpassword')
        self.token = Token.objects.create(
            key='0123456789',
            user=self.test_user
        )
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.bank = Bank.objects.create(
            name='test',
            address='address test',
            email='bank@example.com',
            phone='11998876543'
        )
        self.contract = Contract.objects.create(
            bank_id=self.bank,
            amount="10000",
            interest_rate="15",
            ip_remote_address='127.0.0.1',
            submission_date=datetime.date.today(),
            customer_id=self.test_user
        )

    def test_create_bank(self):
        bank = {
            "name": "Bradesco",
            "address": "São Paulo",
            "email": "contato@bradesco.com",
            "phone": "11996543212"
        }
        response = self.client.post(
            '/api/v1/bank', bank, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bank.objects.count(), 2)

    def test_create_contract(self):
        contract = {
            "bank_id": 1,
            "amount": "10000",
            "interest_rate": "15"
        }
        response = self.client.post(
            '/api/v1/contract', contract, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contract.objects.count(), 2)

    def test_payment_contract(self):
        payment = {
            "contract_id": 1,
            "payment_date": "2020-10-09",
            "payment_amount": "11500"
        }
        response = self.client.post(
            '/api/v1/payment', payment, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contract = self.client.get('/api/v1/contract')
        self.assertEqual(contract.status_code, status.HTTP_200_OK)
        self.assertEqual(len(contract.data), 1)
        self.assertEqual(contract.data[0]['is_paid'], True)
        self.assertEqual(len(contract.data[0]['payments']), 1)

    def test_payment_amount_greater_than_contract(self):
        payment = {
            "contract_id": 1,
            "payment_date": "2020-10-09",
            "payment_amount": "50000"
        }
        response = self.client.post(
            '/api/v1/payment', payment, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_two_payments_amount_greater_than_contract(self):
        payment_one = {
            "contract_id": 1,
            "payment_date": "2020-10-09",
            "payment_amount": "11500"
        }
        response = self.client.post(
            '/api/v1/payment', payment_one, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payment_two = {
            "contract_id": 1,
            "payment_date": "2020-10-09",
            "payment_amount": "500"
        }
        response = self.client.post(
            '/api/v1/payment', payment_two, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_two_payments_contract(self):
        payment_one = {
            "contract_id": 1,
            "payment_date": "2020-10-09",
            "payment_amount": "11000"
        }
        response = self.client.post(
            '/api/v1/payment', payment_one, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payment_two = {
            "contract_id": 1,
            "payment_date": "2020-10-09",
            "payment_amount": "500"
        }
        response = self.client.post(
            '/api/v1/payment', payment_two, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contract = self.client.get('/api/v1/contract')
        self.assertEqual(contract.status_code, status.HTTP_200_OK)
        self.assertEqual(len(contract.data), 1)
        self.assertEqual(contract.data[0]['is_paid'], True)
        self.assertEqual(len(contract.data[0]['payments']), 2)

    def test_payment_date_less_than_contract_date(self):
        today = datetime.date.today()
        first_day = today.replace(day=1)
        last_month = first_day - datetime.timedelta(days=1)
        payment = {
            "contract_id": 1,
            "payment_date": last_month.strftime('%Y-%m-%d'),
            "payment_amount": "11500"
        }
        response = self.client.post(
            '/api/v1/payment', payment, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_requests_contract_endpoint(self):
        contract = {
            "bank_id": 1,
            "amount": "10000",
            "interest_rate": "15"
        }
        unauthorized_client = self.client
        unauthorized_client.credentials(**{})
        response = unauthorized_client.post(
            '/api/v1/contract', contract, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_requests_payment_endpoint(self):
        payment = {
            "contract_id": 1,
            "payment_date": "2020-10-09",
            "payment_amount": "100"
        }
        unauthorized_client = self.client
        unauthorized_client.credentials(**{})
        response = unauthorized_client.post(
            '/api/v1/payment', payment, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


