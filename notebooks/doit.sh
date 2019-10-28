#!/bin/bash
#
# Simple script to execute 3 MCFOST cols.
# Example: sh doit.sh ../para_files/test_21_10_2019.para 0.5
# Will run MCFOST and compute dust and scattered light images at 0.5 microns.


mcfost='/Users/hcanovas/Astrofisica/MCFOST/mcfost'
para_file=$1

$mcfost $1
$mcfost $1 -dust_prop -op $2
$mcfost $1 -img $2 -rt

ndir_name=mcfostout_$(date '+%d_%m_%Y_%H%M%S')
mkdir $ndir_name
mv data_* $ndir_name
