## SIFT: Semantically dIscerning Fact from Tale

<img src="assets/banner-v1-2.png" width="800px"></img>

## Setup

Create a conda environment with python 3.12

```bash
conda create -n sift python=3.12
conda activate sift
```

Clone this repo and install the required packages

```bash
git clone https://github.com/imbulana/sift.git

cd sift
python3 -m pip install -r requirements.txt
```

## Dataset

The dataset, intermediate steps, models, and experiment results are either stored and tracked in a DVC remote storage on Google Drive.

If you have access to the remote storage, pull it with

```bash
dvc pull
```

Otherwise set up your own remote storage following the instructions [here](https://dvc.org/doc/user-guide/data-management/remote-storage).

Then download the dataset. See [here](data/README.md) for more information about the dataset.

```bash
cd data/raw
curl -L -o data.zip \
    https://www.kaggle.com/api/v1/datasets/download/clmentbisaillon/fake-and-real-news-dataset

unzip data.zip && rm data.zip
mv True.csv real.csv && mv Fake.csv fake.csv
cd ../..
```

## Experiments

### Reproduce Current Workspace

To reproduce the pipeline [`dvc.yaml`](dvc.yaml) in the current workspace, run

```bash
dvc repro
```

To create a new experiment, modify the hyperparameters in [`params.yaml`](params.yaml) and the pipeline in [`dvc.yaml`](dvc.yaml) as required, then run

```bash
dvc exp run
``` 

To easily compare experiments, install the [DVC](https://marketplace.visualstudio.com/items?itemName=Iterative.dvc) extension on VSCode.

### Experiment Queue / Parallel Runs

To run a series of experiments with different hyperparamters in [`params.yaml`](params.yaml), add them to an experiment queue

```bash
dvc exp run -S 'featurize.max_features=5,10' -S 'featurize.ngrams=1,2,3' --queue
```

Then, run the experiments in parallel locally

```bash
dvc queue start -j <number of parallel jobs>
# OR if you want to time the set of experiments
time dvc exp run --run-all -j <number of parallel jobs>
```

## Deployment

Build a docker image

```bash
rm -rf bulid # remove existing build (if any)

mlem build docker_dir --model models/random_forest --server fastapi --target build
docker build build -t mlem-model:latest
```

### Local w/ Docker

Run the docker container to serve the model with FastAPI

```bash
docker run -p 8080:8080 mlem-model:latest
```

Navigate to http://localhost:8080/docs to see the OpenAPI spec.

See [here](https://mlem.ai/doc/user-guide/building/docker) more instructions and other build and serve options.


## Model Registry

Models are versioned within this repository using git tags. However the model files are stored in the remote DVC repository.

First store the repo url to a shell variable

```bash
export REPO=https://github.com/imbulana/sift
```

To see registered models, run

```bash
gto show
```

To register a new model, run

```bash
gto register <path_to_model> --repo $REPO
```