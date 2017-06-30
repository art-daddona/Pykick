#!/bin/bash
dropdb -U art kicker
dropdb -U art kickerlist
createdb -U art kicker
createdb -U art kickerlist
psql -U art kicker -f /home/art/work_stuff/pykick/config/kicker.sql
psql -U art kickerlist -f /home/art/work_stuff/pykick/config/kickerlist.sql
