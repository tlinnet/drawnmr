from py2nb.tools import python_to_notebook
import os.path
import os
import glob

for filepath in glob.iglob('**/*.py', recursive=True):
    # Pass
    if filepath in ['make_notebooks_from_py.py']:
        continue
    # Get filename and extension
    f, ext = os.path.splitext(filepath)
    python_to_notebook(f+'.py', f+'.ipynb')
    print("Converting to .ipynb notebook:", filepath)