-- Clear tables that already exist
DROP TABLE IF EXISTS fips_codes;
DROP TABLE IF EXISTS counties;
DROP TABLE IF EXISTS states;

-- Upload FIPS data
CREATE TABLE fips_codes
  (abbrev CHAR(2), state_fips CHAR(2), county_fips CHAR(3),
   fips CHAR(5), ansi CHAR(8), name VARCHAR(128), description VARCHAR(50));

\copy fips_codes FROM './fips_all.csv' DELIMITER ',' CSV HEADER;

-- Setup states table
SELECT state_fips AS fips,
       abbrev,
       ansi,
       name
  INTO states
  FROM fips_codes
 WHERE county_fips = '000' AND fips = '00000';

ALTER TABLE states ADD PRIMARY KEY (fips);

-- Setup counties table
SELECT county_fips AS fips,
       state_fips,
       abbrev AS state_abbrev,
       ansi,
       name,
       description
  INTO counties
  FROM fips_codes
 WHERE fips = '00000' AND county_fips != '000';

ALTER TABLE counties ADD PRIMARY KEY (state_fips, fips);
ALTER TABLE counties ADD CONSTRAINT state_county_fk FOREIGN KEY (state_fips) REFERENCES states ON DELETE CASCADE;
