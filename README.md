# md2nb
Script to parse headers and ordered lists from Markdown files into Jupyter Notebook markdown cells.

Mainly used to parse and convert COMP162 classwork markdown files to .ipynb

## Pre-requisites
```
pip install nbformat
```

## Usage
```
python3 md2nb.py [-h] <input_file> <output_file>
```
**positional arguments:**
  * `input_file`: path to .md file to be parsed
  * `output_file`: path to save .ipynb file

**Options:**
* `-h`, `--help`: show help message

### Example
```
$ python3 md2nb.py classwork17.md classwork17.ipynb

> Conversion Successful! Jupyter Notebook saved to classwork17.ipynb
```