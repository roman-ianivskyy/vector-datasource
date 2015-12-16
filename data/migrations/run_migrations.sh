#!/bin/bash

migration_dir=${0%/*}

# first run functions and triggers, bailing if either of these fail, as they
# are required by later steps.
psql --set ON_ERROR_STOP=1 -f "${migration_dir}/../functions.sql" $*
if [ $? -ne 0 ]; then echo "Installing new functions failed.">&2; exit 1; fi
psql --set ON_ERROR_STOP=1 -f "${migration_dir}/../triggers.sql" $*
if [ $? -ne 0 ]; then echo "Installing new triggers failed.">&2; exit 1; fi

# then disable triggers
for table in planet_osm_point planet_osm_line planet_osm_polygon; do
    psql -c "ALTER TABLE ${table} DISABLE TRIGGER USER" $*
done

# run updates in parallel. note that we don't bail here, as we want to
# re-enable the triggers regardless of whether we failed or not.
for sql in ${migration_dir}/*.sql; do
    psql -f "$sql" $* &
done

wait

# re-enable triggers
for table in planet_osm_point planet_osm_line planet_osm_polygon; do
    psql -c "ALTER TABLE ${table} ENABLE TRIGGER USER" $*
done
