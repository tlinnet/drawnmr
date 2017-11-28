from py2nb.tools import python_to_notebook
import os.path
import os
import glob
import subprocess

for filepath in glob.iglob('**/*.py', recursive=True):
#for filepath in glob.iglob('*.py'):
    # Pass
    if filepath in ['make_notebooks_from_py.py']:
        continue
    # Get filename and extension
    f, ext = os.path.splitext(filepath)
    # Only replace if not existing
    if os.path.isfile(f+'.ipynb'):
        print(".ipynb notebook already exists:", filepath)
    else:
        # Convert
        python_to_notebook(f+'.py', f+'.ipynb')
        # Execute it
        subprocess.call(["jupyter", "nbconvert", "--allow-errors", "--ExecutePreprocessor.timeout=30", "--to", "notebook", "--execute", f+'.ipynb', "--output", f+'.ipynb'])
        # Trust notebook
        subprocess.call(["jupyter", "trust", f+'.ipynb'])
        print("Converting to .ipynb notebook:", filepath)