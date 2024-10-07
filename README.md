# Introduction

this project extract entity and relationship from chemical literatures

# Usage

## Install prerequisite packages

```shell
sudo apt install default-jre opennlp antlr4 python3-jpype python3-urllib3
python3 -m pip install -r requirements.txt
```

## extract experimental steps

```shell
python3 steps.py --input_dir <path/to/literatures/in/markdown/format> --output_dir <output/path>
```
