from invoke import task, run
from functools import partial
run = partial(run, echo=True)


@task
def clean():
    run("find . -name '*.so' -delete")
    run("rm -rf kmeans.egg-info")
    run("rm -rf docs/_build/")
    run("rm -rf build/")


@task(clean)
def build():
    run("python setup.py develop")


@task(clean)
def pypi():
    run('python setup.py sdist upload')


@task(build)
def test():
    run('tox')


@task(build)
def benchmark():
    run('python performance.py')
