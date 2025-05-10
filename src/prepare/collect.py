import os
import sys
import yaml
import pandas as pd


def collect(in_path, out_path):
    """
    Collect data in directory into a single dataset

    Args:
        in_path (folder): Input folder path
        out_path (folder): Output folder path
    """

    collated = None
    for f in os.listdir(in_path):
        if f.endswith(".csv"):
            path = os.path.join(in_path, f)
            df = pd.read_csv(path)

            # combine
            if collated is None:
                collated = df
            else:
                collated = pd.concat([collated, df], ignore_index=True)

    # save collated dataset
    os.makedirs(os.path.join("data", ""), exist_ok=True)
    collated_out = os.path.join("data", "collated", "data.csv")

    collated.to_csv(collated_out, index=False)

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Arguments error.\n")
        sys.stderr.write("Usage: python3 src/prepare/collate.py path-to-data\n")
        sys.exit(1)

    params = yaml.safe_load(open("params.yaml"))["prepare"]
    seed = params["seed"]

    data_path = sys.argv[1]
    collect(data_path, seed)

if __name__ == "__main__":
    main()
