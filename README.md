# NOVA Programming Language

Nova is a modern, experimental programming language focused on simplicity, performance, and extensibility. The project currently includes a custom lexer, parser, abstract syntax tree (AST), source tracking, error handling, and the foundation for a complete compiler/interpreter.

## Current Features

- ✨ Custom lexer/tokenizer
- 📍 Source position tracking
- ⚠️ Error handling
- 🌳 Abstract Syntax Tree (AST)
- 🔄 Recursive descent parser
- 📦 Import system
- 🔧 Functions
- 📋 Structs
- 🎯 Enums
- 📝 Expression parsing framework

## Project Status

🚧 **Early Development (v0.5)**

## Roadmap

- [x] Lexer
- [x] Parser
- [ ] Semantic analyzer
- [ ] Type checker
- [ ] Interpreter
- [ ] Compiler backend
- [ ] Standard library

## Example

```nova
import io

fn main() {
    let x = 42

    if x >= 10 {
        io.println("Hello, Nova!")
    }
}
```

## Project Structure

```
nova-lang/
├── src/
│   └── nova.py          # Main compiler implementation
└── README.md            # This file
```

## Getting Started

### Prerequisites

- Python 3.8+

### Running the Lexer

```python
from nova import Lexer

source = """
fn main() {
    let x = 42
}
"""

lexer = Lexer(source)
tokens = lexer.tokenize()

for token in tokens:
    print(token)
```

### Running the Parser

```python
from nova import Lexer, Parser

lexer = Lexer(source)
tokens = lexer.tokenize()
parser = Parser(tokens)
program = parser.parse()
```

## Language Features

### Variables

Nova supports three types of variable declarations:

```nova
let x = 10          // Immutable binding
var y = 20          // Mutable variable
const PI = 3.14     // Constant
```

### Functions

```nova
fn add(x: i32, y: i32) -> i32 {
    return x + y
}
```

### Data Structures

**Structs:**
```nova
struct Point {
    x: i32,
    y: i32
}
```

**Enums:**
```nova
enum Result {
    Ok,
    Err
}
```

### Control Flow

```nova
if condition {
    // code
} else {
    // code
}

while condition {
    // code
}

for item in collection {
    // code
}
```

## Development Notes

- The lexer handles single-line comments (`//`)
- String escape sequences are supported (`\n`, `\t`, `\"`, `\\`)
- The parser uses recursive descent parsing
- Source positions are tracked for error reporting

## Contributing

This is an experimental project. Contributions are welcome!

## License

MIT License

## Author

NOVA-PROGRAME
