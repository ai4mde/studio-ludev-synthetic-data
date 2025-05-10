#!/bin/bash

export PROJECT_ID=$1
export PROJECT_SYSTEM=$2
export PROJECT_NAME=$3
export METADATA="$4"
export WORKDIR=/usr/src/prototypes/backend/generation
export OUTDIR=/usr/src/prototypes/generated_prototypes
export ROOT=/usr/src/prototypes/

generate_synthetic_data() {
    python "${WORKDIR}/generation_scripts/generate_synthetic_data.py" "$PROJECT_NAME" "$PROJECT_SYSTEM"
}

exit 0
