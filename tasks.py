from invoke import task, run

_run = run

def run(*args, **kwargs):
    kwargs.update(echo=True)
    return _run(*args, **kwargs)

@task
def clean():
    run("find . -name '*.so' -delete")
    run("rm -rf kmeans.egg-info")
    run("rm -rf docs/_build/")
    run("rm -rf build/")

@task('clean')
def build():
    run("python setup.py develop")

@task('clean')
def pypi():
    run('python setup.py sdist upload')

@task('clean')
def test():
    run('tox')
