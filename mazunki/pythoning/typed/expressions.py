#!/usr/bin/env python
# pkg(mazunki)/pythoning/typed/expressions.py

from typing import Any, Protocol
import ast, inspect, dis


class IllegalIteration(RuntimeError):
    def __init__(self, obj, extra=None):
        self.message = f"Iterating over {type(obj).__name__} is not permitted"
        if extra:
            self.message += f" (using {extra})"
        super().__init__(self.message)


class NotExpressableError(TypeError):
    def __init__(self, obj):
        super().__init__(f"{type(obj)} doesn't implement a __str__ function")


class Expressable(Protocol):
    def __str__(self) -> str: ...


class Expression:
    def __init__(self, text: Expressable):
        if self.implements_own_string(text):
            self.text = text
        else:
            raise NotExpressableError(text)

    @staticmethod
    def implements_own_string(text: Any):
        stringers = [
            stringer
            for stringer in text.__class__.mro()[:-1]
            if "__str__" in stringer.__dict__
        ]  # yeeting last element since it's guaranteed (i believe) to be 'object', and implements the default stringer
        return bool(stringers)

    def __iter__(self):
        return iter(self.text)

    def __str__(self):
        return str(self.text)


class LineVisitor(ast.NodeVisitor):
    def __init__(self, pos):
        self.pos = pos
        self.nodes = []

    def visit(self, node):
        if self.has_pos(node) and self.get_position(node) == self.pos:
            self.nodes.append(node)
        self.generic_visit(node)

    def has_pos(self, node):
        return all(
            hasattr(node, attr)
            for attr in ("lineno", "col_offset", "end_lineno", "end_col_offset")
        )

    def get_position(self, node):
        return node.lineno, node.end_lineno, node.col_offset, node.end_col_offset


class Parser:
    def __init__(self, source_code: str):
        self.tree = ast.parse(source_code)

    def find_nodes_at_line(self, pos: dis.Positions):
        visitor = LineVisitor(pos)
        visitor.visit(self.tree)

        return visitor.nodes

    def find_parent(self, node):
        for parent in ast.walk(self.tree):
            for child in ast.iter_child_nodes(parent):
                if child is node:
                    return parent


class LiteralExpression(Expression):
    def __init__(self, text: str):
        super().__init__(text)
        self._literal_text = text

    def __str__(self) -> str:
        if illegal := self._check_illegal_stack():
            raise IllegalIteration(self, illegal)
        return self._literal_text

    def _check_illegal_stack(self):
        stack = inspect.stack()
        restricted_functions = {"__iter__", "__getitem__", "__contains__"}
        for idx, frame_info in enumerate(stack):
            if frame_info.function in restricted_functions:
                return frame_info.function

            if frame_info.function == "__str__":
                for sub_frame in stack[idx + 1 :]:
                    if not sub_frame.code_context:
                        continue

                    if self._is_illegal_usage(sub_frame):
                        return sub_frame.function

    @staticmethod
    def _is_illegal_usage(frame_info: inspect.FrameInfo) -> bool:
        filename = frame_info.filename
        pos = frame_info.positions
        if not pos:
            return False

        with open(filename, "r") as file:
            lines = file.read()

        parser = Parser(lines)
        nodes = parser.find_nodes_at_line(pos)
        for node in nodes:
            parent = parser.find_parent(node)
            if isinstance(parent, ast.For):
                return True
        return False

    def __iter__(self):
        raise IllegalIteration(self, self._check_illegal_stack())

    def __getitem__(self, _):
        raise IllegalIteration(self, self._check_illegal_stack())

    def __contains__(self, _):
        raise IllegalIteration(self, self._check_illegal_stack())


def test_loop_allocation(expr):
    for _ in str(expr):
        pass


def test_iteration(expr):
    for _ in expr:
        pass


def test_indexing(expr):
    expr[0]


def test_container(expr):
    _ = "a" in expr


for test in test_loop_allocation, test_iteration, test_indexing, test_container:
    try:
        expr = LiteralExpression("hello")
        test(expr)
    except IllegalIteration as e:
        print(e)

#  vim: set sw=4 ts=4 expandtab
