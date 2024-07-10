# PySAPRPA

PySAPRPA—a Python library for RPA functions in SAP GUI. PySAPRPA provides an easy-to-use interface for automating tasks within the SAP GUI environment.

## Installation

To install PySAPRPA, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/eoinomahon/pysaprpa.git
   cd pysaprpa
   ```

2. Install the library:
   ```bash
   pip install .
   ```

## Usage

Getting started with PySAPRPA is straightforward. Simply import the library and start using its functions. Here's an example:

```python
import pysaprpa
# Use the library's functions here
```

## API Reference

### `ObjectTree` Class

The `ObjectTree` class provides methods for interacting with SAP objects. Here are some key methods:

- `__init__(self, session: object = None, date_format: str = '%m/%d/%Y')`: Initialize the `ObjectTree` class.
- `start_transaction(self, t_code: str = None)`: Start a new transaction in the SAP system.
- `end_transaction(self)`: End the current transaction and return to the menu.
- `get_objects(self, window: int = 0)`: Retrieve the object tree from the SAP system.
- `set_parameters(self, variant: str = '', **kwargs)`: Set parameters for an instance of `ObjectTree`.
- `execute(self, vkey: Union[int, str] = '')`: Execute a command in the SAP system.
- `export(self, how: str, directory: str, file_name: str)`: Export data from SAP.

### `connect_SAP` Function

The `connect_SAP` function establishes a connection to the SAP system and returns the session object necessary for interaction.

## Documentation

For detailed information and examples, please refer to the [PySAPRPA Documentation](https://github.com/eoinomahon/PySAPRPA/wiki/Docs).

## Changelog

### Version 1.0.0

- Initial release of PySAPRPA
- Project is still in beta, and updates are coming soon.
- If you encounter any issues or find bugs, please feel free to contact me!

---
