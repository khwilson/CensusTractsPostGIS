# PostGIS Census Tracts

For some reason it's super hard to find a simple instruction manual to
setup PostGIS and get some census tracts going. So for your enjoyment,
here are some scripts that do it.

Once you have Postgres and PostGIS setup, then set the environment variables
```
PGDATABASE=<dbname>
PGHOST=<host>
PGUSER=<user>
PGPASSWORD=<password>
```

Then run `python get_tracts.py`, followed by `cat make_fips_table.sql | psql`.

## Requirements

* postgres running with postgis somewhere
* `psql` on the box you're using
* `python` with dependencies:
  * `lxml`
  * `requests`

