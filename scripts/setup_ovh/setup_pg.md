
```{bash}
sudo su - postgres
psql
```

```{sql}
CREATE DATABASE hitarget;
CREATE USER django_hitarget WITH PASSWORD 'li8oph6aw8ulk7en6cyp7vak7ur3yet0bum6nom2cip3nird4y';

ALTER ROLE django_hitarget SET client_encoding TO 'utf8';
ALTER ROLE django_hitarget SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_hitarget SET timezone TO 'UTC+1';
GRANT ALL PRIVILEGES ON DATABASE hitarget TO django_hitarget;
\q
```