# parse.py: Parse markdown sections into jupyter notebook
import re
import os
import sys
import nbformat
import argparse


def pattern_check(line: str) -> bool:
    """
    Look for headers and ordered lists in current line. 

    Params:
    * line: current line in markdown file

    Return:
    * `True` if current line is a header or ordered list. `False` otherwise.
    """
    # Look for headers in line
    header_levels = [
        '#',
        '##',
        '###',
        '####'
        ]
    pattern = ''
    for header in header_levels:
        pattern = fr'^{header}\s+(.*?)\s*$'
        if re.match(pattern, line):
            return True

    # Look for ordered lists in line (e.g.: "1.")
    pattern = r'\d.\s+(.*?)$'
    if re.match(pattern, line):
        return True

    return False

def md2nb(input_file: str, output_file: str):
    """
    Parse Markdown file sections and create Jupyter Notebook.

    Params:
    * input_file: path to .md file to be parsed
    * output_file: path to save .ipynb file
    """
    cells = []
    # Parse markdown sections
    with open(input_file, 'r') as f:
        markdown_content = ''
        in_code_block = False
        for line in f:
            if re.match(r"```", line):
                # Check for code blocks to not confuse python comments with headers
                in_code_block = not in_code_block
                markdown_content += line
                continue
            elif in_code_block:
                markdown_content += line
                continue
            elif pattern_check(line):
                cells.append(nbformat.v4.new_markdown_cell(source=markdown_content))
                markdown_content = '' + line
            else:
                markdown_content += line
        
        # Append last markdown content
        cells.append(nbformat.v4.new_markdown_cell(source=markdown_content))

    notebook = nbformat.v4.new_notebook()
    notebook['cells'] = cells

    with open(output_file, 'w') as f:
        nbformat.write(notebook, f)
        
    print(f'\nConversion Successful! Jupyter Notebook saved to "{output_file}"')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='md2nb',
        description='Convert Markdown headers to Jupyter Notebooks cells'
        )
    parser.add_argument('input_file', type=str, help='path to .md file to be parsed')
    parser.add_argument('output_file', type=str, help='path to save .ipynb file')
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f'\nERROR: Could not find markdown file in "{args.input_file}"')
        sys.exit()
    elif not args.input_file.endswith('.md'):
        print(f'\nERROR: input file "{args.input_file}" is not a markdown file')
        sys.exit()

    md2nb(input_file=args.input_file, output_file=args.output_file)
