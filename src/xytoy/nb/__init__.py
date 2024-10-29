"""There are some funcitons to build the workflow around Jupyter notebooks."""

import os

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor


def execute_notebook(ipynb_file: str, executed_ipynb_file: str) -> None:
    """Execute a Jupyter notebook and save the executed notebook.

    Parameters:
    ipynb_file (str): Path to the input Jupyter notebook file.
    executed_ipynb_file (str): Path to save the executed Jupyter notebook file.
    """
    with open(ipynb_file, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600)
    # ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ipynb_dir = os.path.dirname(ipynb_file)
    print(ipynb_dir)
    ep.preprocess(nb, {"metadata": {"path": ipynb_dir}})

    with open(executed_ipynb_file, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)


def py2ipynb(py_file: str, ipynb_file: str) -> None:
    """Convert a Python script to a Jupyter notebook.

    Parameters:
    py_file (str): Path to the input Python script file.
    ipynb_file (str): Path to save the converted Jupyter notebook file.
    """
    with open(py_file, encoding="utf-8") as f:
        code = f.read()

    # Split the code into cells based on `# %%` markers
    code_cells = code.split("# %%")

    # Create a new Jupyter notebook
    nb = nbformat.v4.new_notebook()

    for cell_code in code_cells:
        cell_code = cell_code.strip()
        if cell_code:
            nb.cells.append(nbformat.v4.new_code_cell(cell_code))

    # Write the notebook to a file
    with open(ipynb_file, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)


def ipynb2html(ipynb_file: str, html_file: str) -> None:
    """Convert a Jupyter notebook to an HTML file.

    Parameters:
    ipynb_file (str): Path to the input Jupyter notebook file.
    html_file (str): Path to save the converted HTML file.
    """
    with open(ipynb_file, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    html_exporter = HTMLExporter()
    body, _ = html_exporter.from_notebook_node(nb)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(body)
