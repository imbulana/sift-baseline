import os
import pickle
import sys

import numpy as np
import yaml
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import FunctionTransformer

from mlem.api import save
from utils import to_numpy

def train(seed, n_est, min_split, matrix):
    """
    Train a random forest classifier.

    Args:
        seed (int): Random seed.
        n_est (int): Number of trees in the forest.
        min_split (int): Minimum number of samples required to split an internal node.
        matrix (scipy.sparse.csr_matrix): Input matrix.

    Returns:
        sklearn.ensemble.RandomForestClassifier: Trained classifier.
    """
    labels = np.squeeze(matrix[:, 1].toarray())
    x = matrix[:, 2:]

    sys.stderr.write("Input matrix size {}\n".format(matrix.shape))
    sys.stderr.write("X matrix size {}\n".format(x.shape))
    sys.stderr.write("Y matrix size {}\n".format(labels.shape))

    clf = RandomForestClassifier(
        n_estimators=n_est, min_samples_split=min_split, n_jobs=2, random_state=seed
    )

    clf.fit(x, labels)

    return clf


def preprocess(text_batch):
    """
    Preprocess the text.

    Args:
        text (str): Input text.

    Returns:
        str: Preprocessed text.
    """
    return np.array([text.lower().strip() for text in text_batch])


def get_labels(predictions):
    """
    Get the label from the predictions.

    Args:
        predictions (numpy.ndarray): Predictions array.

    Returns:
        numpy.ndarray: Labels array.
    """
    return map(lambda x: "REAL" if x == 1 else "FAKE", predictions)


def main():
    params = yaml.safe_load(open("params.yaml"))["train"]

    if len(sys.argv) != 3:
        sys.stderr.write("Arguments error. Usage:\n")
        sys.stderr.write("\tpython train.py features model\n")
        sys.exit(1)

    input = sys.argv[1]
    output = sys.argv[2]
    seed = params["seed"]
    n_est = params["n_est"]
    min_split = params["min_split"]

    # Load the data
    with open(os.path.join(input, "train.pkl"), "rb") as fd:
        matrix, _ = pickle.load(fd)

    clf = train(seed=seed, n_est=n_est, min_split=min_split, matrix=matrix)

    # Save the model
    # with open('model.pkl', "wb") as fd:
    #     pickle.dump(clf, fd)

    vectorizer_path = os.path.join(input, "vectorizer.pkl")
    transformer_path = os.path.join(input, "tfidf_transformer.pkl")
    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)
    with open(transformer_path, "rb") as f:
        transformer = pickle.load(f)

    pipeline = Pipeline([
        ("vectorizer", vectorizer),
        ("tfidf", transformer),
        ("clf", clf),
    ])

    # mlem save
    save(
        pipeline,
        output,
        preprocess=to_numpy,
        sample_data=["Your AWS cloud cost optimizer is lying to you - Alexander the Great circa 320 BC."]
    )


if __name__ == "__main__":
    main()
