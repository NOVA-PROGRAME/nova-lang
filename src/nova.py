# ==========================================
# NOVA v0.5 (Part 1)
# Lexer + Tokens + Errors + Source Tracking
# ==========================================

from dataclasses import dataclass
from enum import Enum, auto


# ==========================================
# Errors
# ==========================================

class NovaError(Exception):
    pass


class NovaSyntaxError(NovaError):
    pass


class NovaLexerError(NovaError):
    pass


# ==========================================
# Source Position
# ==========================================

@dataclass
class SourcePosition:
    line: int
    column: int
    index: int

    def __str__(self):
        return f"{self.line}:{self.column}"


# ==========================================
# Token Types
# ==========================================

class TokenType(Enum):

    EOF = auto()

    IDENTIFIER = auto()

    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    CHAR = auto()

    TRUE = auto()
    FALSE = auto()

    LET = auto()
    VAR = auto()
    CONST = auto()

    FN = auto()
    RETURN = auto()

    IF = auto()
    ELSE = auto()

    WHILE = auto()

    FOR = auto()
    IN = auto()

    STRUCT = auto()
    ENUM = auto()

    MATCH = auto()

    IMPORT = auto()
    AS = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()

    EQUAL = auto()

    EQUAL_EQUAL = auto()
    BANG_EQUAL = auto()

    GREATER = auto()
    GREATER_EQUAL = auto()

    LESS = auto()
    LESS_EQUAL = auto()

    AND_AND = auto()
    OR_OR = auto()

    BANG = auto()

    PLUS_EQUAL = auto()
    MINUS_EQUAL = auto()
    STAR_EQUAL = auto()
    SLASH_EQUAL = auto()

    ARROW = auto()
    FAT_ARROW = auto()

    DOT = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()

    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()

    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()

    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()

    RANGE = auto()


# ==========================================
# Token
# ==========================================

@dataclass
class Token:
    type: TokenType
    value: str
    position: SourcePosition

    def __repr__(self):
        return (
            f"Token("
            f"{self.type.name}, "
            f"{repr(self.value)}, "
            f"{self.position}"
            f")"
        )


# ==========================================
# Keywords
# ==========================================

KEYWORDS = {
    "let": TokenType.LET,
    "var": TokenType.VAR,
    "const": TokenType.CONST,

    "fn": TokenType.FN,
    "return": TokenType.RETURN,

    "if": TokenType.IF,
    "else": TokenType.ELSE,

    "while": TokenType.WHILE,

    "for": TokenType.FOR,
    "in": TokenType.IN,

    "struct": TokenType.STRUCT,
    "enum": TokenType.ENUM,

    "match": TokenType.MATCH,

    "import": TokenType.IMPORT,
    "as": TokenType.AS,

    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
}


# ==========================================
# Lexer
# ==========================================

