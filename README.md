# SRO Measures Demo

This study is a step-by-step walk-through of the OpenSAFELY framework, using the Service Restoration Observatory (SRO) Measures study as a guide.

* Released outputs are in the [released outputs folder][].
* If you are interested in how we defined our variables, then take a look at the [study definition][];
  this is written in Python, but non-programmers should be able to understand what is going on there.
* If you are interested in how we defined our codelists, then take look in the [codelists folder][].
* Developers and epidemiologists interested in the framework should review the [OpenSAFELY documentation][].

## Development

### Remote

Use [Gitpod][] for remote development:
<https://gitpod.io/#https://github.com/opensafely/sro-measures-demo>.

### Local

For local (non-Docker) development, first install [pyenv][] and execute:

```sh
pyenv install $(pyenv local)
```

Then, execute:

```sh
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

###  QA

```sh
bin/codestyle.sh .
```

## About OpenSAFELY

OpenSAFELY is a secure analytics platform for electronic health records research in the NHS.
You can read more at [OpenSAFELY.org][].

[codelists folder]: codelists
[Gitpod]: https://www.gitpod.io/
[OpenSAFELY documentation]:https://docs.opensafely.org
[OpenSAFELY.org]: https://opensafely.org
[pyenv]: https://github.com/pyenv/pyenv
[released outputs folder]: released_outputs
[study definition]: analysis/study_definition.py
