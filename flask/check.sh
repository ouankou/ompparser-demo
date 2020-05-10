#!/bin/bash
source /home/rds/.bashrc
rm -rf /home/rds/dataracebench/micro-benchmarks/*
rm -rf /home/rds/dataracebench/results/*
mv /tmp/rds/* /home/rds/dataracebench/micro-benchmarks/.
cd /home/rds/dataracebench
scripts/test-harness.sh -d 32 -x archer
