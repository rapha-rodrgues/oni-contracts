DESCRIPTION
===========
A small API for contract management
The service is published on Heroku: https://oni-contracts.herokuapp.com
[Documentation](https://oni-contracts.herokuapp.com/swagger)


Instalation
===========
```bash
git clone https://github.com/rodriguesraphael/oni-contracts
cd oni-contracts/
virtualenv env -p python3
source env/bin/activate
```

Environment Variables
=====================
*[Dynaconf](https://dynaconf.readthedocs.io/en/latest/) was used to manage Django's environment variables and settings. 
Before starting the application create a .env file with the variables needed to start Django, you can copy the example contained in the repository, see the example below.*
```bash
cp .env.example .env
```

*Or you can export the variables in the environment.*
```bash
export CONTRACTS_ENV=development
export CONTRACTS_SECRET_KEY="CHANGE_ME!!!! (P.S. the SECRET_KEY environment variable will be used, if set, instead)."
export CONTRACTS_DEBUG=true
export CONTRACTS_ALLOWED_HOSTS=*
```


Deploy in Develop Environment
============================
```bash
pip install -r requirements-dev.txt
./manage.py migrate
```

Run Tests
=========
```bash
./manage.py test
```

Deploy in Docker
================
```bash
docker-compose up
```
*To execute commands in the application do as in the example below*
```bash
docker-compose run web ./manage.py test
```

HOW TO USE API - EXAMPLES
=========================

##### Create User

```bash
curl -i -X POST oni-contracts.herokuapp.com/api/v1/auth/signup \
        -H 'Content-Type: application/json' \
        -d '{
            "username": "foo",
            "email": "foo@bar.com",
            "password": "foobarpass"
        }'
```
*Expected Return*
```bash
HTTP/1.1 201 Created
Date: Sun, 06 Oct 2019 21:07:53 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Content-Type: application/json
Vary: Accept
Allow: POST, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 98

{"id":2,"username":"foo","email":"foo@bar.com","token":"4d3c775040dfb9d099118c707fe3220b50c7cf99"}
```

*Use the returned token to authenticate to the API and manage your contracts.*
*See in the example*

##### Create new Bank
```bash
curl -i -X POST https://oni-contracts.herokuapp.com/api/v1/bank \
        -H 'Content-Type: application/json' \
        -d '{
            "name": "foo",
            "address": "foo@bar.com",
            "email": "foo@bank.com",
            "phone": "9999988888"
        }'
```

*Expected Return*
```bash
HTTP/1.1 201 Created
Date: Sun, 06 Oct 2019 23:09:36 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 89

{"id":3,"name":"foo","address":"foo@bar.com","email":"foo@bank.com","phone":"9999988888"}
```

##### Create New Contract

```bash
curl -i -X POST https://oni-contracts.herokuapp.com/api/v1/contract \
        -H 'Content-Type: application/json' \
        -H "Authorization: Token 4d3c775040dfb9d099118c707fe3220b50c7cf99" \
        -d '{
            "bank_id": "1",
            "amount": "1000",
            "interest_rate": "10"
        }'
```

*Expected Return*
```bash
HTTP/1.1 201 Created
Date: Sun, 06 Oct 2019 23:20:03 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 163

{"customer_id":"foo","bank_id":1,"amount":"1000.00","interest_rate":"10.00","ip_remote_address":"127.0.0.1","submission_date":"2019-10-06"}  
```

##### Post Payment Contract
```bash
curl -i -X POST https://oni-contracts.herokuapp.com/api/v1/payment \
        -H 'Content-Type: application/json' \
        -H "Authorization: Token 4d3c775040dfb9d099118c707fe3220b50c7cf99" \
        -d '{
            "contract_id": "1",
            "payment_date": "2019-12-10",
            "payment_amount": "1000"
        }'
```

##### List Contracts
```bash
curl -i -X GET https://oni-contracts.herokuapp.com/api/v1/contract \
        -H "Authorization: Token 4d3c775040dfb9d099118c707fe3220b50c7cf99"
```

##### List Payments
```bash
curl -i -X GET https://oni-contracts.herokuapp.com/api/v1/payment \
        -H "Authorization: Token 4d3c775040dfb9d099118c707fe3220b50c7cf99"
```

##### List Banks
```bash
curl -i -X GET https://oni-contracts.herokuapp.com/api/v1/bank
```