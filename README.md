# Traceipy

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/DebanKsahu/traceipy)](https://github.com/DebanKsahu/traceipy/blob/main/LICENSE)

Traceipy is a powerful Python tracing and profiling tool that provides detailed insights into your code execution, supporting both synchronous and asynchronous functions. It helps you understand the performance characteristics and execution flow of your Python applications with beautiful rich-formatted output.

## Features

- 🔄 Support for both synchronous and asynchronous functions
- 📊 Detailed CPU time and wait time measurements
- 🌳 Hierarchical function call tracking with visual tree representation
- 🎨 Beautiful rich-formatted output tables
- 🔍 Function call stack visualization
- 🏷️ Unique function call ID generation with natural ordering
- 📝 Parent-child relationship tracking
- 🎯 Visual function call tree with timing information
- 🔀 Ordered trace output using custom function ID comparison

## Installation

```bash
pip install traceipy
```

## Usage

Here's a simple example that demonstrates how to use Traceipy:

```python
import asyncio
from traceipy import Traceipy
from traceipy.trace_decorator import traceipy_decorator

# Initialize the tracer
root_class = Traceipy()

# Decorate your functions
# Set show_tree=True to display the execution tree visualization
@traceipy_decorator(root_class=root_class, show_tree=True)
def cpu_bound(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

@traceipy_decorator(root_class=root_class, show_tree=True)
async def slow_async():
    await asyncio.sleep(1)
    return cpu_bound(1000000)

@traceipy_decorator(root_class=root_class, show_tree=True)
async def main():
    x = await slow_async()
    y = cpu_bound(100000000)
    return x + y

# Run your code
if __name__ == "__main__":
    result = asyncio.run(main())
```

The output includes:

1. A detailed profiling table showing:
   - Parent function ID and name
   - Current function ID and name
   - CPU time consumption
   - Wait time for async functions
   - Function type indication (SYNC/ASYNC)

2. A visual execution tree (when show_tree=True) displaying:
   - Hierarchical function calls
   - CPU time for each function
   - Wait time for async functions
   - Parent-child relationships in tree format

## How It Works

Traceipy uses context variables to maintain the execution state and provides a decorator that can be applied to both synchronous and asynchronous functions. It tracks:

- Function call depth
- Parent-child relationships
- CPU time using `time.process_time()`
- Wait time for async operations
- Unique call IDs for each function invocation

The trace data is organized using a custom-ordered data structure where function IDs are compared naturally (e.g., "1.2" comes before "1.10"). This ordering is implemented using Python's `@total_ordering` decorator, ensuring consistent and logical presentation of the execution trace.

## Requirements

- Python 3.12 or higher
- rich>=14.1.0
- yappi>=1.6.10

## Contributing

Contributions are welcome! Feel free to:
- Report issues
- Submit pull requests
- Suggest new features
- Improve documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- Deban Kumar Sahu