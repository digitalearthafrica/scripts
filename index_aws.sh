#!/usr/bin/env bash
datacube product add ../deafrica_config/products/ls5_usgs_sr_scene.yaml
datacube product add ../deafrica_config/products/ls8_usgs_sr_scene.yaml
datacube product add ../deafrica_config/products/ls_usgs_fc_scene.yaml

python3 ../cube-in-a-box/scripts/ls_public_bucket.py test-results-deafrica-st\
aging-west -p test  --suffix=".xml"  --start_date 1980-01-01 --end_date 2020-01\
-01

