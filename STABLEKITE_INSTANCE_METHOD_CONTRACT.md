# Instance callable contracts

An ordinary method and an explicitly annotated callable stored on an instance
have distinct lookup behavior. Instance lookup uses the writable annotation;
class lookup and `super` retain the original function and its receiver.

The redeclaration exemption requires a fully known callable contract compatible
in both directions with the bound method. Callback protocols retain their named
parameters. Mutable overrides remain invariant. Explicit variant type variables,
`Self` results, unknown signatures, properties, final methods, frozen instances,
and classes without instance dictionaries do not gain writable-method permission.
Assignments through aliases retain the declared instance contract.

An explicit generic `type[T]` receiver of an ordinary custom-metaclass method
also carries the declaring metaclass requirement. This requirement is checked
for manual calls and callable assignments, including forwarding and partial
application. It applies to the class object, not to values constructed from it.
An unconstrained `type[T]` return annotation does not gain a metaclass guarantee
from a qualified argument.
Zero-argument `super` requires a positional parameter.

Regression samples cover class and instance lookup, protocols, inherited fields,
writable overrides, aliases, readonly boundaries, generic metaclass results,
manual receiver rejection, and keyword-only `super`. Existing tests and checker
configuration are preserved.
