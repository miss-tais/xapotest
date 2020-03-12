# Xapo test app


## Project Setup

**Ensure that `docker` and `docker-compose` is installed**

```
$ git clone git@gitlab.com:miss-tais/xapotest.git
$ cd xapotest
```
*Then create `.env` file with the following settings:*
```
APP_CONFIG=production
SECRET_KEY=your-secret-key
MYSQL_USER=database-user
MYSQL_PASSWORD=database-password
MYSQL_DATABASE=database-name
MYSQL_ROOT_PASSWORD=mysql-root-password
SQLALCHEMY_TRACK_MODIFICATIONS=false
OER_API_KEY=OpenExchangeRates-api-key
OES_BASE=USD
```
*Run*
```
$ docker-compose up
```

## Examples
*Exchange currency. Parameters:*

* currency - ISO3 code

* amount - amount number
```
curl -X POST "http://localhost:8080/grab_and_save" -d "currency=EUR" -d "amount=10"
```
*Retrieve last exchange operations. Parameters:*

* currency - ISO3 code. Default: None

* number - number of records. Default: 1
```
curl -X GET "http://localhost:8080/last"
curl -X GET "http://localhost:8080/last?currency=EUR"
curl -X GET "http://localhost:8080/last?currency=EUR&number=10"
```

## Tests
*Run docker container with test database*
```
docker run --name test-mysql -p 3306 -e MYSQL_RANDOM_ROOT_PASSWORD=yes -e MYSQL_DATABASE=test_db -e MYSQL_USER=test_db_user -e MYSQL_PASSWORD=test_db_password -p 3307:3306 -d mysql:8
```
*Run tests*
```
python api/manage.py test
```