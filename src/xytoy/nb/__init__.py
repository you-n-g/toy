"""There are some funcitons to build the workflow around Jupyter notebooks."""

import os
from pathlib import Path
from typing import Union

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


def py2html(py_file: str, html_file: Union[str, None] = None) -> str:
    """Convert a Python script to an HTML file by first converting it to a Jupyter notebook and executing it.

    Parameters:
    py_file (str): Path to the input Python script file.
    html_file (str, optional): Path to save the converted HTML file. If not provided, defaults to the same name
    as the Python file with an .html extension.
    """
    # Convert paths to Path objects for more robust handling
    py_path = Path(py_file)
    ipynb_file = py_path.with_suffix(".py.ipynb")
    executed_ipynb_file = py_path.with_suffix(".py.exec.ipynb")

    # Convert Python script to Jupyter notebook
    py2ipynb(str(py_path), str(ipynb_file))

    # Execute the Jupyter notebook
    execute_notebook(str(ipynb_file), str(executed_ipynb_file))

    # Determine the HTML file path if not provided
    if html_file is None:
        html_file = str(py_path.with_suffix(".py.html"))

    # Convert the executed notebook to HTML
    ipynb2html(str(executed_ipynb_file), html_file)
    return html_file
