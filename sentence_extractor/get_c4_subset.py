# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.  
# SPDX-License-Identifier: CC-BY-NC-4.0

import os
import argparse

from datasets import load_dataset


def main(args):
    target_dir = args.target_dir
    cache_dir = args.cache_dir
    num_proc = args.num_proc
    url_path = args.url_path

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    urls = set()
    with open(url_path) as f:
        for line in f:
            urls.add(line.strip())
    print(f"Loaded {len(urls)} urls.")

    print(f"Filtering c4 for WebIE urls and store in HuggingFace format...")
    ds = load_dataset("c4", "en", cache_dir=cache_dir)
    webie_ds = ds.filter(lambda example: example["url"] in urls, num_proc=num_proc)
    webie_ds.save_to_disk(target_dir)
    print(f"WebIE c4 data is stored at {target_dir}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--target_dir",
        type=str,
        help="Path to target directory storing c4 WebIE data",
        default="../data/webie_c4",
    )
    parser.add_argument(
        "--url_path",
        type=str,
        help="Path to urls.txt file",
        default="../data/urls.txt",
    )
    parser.add_argument(
        "--cache_dir", type=str, help="(Optional) Cache directory to store c4 data"
    )
    parser.add_argument(
        "--num_proc",
        type=int,
        help="(Optional) Number of processes when processing the dataset locally",
        default=100,
    )

    args = parser.parse_args()
    main(args)
