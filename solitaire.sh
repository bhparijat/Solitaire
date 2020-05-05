#!/bin/bash
#SBATCH -A eecs
#SBATCH -p dgx2
#SBATCH -J data_cleaning
#SBATCH --nodes=2
#SBATCH --mem=40G
#SBATCH -o solitaire.out
#SBATCH -e solitaire.err
#SBATCH --time=7-00:00:00
echo "resource allocation done"
source /nfs/hpc/share/bhattpa/anaconda3/etc/profile.d/conda.sh
conda activate Solitaire
echo "conda environment activated"

python3 collect_data.py

echo "data collection done"
