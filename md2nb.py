# parse.py: Parse markdown sections into jupyter notebook
import re
import nbformat


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
        '###'
        ]
    pattern = ''
    for header in header_levels:
        pattern = fr'^{header}\s+(.*?)\s*$'
        if re.match(pattern, line):
            print('Check!', line)
            return True

    # Look for ordered lists in line (e.g.: "1.")
    pattern = r'\d.\s+(.*?)$'
    if re.match(pattern, line):
        return True

    return False


# Parse markdown sections
input_file = 'classwork17.md'
with open(input_file, 'r') as f:
    # Add Markdown cells
    cells = []
    markdown_content = ''
    in_code_block = False
    for line in f:
        if re.match(r"```", line):
            # Check for code block start
            print("code block!")
            in_code_block = not in_code_block
            markdown_content += line
            continue
        elif in_code_block:
            # if inside code block, continue
            markdown_content += line
            continue
        elif pattern_check(line):
            # end concatenation. Create markdown cell and start over
            cells.append(nbformat.v4.new_markdown_cell(source=markdown_content))
            markdown_content = '' + line
        else:
            markdown_content += line
    
    cells.append(nbformat.v4.new_markdown_cell(source=markdown_content))

# Create new jupyter notebook
notebook = nbformat.v4.new_notebook()
notebook['cells'] = cells

output_file = 'test.ipynb'
with open(output_file, 'w') as f:
    nbformat.write(notebook, f)
    
print(f"Conversion Successful! Jupyter Notebook saved to {output_file}")