class Lexer:

    def __init__(self, source: str):

        self.source = source

        self.index = 0
        self.line = 1
        self.column = 1

    # ----------------------

    def current(self):

        if self.index >= len(self.source):
            return '\0'

        return self.source[self.index]

    # ----------------------

    def peek(self, offset=1):

        pos = self.index + offset

        if pos >= len(self.source):
            return '\0'

        return self.source[pos]

    # ----------------------

    def advance(self):

        ch = self.current()

        self.index += 1

        if ch == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return ch

    # ----------------------

    def position(self):

        return SourcePosition(
            self.line,
            self.column,
            self.index
        )

    # ----------------------

    def skip_whitespace(self):

        while True:

            ch = self.current()

            if ch in (' ', '\t', '\r', '\n'):
                self.advance()
                continue

            # comments

            if ch == '/' and self.peek() == '/':

                while (
                    self.current() != '\n'
                    and self.current() != '\0'
                ):
                    self.advance()

                continue

            break

    # ----------------------

    def number(self):

        start = self.position()

        text = ""

        while self.current().isdigit():

            text += self.advance()

        if (
            self.current() == '.'
            and self.peek().isdigit()
        ):

            text += self.advance()

            while self.current().isdigit():

                text += self.advance()

            return Token(
                TokenType.FLOAT,
                text,
                start
            )

        return Token(
            TokenType.INTEGER,
            text,
            start
        )

    # ----------------------

    def identifier(self):

        start = self.position()

        text = ""

        while (
            self.current().isalnum()
            or self.current() == '_'
        ):
            text += self.advance()

        token_type = KEYWORDS.get(
            text,
            TokenType.IDENTIFIER
        )

        return Token(
            token_type,
            text,
            start
        )

    # ----------------------

    def string(self):

        start = self.position()

        self.advance()

        text = ""

        while True:

            ch = self.current()

            if ch == '\0':

                raise NovaLexerError(
                    f"Unterminated string at {start}"
                )

            if ch == '"':

                self.advance()

                break

            if ch == '\\':

                self.advance()

                esc = self.current()

                mapping = {
                    'n': '\n',
                    't': '\t',
                    '"': '"',
                    '\\': '\\'
                }

                text += mapping.get(
                    esc,
                    esc
                )

                self.advance()

                continue

            text += self.advance()

        return Token(
            TokenType.STRING,
            text,
            start
        )

    # ----------------------

    def next_token(self):

        self.skip_whitespace()

        start = self.position()

        ch = self.current()

        if ch == '\0':

            return Token(
                TokenType.EOF,
                "",
                start
            )

        if ch.isdigit():

            return self.number()

        if (
            ch.isalpha()
            or ch == '_'
        ):

            return self.identifier()

        if ch == '"':

            return self.string()

        # 2-char operators

        two = ch + self.peek()

        multi = {
            "==": TokenType.EQUAL_EQUAL,
            "!=": TokenType.BANG_EQUAL,

            ">=": TokenType.GREATER_EQUAL,
            "<=": TokenType.LESS_EQUAL,

            "&&": TokenType.AND_AND,
            "||": TokenType.OR_OR,

            "+=": TokenType.PLUS_EQUAL,
            "-=": TokenType.MINUS_EQUAL,

            "*=": TokenType.STAR_EQUAL,
            "/=": TokenType.SLASH_EQUAL,

            "->": TokenType.ARROW,
            "=>": TokenType.FAT_ARROW,

            "..": TokenType.RANGE,
        }

        if two in multi:

            self.advance()
            self.advance()

            return Token(
                multi[two],
                two,
                start
            )

        single = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,

            '*': TokenType.STAR,
            '/': TokenType.SLASH,
            '%': TokenType.PERCENT,

            '=': TokenType.EQUAL,

            '>': TokenType.GREATER,
            '<': TokenType.LESS,

            '!': TokenType.BANG,

            '.': TokenType.DOT,

            ',': TokenType.COMMA,
            ':': TokenType.COLON,
            ';': TokenType.SEMICOLON,

            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,

            '{': TokenType.LEFT_BRACE,
            '}': TokenType.RIGHT_BRACE,

            '[': TokenType.LEFT_BRACKET,
            ']': TokenType.RIGHT_BRACKET,
        }

        if ch in single:

            self.advance()

            return Token(
                single[ch],
                ch,
                start
            )

        raise NovaLexerError(
            f"Unexpected character "
            f"{repr(ch)} "
            f"at {start}"
        )

    # ----------------------

    def tokenize(self):

        tokens = []

        while True:

            token = self.next_token()

            tokens.append(token)

            if token.type == TokenType.EOF:
                break

        return tokens


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    source = """
    import io

    fn main() {
        let x = 42
        let y = 3.14

        if x >= 10 {
            io.println("Hello Nova")
        }
    }
    """

    lexer = Lexer(source)

    for token in lexer.tokenize():
        print(token)


# ==========================================
# NOVA v0.5 (Part 2A)
# AST Nodes + Parser Skeleton
# Append below Part 1
# ==========================================

from dataclasses import dataclass, field
from typing import Optional, List, Any


# ==========================================
# AST BASE
# ==========================================

class ASTNode:
    pass


class Statement(ASTNode):
    pass


class Expression(ASTNode):
    pass


class Declaration(ASTNode):
    pass


# ==========================================
# PROGRAM
# ==========================================

@dataclass
class Program(ASTNode):
    imports: List[Any]
    declarations: List[Any]


# ==========================================
# IMPORTS
# ==========================================

@dataclass
class ImportDecl(Declaration):
    module: List[str]
    alias: Optional[str]


