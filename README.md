# WebIE

This is a repository for the dataset of our paper [WebIE: Faithful and Robust Information Extraction on the Web](https://aclanthology.org/2023.acl-long.428/), published at ACL 2023.

Our dataset is created from the [c4 dataset](https://huggingface.co/datasets/c4), last downloaded May 2023. We only release our annotations, alongside preprocessing scripts to extract the sentences from c4 that we used to create the annotations. Please note that the dataset generated using these scripts may differ slightly from the one we used in the paper.

## Installation

First, activate a virtual environment, e.g. conda. Then, install the HuggingFace `datasets` library.
```
git clone https://github.com/amazon-science/webie.git
cd WebIE
conda create -n webie python=3.8
conda activate
pip install datasets
```

## Data Format

The WebIE annotations can be found in `data/webie_annotations` and the mWebIE annotations can be found in `data/mwebie_annotations`.

Each example in the dataset follows the format:
```
{
    "id": # id of the example, 
    "uri": # url of the example, 
    "meta_obj": # metadata of the example (triples, nli scores, etc), 
    "output": # gold answer, 
    "timestamp": # url timestamp, 
    "span": {
        "start": # character start index in the url's doc, 
        "end": # character end index in the doc url's doc}
    }
```

To create the full dataset, download the c4 data, and filter to only contains the subset used in WebIE. This might take a few hours, and you might need a large cache (350GB) for this. You can use `--cache_dir` option to specify your cache directory. E.g.
```
cd sentence_extractor
python get_c4_subset.py --target_dir ../data/webie_c4 --cache_dir /cache/huggingface/datasets
```

## Extract Sentences from C4

To extract the sentences, use the following command:
```
python extract_sentences.py --annotation_dir ../data/webie_annotations --data_dir ../data/webie_c4 --target_dir ../data/webie_complete
```
For mWebIE, you can add `--multilingual` flag:
```
python extract_sentences.py --annotation_dir ../data/mwebie_annotations --data_dir ../data/webie_c4 --target_dir ../data/mwebie_complete --multilingual
```
In the generated data, you will see a new json field `input` which is the input sentence for that example. Both `input` and `output` follow the same format used for the [GenIE](https://github.com/epfl-dlab/GenIE/tree/master) paper.

## Human Annotations

The ids of the examples that are validated with human annotations can be found in `data/annotated_ids.txt`.

## LICENSE
This project is licensed under the CC BY-NC-4.0 License. The c4 data may be subject to other licenses and copyrights, as applicable.

## Citation
```
@inproceedings{whitehouse-etal-2023-webie,
    title = "{W}eb{IE}: Faithful and Robust Information Extraction on the Web",
    author = "Whitehouse, Chenxi and Vania, Clara and Aji, Alham Fikri and Christodoulopoulos, Christos and Pierleoni, Andrea",
    booktitle = "Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.acl-long.428",
    pages = "7734--7755",
}
```
