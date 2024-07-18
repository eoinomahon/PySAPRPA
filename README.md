# PySAPRPA: Effortlessly Automate Your SAP Processes 

PySAPRPA is a Python library designed to supercharge your SAP automation efforts.

### Here's how it works: ###
* **Intelligent Object Identification:**  PySAPRPA automatically detects and labels SAP objects, eliminating the tedious and error-prone manual process of object extraction.
* **Environment-Agnostic Scripts:**  PySAPRPA eliminates the headache of environment-dependent scripts, enabling you to automate confidently across SAP landscapes.

**Benefits:**

* **Accelerated Development:**  Focus on your automation logic, not object identification. PySAPRPA significantly reduces development time and effort.
* **Increased Reliability:**  Environment-agnostic scripts ensure your automations remain robust and reliable regardless of SAP system changes.
* **Simplified Maintenance:**  Clear object labeling makes scripts easier to understand, debug, and maintain.

**Note:** Extensive testing is still pending. 


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

## Prerequisites:
1. Windows OS
2. SAP GUI on local device

## Usage

Getting started with PySAPRPA is straightforward. Import the library to start using its functions. Here's an example:

```python
import pysaprpa as saprpa
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
Author: Eoin O'Mahony\
LinkedIn: https://www.linkedin.com/in/eoin-omahony \
Email: eoinomahony028@gmail.com

## Changelog

### Version 1.0.0

- Initial release of PySAPRPA
- Project is still in beta, and updates are coming soon.
- If you encounter any issues or find bugs, please feel free to contact me!

## Coming Soon
- Export all file types
- get_objects() support for GuiShell objects
- ComboBox object support

---