# ==========================================
# FUNCTIONS
# ==========================================

@dataclass
class Parameter(ASTNode):
    name: str
    type_name: Optional[str]


@dataclass
class FunctionDecl(Declaration):
    name: str
    parameters: List[Parameter]
    return_type: Optional[str]
    body: List[Statement]


# ==========================================
# VARIABLES
# ==========================================

@dataclass
class VariableDecl(Statement):
    mutable: bool
    constant: bool
    name: str
    declared_type: Optional[str]
    initializer: Optional[Expression]


# ==========================================
# STRUCTS
# ==========================================

@dataclass
class StructField(ASTNode):
    name: str
    type_name: str


@dataclass
class StructDecl(Declaration):
    name: str
    fields: List[StructField]


# ==========================================
# ENUMS
# ==========================================

@dataclass
class EnumVariant(ASTNode):
    name: str
    payload_types: List[str]


@dataclass
class EnumDecl(Declaration):
    name: str
    variants: List[EnumVariant]


# ==========================================
# BLOCKS
# ==========================================

@dataclass
class ReturnStmt(Statement):
    value: Optional[Expression]

@dataclass
class ExpressionStmt(Statement):
    expression: Expression


# ==========================================
# EXPRESSIONS
# ==========================================

@dataclass
class Identifier(Expression):
    name: str


@dataclass
class Literal(Expression):
    value: Any


@dataclass
class BinaryExpr(Expression):
    left: Expression
    operator: Token
    right: Expression

@dataclass
class BlockStmt:
    statements: list
    
@dataclass
class UnaryExpr(Expression):
    operator: Token
    operand: Expression


@dataclass
class GroupExpr(Expression):
    expression: Expression


@dataclass
class CallExpr(Expression):
    callee: Expression
    arguments: List[Expression]


@dataclass
class MemberExpr(Expression):
    object_expr: Expression
    member: str


@dataclass
class IndexExpr(Expression):
    object_expr: Expression
    index_expr: Expression


@dataclass
class ListExpr(Expression):
    elements: List[Expression]


@dataclass
class MapEntry(ASTNode):
    key: Expression
    value: Expression


@dataclass
class MapExpr(Expression):
    entries: List[MapEntry]


# ==========================================
# PARSER
# ==========================================

