#!/bin/bash
export models_dir=$PWD/../../models_repo
#copy models files
cp -r -n ${models_dir}/PaddleRec/multiview_simnet/. ./

./.run_ce.sh
