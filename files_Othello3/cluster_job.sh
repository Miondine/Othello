#!/bin/bash

# Request resources:
#SBATCH -n 1          # 1 CPU core
#SBATCH --mem=8G      # 1 GB RAM
#SBATCH --time=50:0:0  # 20 hours (hours:minutes:seconds)
#SBATCH -p seq7.q

# SBATCH --mail-type=ALL
# SBATCH --mail-user skcn96@durham.ac.uk


# Make python available:
module load python/3.6.8

# Commands to be run:

python3 main7.py