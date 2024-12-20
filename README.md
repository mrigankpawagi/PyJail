# PyJail

<p align=center>
    <img src="https://github.com/user-attachments/assets/abea90ce-abe7-4f74-bd00-e4b73d17fb8f" />
</p>

PyJail is a Python module designed to provide a secure environment for executing untrusted code. PyJail is available on [PyPI](https://pypi.org/project/PyJail/).

> [!NOTE]
> PyJail uses `chroot` and is therefore currently supported only on Linux. Further, you must run your Python script as root.

```bash
pip install PyJail
```

To execute a function without access to your system, call it through PyJail as shown below.

```python
from pyjail import Jail

with Jail() as jail:
    result = jail.execute(untrusted_func, args=func_args, kwargs=func_kwargs)
```

The `Jail` class constructor has the optional parameters `path=os.path.join(os.getcwd(), "jail")`, `clear_before_create=False` and `clear_after_destroy=True`. The `path` parameter specifies the directory where the jail will be created. The `clear_before_create` parameter specifies whether the jail directory should be cleared before creation (if it already exists) and the `clear_after_destroy` parameter specifies whether the jail directory should be cleared after destruction.

The `execute` method takes the optional parameters `args` (positional arguments) and `kwargs` (keyword arguments) to pass arguments to the function `untrusted_func`. The `execute` method also takes an optional `timeout` parameter to specify the maximum time in seconds that the function is allowed to run. A `TimeoutError` will be raised if the function takes longer than the specified time to execute. Otherwise, the return value of the function is returned (and exceptions are raised if the function raises an exception).
