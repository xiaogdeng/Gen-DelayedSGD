## Towards Understanding the Generalizability of Delayed Stochastic Gradient Descent

This repository is the official implementation of paper **Towards Understanding the Generalizability of Delayed Stochastic Gradient Descent**. 

### Requirements

```setup
# GPU environment required
torch>=1.10.0
torchvision>=0.11.1
numpy>=1.19.5
```

### Dataset

The MNIST, CIFAR-10, and CIFAR-100 datasets can be downloaded automatically by `torchvision.datasets`. The four datasets of the LIBSVM database are available with `libsvm_data.py`

### Example Usage

```train
python server.py --cuda-ps --model 'ResNet' --dataset 'CIFAR100' \
                 --delay-type 'random' --delay 16 \
                 --num-workers 16 --lr 0.1 \
                 --num-epochs 200 --seed 42\
```

### Usage

```
usage: server.py [-h]
    [--model  {ResNet, MNISTNet, LinearNet_ijcnn1, LinearNet_covtype, Linearnet_rcv1, Linearnet_gisette}]
    [--dataset  {CIFAR10, CIFAR100, MNIST, IJCNN1, COVTYPE, RCV1, GISETTE}]
    [--delay-type  {fixed, random}]
    [--delay  Fixed or random delays]
    [--num-workers  Number of workers]
    [--lr  Learning rate]
    [--batch-size  Batch size] 
    [--num-epochs  Epoch]
    [--seed Random  Seed]
```

#### Note

* We provide a demo bash script file `bashrun.sh`

