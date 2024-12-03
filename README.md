# PyJail

PyJail is a Python module designed to provide a secure environment for executing untrusted code. PyJail is available on [PyPI](https://pypi.org/project/PyJail/).

```bash
pip install PyJail
```

To execute a function without access to your system, call it through PyJail as shown below.

```python
from pyjail import Jail

with Jail() as jail:
    result = jail.execute(untrusted_func, *func_args, **func_kwargs)
```

The `Jail` class constructor has the optional parameters `path=os.path.join(os.getcwd(), "jail")` and `clear_before_create=True`. The `path` parameter specifies the directory where the jail will be created (note that this is a transient directory that will be deleted when the `Jail` object is destroyed) and the `clear_before_create` parameter specifies whether the jail directory should be cleared before creation (if it already exists).

> [!NOTE]
> You must run your python script as root to create a jail.
