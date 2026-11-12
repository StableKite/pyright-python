# Callable fields that override inherited methods

A callback protocol can describe a bound method precisely, including its keyword
names, positional parameters, overloads and generic return types. A pure instance
field with that protocol type can safely replace a compatible inherited method:

```python
from typing import Protocol


class Writer(Protocol):
    def __call__(self, *, data: bytes) -> int: ...


class Parent:
    def push(self, *, data: bytes) -> int:
        return len(data)


class Child(Parent):
    def __init__(self) -> None:
        self.push: Writer = self._selected

    def _selected(self, *, data: bytes) -> int:
        return len(data)
```

The field is declared through `self.push`, without a class-body declaration.
`Child.push` still resolves to the inherited method descriptor. Calling it through
the class therefore requires a receiver, just as `Parent.push` does. Assigning a
callback object to `Child.push`, including through `cls.push` in a class method,
must still be rejected.

In Pyright's documented storage model, `push: Writer` in the class body is a
regular class variable, even without an initial value. This change preserves its
existing incompatible-override diagnostic. It does not change class attribute
lookup, introduce descriptors, or reinterpret class annotations as slots.

The checker compares the callable field against the inherited method after
binding its receiver. Class and method type parameters remain universally
quantified, and `Self` remains polymorphic across further subclasses. Normal
callable assignment checks enforce parameter variance, return variance, keyword
names, optional arguments and complete overload coverage. Final methods,
abstract methods, special methods, explicit `ClassVar` declarations and slot
descriptors retain their existing checks.

## Generic aliases in instance member annotations

An independent evaluator fix permits an alias's own formal type parameters while
resolving the alias name, before its supplied arguments have been substituted:

```python
type Identity[T] = T


class Box:
    def __init__(self) -> None:
        self.value: Identity[int] = 1
```

The annotation has type `int`. Actual method-scoped arguments still cannot escape
into an instance member type. Alias bounds, argument counts, incompatible
assignments and missing arguments retain their diagnostics.

## Regression scope

Classification B: checker/evaluator limitations. No typeshed change is involved.
No existing tests, expected types, diagnostic rules or suppressions are changed.
The new suites cover 43 callable/storage cases and 12 alias scope cases, including
strict negative cases and `assert_type` checks for alias precision.

References: the existing [class and instance variable documentation](https://github.com/StableKite/pyright/blob/43cfb286744a6481c2ef78e327e984ab4ecaa6ae/docs/type-concepts-advanced.md#class-and-instance-variables)
and the [typing specification for class compatibility](https://typing.python.org/en/latest/spec/class-compat.html).
