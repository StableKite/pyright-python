# Constructor results

Version: `1.1.414-stablekite.6`. Base: StableKite 5 engine,
`c8698ccb7e22daa0c1a963c12f4cc7332fa284b7`.

The normative reference is the
[typing constructor specification](https://typing.python.org/en/latest/spec/constructors.html).

An explicit unrelated `__new__` result bypasses `__init__`. Constructor
signature consistency now compares only stages that can participate in the
same call. A returned concrete subclass uses its applicable initializer.
Mixed overloads retain consistency validation on their related branches.
The previous policy for overloaded declarations without an implementation
is retained, including the built-in `type.__new__` declarations.

Abstract usage is checked after the actual constructor result is evaluated.
An abstract facade returning an unrelated concrete resource is accepted;
an actual abstract allocation remains an error. Custom metaclass `__call__`
results and related concrete subclasses are also considered. Protocol
instantiation checks retain their existing policy.

An argument error in a `__new__` with a declared unrelated return does not
turn its result into an allocation of the facade. Its real argument errors
are retained without cascading through an inapplicable initializer.
`Never` bypasses initialization, including constructor-to-callable analysis.

Four added strict tests preserve the primary real Python programs and
cover generic, union, protocol, callable, literal, `None`, explicit `Any`,
`Never`, overload, metaclass, abstract and genuine bad argument/body controls.
Strict constructor consistency remains enabled. The original programs and
expected diagnostics are unchanged. All 80 suites and 2,837 tests pass
(2,833 previous plus four added), along with the original source style and
TypeScript checks.

Separate stock CPython 3.13/3.15 executions on Windows and Linux verify the
actual return and initializer behavior. The mixed-union related runtime
branch calls its initializer; its unrelated branch does not. Distribution
and CI qualification are recorded separately.

The new primary positive fixture omits only one explicitly authorized,
redundant EOF LF. A separate SHA256 and complete AST/coordinate ledger records
that precise delta; all remaining bytes and all other input programs are exact.

The earlier StableKite 5 wrapper macOS capacity hold remains unchanged.
This is a distinct source revision requiring its own complete qualification;
it does not promote a default or retry the earlier unchanged runs.
