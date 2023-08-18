#!/bin/bash

# model: ResNet, MNISTNet, LinearNet_ijcnn1, LinearNet_CovType, Linearnet_rcv1, Linearnet_gisette
MODEL='ResNet'

# dataset: CIFAR10, CIFAR100, MNIST, IJCNN1, COVTYPE, RCV1, GISETTE
DATASET='CIFAR100'

LOGDIR_OUT='./log'
LOGDIR='./runs/'
if [ ! -d $LOGDIR_OUT ]; then
  mkdir -p $LOGDIR_OUT
fi
if [ ! -d ${LOGDIR_OUT}/${MODEL}_${DATASET} ]; then
  mkdir -p ${LOGDIR_OUT}/${MODEL}_${DATASET}
fi

NUM_WORKERS=16
BATCH_SIZE=16
EPOCH=200
SEED=42
# SEED_list='1 19 42 44 80'

LR=0.1
# choices=['fixed', 'random']
DELAY_TYPE='random'

MAX_DELAY=4
JOB_NAME=${LOGDIR_OUT}/${MODEL}_${DATASET}/log_worker-${NUM_WORKERS}_${DELAY_TYPE}-${MAX_DELAY}delay_bs-${BATCH_SIZE}_lr-${LR}_seed-${SEED}
echo $JOB_NAME
python -u server.py --model $MODEL --cuda-ps --batch-size $BATCH_SIZE \
                    --dataset $DATASET --delay $MAX_DELAY --logdir $LOGDIR \
                    --delay-type $DELAY_TYPE --num-workers $NUM_WORKERS \
                    --lr $LR --num-epochs $EPOCH --seed $SEED\
                    > ${JOB_NAME}.out 2>&1 &
wait

MAX_DELAY=8
JOB_NAME=${LOGDIR_OUT}/${MODEL}_${DATASET}/log_worker-${NUM_WORKERS}_${DELAY_TYPE}-${MAX_DELAY}delay_bs-${BATCH_SIZE}_lr-${LR}_seed-${SEED}
echo $JOB_NAME
python -u server.py --model $MODEL --cuda-ps --batch-size $BATCH_SIZE \
                    --dataset $DATASET --delay $MAX_DELAY --logdir $LOGDIR \
                    --delay-type $DELAY_TYPE --num-workers $NUM_WORKERS \
                    --lr $LR --num-epochs $EPOCH --seed $SEED\
                    > ${JOB_NAME}.out 2>&1 &
wait

MAX_DELAY=16
JOB_NAME=${LOGDIR_OUT}/${MODEL}_${DATASET}/log_worker-${NUM_WORKERS}_${DELAY_TYPE}-${MAX_DELAY}delay_bs-${BATCH_SIZE}_lr-${LR}_seed-${SEED}
echo $JOB_NAME
python -u server.py --model $MODEL --cuda-ps --batch-size $BATCH_SIZE \
                    --dataset $DATASET --delay $MAX_DELAY --logdir $LOGDIR \
                    --delay-type $DELAY_TYPE --num-workers $NUM_WORKERS \
                    --lr $LR --num-epochs $EPOCH --seed $SEED\
                    > ${JOB_NAME}.out 2>&1 &
wait

MAX_DELAY=32
JOB_NAME=${LOGDIR_OUT}/${MODEL}_${DATASET}/log_worker-${NUM_WORKERS}_${DELAY_TYPE}-${MAX_DELAY}delay_bs-${BATCH_SIZE}_lr-${LR}_seed-${SEED}
echo $JOB_NAME
python -u server.py --model $MODEL --cuda-ps --batch-size $BATCH_SIZE \
                    --dataset $DATASET --delay $MAX_DELAY --logdir $LOGDIR \
                    --delay-type $DELAY_TYPE --num-workers $NUM_WORKERS \
                    --lr $LR --num-epochs $EPOCH --seed $SEED\
                    > ${JOB_NAME}.out 2>&1 &
wait

echo 'finish!'

