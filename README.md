[![Build Status](https://travis-ci.org/ltalirz/aiida-ase-basic.svg?branch=master)](https://travis-ci.org/ltalirz/aiida-ase-basic)
[![Coverage Status](https://coveralls.io/repos/github/ltalirz/aiida-ase-basic/badge.svg?branch=master)](https://coveralls.io/github/ltalirz/aiida-ase-basic?branch=master)
[![Docs status](https://readthedocs.org/projects/aiida-ase-basic/badge)](http://aiida-ase-basic.readthedocs.io/)
[![PyPI version](https://badge.fury.io/py/aiida-ase-basic.svg)](https://badge.fury.io/py/aiida-ase-basic)

# aiida-ase-basic

AiiDA plugin for wrapping the atomistic simulation environment.

## Features

 * Add input files using `SinglefileData`:
   ```python
   SinglefileData = DataFactory('singlefile')
   inputs['files']['file1'] = SinglefileData(file='/path/to/file1')
   inputs['files']['file2'] = SinglefileData(file='/path/to/file2')
   ```

## Installation

```shell
pip install aiida-ase-basic
verdi quicksetup  # better to set up a new profile
verdi plugin list aiida.calculations  # should now show your calclulation plugins
```

```
verdi code setup  # set up python code 'python3'
cd examples
verdi run example_emt.py python3
```

## Development

```shell
git clone https://github.com/ltalirz/aiida-ase-basic .
cd aiida-ase-basic
pip install -e .[pre-commit,testing]  # install extra dependencies
pre-commit install  # install pre-commit hooks
pytest -v  # discover and run all tests
```

See the [developer guide](http://aiida-ase-basic.readthedocs.io/en/latest/developer_guide/index.html) for more information.

## License

MIT


## Contact

leopold.talirz@gmail.com

