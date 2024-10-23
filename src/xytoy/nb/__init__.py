import os
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from typing import Any


def execute_notebook(ipynb_file: str, executed_ipynb_file: str) -> None:
    with open(ipynb_file, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600)
    # ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ipynb_dir = os.path.dirname(ipynb_file)
    print(ipynb_dir)
    ep.preprocess(nb, {'metadata': {'path': ipynb_dir}})

    with open(executed_ipynb_file, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)


def py2ipynb(py_file: str, ipynb_file: str) -> None:
    with open(py_file, 'r', encoding='utf-8') as f:
        code = f.read()

    # Split the code into cells based on `# %%` markers
    code_cells = code.split('# %%')

    # Create a new Jupyter notebook
    nb = nbformat.v4.new_notebook()

    for cell_code in code_cells:
        cell_code = cell_code.strip()
        if cell_code:
            nb.cells.append(nbformat.v4.new_code_cell(cell_code))

    # Write the notebook to a file
    with open(ipynb_file, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)


def ipynb2html(ipynb_file: str, html_file: str) -> None:
    with open(ipynb_file, 'r', encoding='utf-8') f:
        nb = nbformat.read(f, as_version=4)

    html_exporter = HTMLExporter()
    (body, resources) = html_exporter.from_notebook_node(nb)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(body)
