"""
Deployment file to facilitate AbiPy releases.
Use invoke --list to get list of tasks
"""

import os
import subprocess

from invoke import task
from monty.os import cd

#from abipy.core.release import __version__ as CURRENT_VER
#NEW_VER = datetime.datetime.today().strftime("%Y.%-m.%-d")

ABIPY_ROOTDIR = os.path.dirname(__file__)
#DOCS_DIR = os.path.join(ABIPY_ROOTDIR, "docs")

@task
def make_html(ctx):
    # Get all ipynb files
    top = os.path.join(ABIPY_ROOTDIR, "abitutorials")
    from monty.os.path import find_exts
    nbpaths = find_exts(top, ".ipynb", exclude_dirs=".ipynb_checkpoints|old_notebooks")
    # Basenames must be unique.
    assert len(nbpaths) == len(set([os.path.basename(p) for p in nbpaths]))
    #nb_paths = [path for path in nbpaths
    #                 if not any([path.startswith(e) for e in EXCLUDE_NBS])]
    #self.nb_paths = sorted(nbpaths)
    #print("top", top, "\nnbpaths", nbpaths)

    retcode = 0
    for path in nbpaths:
        print("Building notebook:", path)
        try:
            nb, errors = notebook_run(path, with_html=True)
            if errors:
                retcode += 1
                for e in errors:
                    print(e)

        except subprocess.CalledProcessError as exc:
            retcode += 1
            print(exc)

    return retcode


#@task
#def make_doc(ctx):
#    with cd(DOCS_DIR):
#        ctx.run("make clean")
#        ctx.run("make", env=dict(READTHEDOCS="1"), pty=True)
#        open_doc(ctx)


#@task
#def push_doc(ctx):
#    make_doc(ctx)
#    with cd(DOCS_DIR):
#        ctx.run("./ghp_import.py _build/html/ -n -p")


#@task
#def open_doc(ctx):
#    import webbrowser
#    webbrowser.open_new_tab("file://" + os.path.join(ABIPY_ROOTDIR, "docs/_build/html/index.html"))


#@task
#def twine(ctx):
#    with cd(ABIPY_ROOTDIR):
#        ctx.run("rm dist/*.*", warn=True)
#        ctx.run("python setup.py register sdist bdist_wheel")
#        ctx.run("twine upload dist/*")


#@task
#def pytest(ctx):
#    pytest_cmd = r"""\
#pytest -n 2 --cov-config=.coveragerc --cov=abipy -v --doctest-modules abipy \
#    --ignore=abipy/integration_tests --ignore=abipy/data/refs --ignore=abipy/scripts/ \
#    --ignore=abipy/examples/plot --ignore=abipy/examples/flows --ignore=abipy/gui
#"""
#    with cd(ABIPY_ROOTDIR):
#        ctx.run(pytest_cmd, pty=True)
#
#
#@task
#def plots(ctx):
#    with cd(os.path.join(ABIPY_ROOTDIR, "abipy", "examples")):
#        ctx.run("_runplots.py", pty=True)
#
#@task
#def flows(ctx):
#    with cd(os.path.join(ABIPY_ROOTDIR, "abipy", "examples")):
#        ctx.run("_runflows.py", pty=True)

#@task
#def move_to_master(ctx):
#    ctx.run("git tag -a v%s -m \"v%s release\"" % (NEW_VER, NEW_VER))
#    ctx.run("git push --tags")
#    ctx.run("git checkout master")
#    ctx.run("git pull")
#    ctx.run("git merge develop")
#    ctx.run("git push")
#    ctx.run("git checkout develop")


#@task
#def update_changelog(ctx):
#
#    output = subprocess.check_output(["git", "log", "--pretty=format:%s",
#                                      "v%s..HEAD" % CURRENT_VER])
#    lines = ["* " + l for l in output.decode("utf-8").strip().split("\n")]
#    with open("CHANGES.rst") as f:
#        contents = f.read()
#    l = "=========="
#    toks = contents.split(l)
#    head = "\n\nv%s\n" % NEW_VER + "-" * (len(NEW_VER) + 1) + "\n"
#    toks.insert(-1, head + "\n".join(lines))
#    with open("CHANGES.rst", "w") as f:
#        f.write(toks[0] + l + "".join(toks[1:]))


#@task
#def release(ctx, run_tests=True):
#    ctx.run("rm -r dist build abipy.egg-info", warn=True)
#    set_ver(ctx)
#    if run_tests: pytest(ctx)
#    publish(ctx)
#    log_ver(ctx)
#    update_doc(ctx)
#    merge_stable(ctx)
#    release_github(ctx)


def notebook_run(path, with_html=False):
    """
    Execute a notebook via nbconvert and collect output.

    Taken from
    https://blog.thedataincubator.com/2016/06/testing-jupyter-notebooks/

    Args:
        path (str): file path for the notebook object

    Returns: (parsed nb object, execution errors)

    """
    import os
    import nbformat
    import tempfile
    import subprocess

    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=300",
                "--ExecutePreprocessor.allow_errors=True",
                "--output", fout.name, path]
        subprocess.check_call(args)

        fout.seek(0)
        nb = nbformat.read(fout, nbformat.current_nbformat)

        errors = [output for cell in nb.cells if "outputs" in cell
            for output in cell["outputs"] if output.output_type == "error"]

        if not errors and with_html:
            html_path = path.replace(".ipynb", ".html")
            args = ["jupyter", "nbconvert", "--to", "html", "--execute",
                    "--ExecutePreprocessor.timeout=300",
                    "--ExecutePreprocessor.allow_errors=True",
                    "--output", html_path, fout.name]
            subprocess.check_call(args)

    return nb, errors
