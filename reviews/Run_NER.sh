#!/bin/bash
# 
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1              # Partition (job queue)
#SBATCH --requeue                    # Return job to the queue if preempted
#SBATCH --job-name=NER_GPU_Rew      # Assign a short name to your job
#SBATCH --nodes=1                    # Number of nodes you require
#SBATCH --cpus-per-task=1            # Cores per task (>1 if multithread tasks)
#SBATCH --mem=50gb                  # Real memory (RAM) required per node
#SBATCH --time=1-20:00:00            # Total run time limit (DD-HH:MM:SS)
#SBATCH --output=%j.out     # STDOUT file for SLURM output
#SBATCH --mail-type=FAIL   # Email on job start, end, and in case of failure
#SBATCH --mail-user=lopezbec@lafayette.edu

## Create a temp working directory within /scratch on the compute node
mkdir -p /scratch/$USER/$SLURM_JOB_NAME-$SLURM_JOB_ID

## Copy any scripts, data, etc. into the working directory (adjust filenames as needed)
cp -r \
  Run_NER.py  \
/scratch/$USER/$SLURM_JOB_NAME-$SLURM_JOB_ID

## Run the job (again, adjust filenames as needed)
cd /scratch/$USER/$SLURM_JOB_NAME-$SLURM_JOB_ID
export PATH=/home/lopezbec/anaconda3/bin:$PATH
source activate allennlp
srun python Run_NER.py  /home/lopezbec/AI_Gamification_Python/reviews/$1 
## Move outputs to the directory from which job was submitted and clean-up
cp -pru /scratch/$USER/$SLURM_JOB_NAME-$SLURM_JOB_ID/* $SLURM_SUBMIT_DIR
cd
rm -rf /scratch/$USER/$SLURM_JOB_NAME-$SLURM_JOB_ID

## Hang out for 10 seconds just to make sure everything is done
sleep 10
