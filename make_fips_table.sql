DROP TABLE IF EXISTS fips_codes;

CREATE TABLE fips_codes
  (abbrev CHAR(2), state_fips CHAR(2), county_fips CHAR(3),
   fips CHAR(5), ansi CHAR(8), name VARCHAR(128), description VARCHAR(50));

\copy fips_codes FROM './fips_all.csv' DELIMITER ',' CSV HEADER;
