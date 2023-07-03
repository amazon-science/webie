# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.  
# SPDX-License-Identifier: CC-BY-NC-4.0

import os
import json
import gzip
import argparse

from tqdm import tqdm
from datasets import load_from_disk
from typing import Dict


def load_c4_data(data_dir: str) -> Dict[str, Dict]:
    """
    Load subset c4 data that is used in WebIE.

    Args:
    data_dir (str): The path to filtered c4 articles used in WebIE

    Returns:
    c4_data (Dict): A dictionary storing c4 data {url: {doc, timestamp}}
    """
    c4_data = {}
    ds = load_from_disk(data_dir)
    for i in tqdm(range(len(ds["train"]))):
        data = ds["train"][i]
        url = data["url"]
        doc = data["text"]
        timestamp = data["timestamp"]
        c4_data[url] = {"doc": doc, "timestamp": timestamp}
    return c4_data


def main(args):
    """Extract sentence from c4 corresponding to each annotation example."""

    annotation_dir = args.annotation_dir
    data_dir = args.data_dir
    target_dir = args.target_dir

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    print(f"Load filtered c4 data...")
    c4_data = load_c4_data(data_dir)

    splits = ["train", "val", "test"]
    if args.multilingual:
        # we only need to extract the EN sentences for multilingual
        splits = ["en_test"]

    filenames = {
        "train": ["train_part1.json.gz",
                  "train_part2.json.gz",
                  "train_part3.json.gz",
                  "train_part4.json.gz"],
        "val": ["val.json.gz"],
        "test": ["test.json.gz"],
        "en_test": ["en_test.json.gz"]
    }

    print(f"Extract sentences for each data split...")
    for split in splits:
        print(f"Split: {split}")
        out_f = gzip.open(os.path.join(target_dir, split + ".json.gz"), "wt")
        for fname in filenames[split]:
            ann_file = os.path.join(annotation_dir, fname)
            with gzip.open(ann_file, "rt") as in_f:
                for line in tqdm(in_f):
                    data = json.loads(line)

                    span = data["span"]
                    url = data["uri"]

                    timestamp = data["timestamp"]
                    assert timestamp == c4_data[url]["timestamp"]

                    doc = c4_data[url]["doc"]
                    start, end = span["start"], span["end"]
                    assert start < end

                    sentence = doc[start:end]
                    data["input"] = sentence
                    out_f.write(json.dumps(data) + "\n")
        out_f.close()
    print(f"Complete data is stored at {target_dir}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--annotation_dir",
        type=str,
        help="Path to WebIE annotations",
        default="../data/webie_annotations",
    )
    parser.add_argument(
        "--data_dir",
        type=str,
        help="Path to c4 WebIE directory",
        default="../data/webie_c4",
    )
    parser.add_argument(
        "--target_dir",
        type=str,
        help="Path to target directory storing annotations and sentences",
        default="../data/webie_complete",
    )
    parser.add_argument(
        "--multilingual",
        action="store_true",
        help="Add this parameter to transform multilingual WebIE",
    )

    args = parser.parse_args()
    main(args)
