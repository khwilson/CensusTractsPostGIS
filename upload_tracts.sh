for filename in `ls *.zip`; do
  eight="${filename%.*}";
  echo "On file ${eight}";
  unzip ${filename};
  ogr2ogr -update -append -f PostgreSQL PG:"dbname=${PGDATABASE} user=${PGUSER} password=${PGPASSWORD} host=${PGHOST}" "${eight}.shp" -nlt MULTIPOLYGON25D -nln census_tracts -progress;
  rm -f "${eight}.dbf" "${eight}.prj" "${eight}.shp" "${eight}.shp.xml" "${eight}.shx";
done;