class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.current = 0

    # ======================================
    # TOKEN HELPERS
    # ======================================

    def peek(self):

        return self.tokens[self.current]

    def previous(self):

        return self.tokens[self.current - 1]

    def is_at_end(self):

        return (
            self.peek().type
            == TokenType.EOF
        )

    def advance(self):

        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def check(self, token_type):

        if self.is_at_end():
            return False

        return (
            self.peek().type
            == token_type
        )

    def match(self, *types):

        for token_type in types:

            if self.check(token_type):

                self.advance()

                return True

        return False

    def consume(self, token_type, message):

        if self.check(token_type):

            return self.advance()

        token = self.peek()

        raise NovaSyntaxError(
            f"{message} "
            f"at {token.position}"
        )

    # ======================================
    # PROGRAM
    # ======================================

    def parse(self):

        imports = []
        declarations = []

        while not self.is_at_end():

            if self.check(TokenType.IMPORT):

                imports.append(
                    self.parse_import()
                )

            else:

                declarations.append(
                    self.parse_declaration()
                )

        return Program(
            imports=imports,
            declarations=declarations
        )

    # ======================================
    # IMPORTS
    # ======================================

    def parse_import(self):

        self.consume(
            TokenType.IMPORT,
            "Expected 'import'"
        )

        module = []

        first = self.consume(
            TokenType.IDENTIFIER,
            "Expected module name"
        )

        module.append(first.value)

        while self.match(TokenType.DOT):

            part = self.consume(
                TokenType.IDENTIFIER,
                "Expected module part"
            )

            module.append(part.value)

        alias = None

        if self.match(TokenType.AS):

            alias = self.consume(
                TokenType.IDENTIFIER,
                "Expected alias"
            ).value

        return ImportDecl(
            module=module,
            alias=alias
        )

    # ======================================
    # DECLARATIONS
    # ======================================

    def parse_declaration(self):

        if self.check(TokenType.FN):

            return self.parse_function()

        if self.check(TokenType.STRUCT):

            return self.parse_struct()

        if self.check(TokenType.ENUM):

            return self.parse_enum()

        raise NovaSyntaxError(
            f"Unexpected token "
            f"{self.peek()}"
        )

    # ======================================
    # PLACEHOLDERS
    # Part 2B will implement these
    # ======================================
    def parse_function(self):
        self.consume(TokenType.FN, "Expected 'fn'")

        name = self.consume(
            TokenType.IDENTIFIER,
            "Expected function name"
        ).value

        self.consume(
            TokenType.LEFT_PAREN,
            "Expected '('"
        )

        parameters = []

        if not self.check(TokenType.RIGHT_PAREN):

            while True:

                param_name = self.consume(
                    TokenType.IDENTIFIER,
                    "Expected parameter name"
                ).value

                param_type = None

                if self.match(TokenType.COLON):

                    param_type = self.consume(
                        TokenType.IDENTIFIER,
                        "Expected type"
                    ).value

                parameters.append(
                    Parameter(
                        param_name,
                        param_type
                    )
                )

                if not self.match(TokenType.COMMA):
                    break

        self.consume(
            TokenType.RIGHT_PAREN,
            "Expected ')'"
        )

        return_type = None

        if self.match(TokenType.ARROW):

            return_type = self.consume(
                TokenType.IDENTIFIER,
                "Expected return type"
            ).value

        body = self.parse_block().statements

        return FunctionDecl(
            name=name,
            parameters=parameters,
            return_type=return_type,
            body=body
        )

    def parse_struct(self):

        self.consume(
            TokenType.STRUCT,
            "Expected 'struct'"
        )

        name = self.consume(
            TokenType.IDENTIFIER,
            "Expected struct name"
        ).value

        self.consume(
            TokenType.LEFT_BRACE,
            "Expected '{'"
        )

        fields = []

        while not self.check(TokenType.RIGHT_BRACE):

            field_name = self.consume(
                TokenType.IDENTIFIER,
                "Expected field name"
            ).value

            self.consume(
                TokenType.COLON,
                "Expected ':'"
            )

            field_type = self.consume(
                TokenType.IDENTIFIER,
                "Expected field type"
            ).value

            fields.append(
                StructField(
                    field_name,
                    field_type
                )
            )

            self.match(TokenType.COMMA)

        self.consume(
            TokenType.RIGHT_BRACE,
            "Expected '}'"
        )

        return StructDecl(
            name=name,
            fields=fields
        )

    def parse_enum(self):

        self.consume(
            TokenType.ENUM,
            "Expected 'enum'"
        )

        name = self.consume(
            TokenType.IDENTIFIER,
            "Expected enum name"
        ).value

        self.consume(
            TokenType.LEFT_BRACE,
            "Expected '{'"
        )

        variants = []

        while not self.check(TokenType.RIGHT_BRACE):

            variant_name = self.consume(
                TokenType.IDENTIFIER,
                "Expected variant"
            ).value

            variants.append(
                EnumVariant(
                    variant_name,
                    []
                )
            )

            self.match(TokenType.COMMA)

        self.consume(
            TokenType.RIGHT_BRACE,
            "Expected '}'"
        )

        return EnumDecl(
            name=name,
            variants=variants
        )

    def parse_block(self):

        self.consume(
            TokenType.LEFT_BRACE,
            "Expected '{'"
        )

        statements = []

        while (
            not self.check(TokenType.RIGHT_BRACE)
            and not self.is_at_end()
        ):
            statements.append(
                self.parse_statement()
            )

        self.consume(
            TokenType.RIGHT_BRACE,
            "Expected '}'"
        )

        return BlockStmt(
            statements
        )

    def parse_expression(self):

        token = self.advance()

        if token.type == TokenType.INTEGER:
            return Literal(int(token.value))
        if token.type == TokenType.FLOAT:
            return Literal(float(token.value))

    def parse_statement(self):
        # Placeholder for statement parsing
        pass


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    source = """
    import io
    import json as js

    fn main() {
    }
    """

    lexer = Lexer(source)

    tokens = lexer.tokenize()

    print("Before parser")

    parser = Parser(tokens)

    print("Parser created")

    program = parser.parse()

    print("Parser finished")

    print(program)
