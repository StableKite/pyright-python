# Keyword-only override compatibility

This candidate is based on accepted StableKite 3, commit
`5d6b01c2ac6e464d74bd762cb961adf708a65897`. It retains its native ctypes,
out-parameter, callable and metaclass contracts. The unaccepted pure-instance
callable candidate 4 remains separate and on hold; none of its changes are
included here.

A base method accepting a keyword-only argument can be implemented by a method
whose corresponding parameter also accepts a positional argument. The keyword
name, contravariant parameter type and optionality still have to match. The
[typing specification](https://typing.python.org/en/latest/spec/callables.html#parameter-kinds)
defines this relationship. The implementation previously searched only the
override's keyword-only parameters and incorrectly reported a standard parameter
as missing.

The override comparison now searches standard and keyword-only parameters by
name. A required standard parameter corresponding to a required base keyword is
not an additional required argument. Existing type and default checks apply to
the matched parameter. A standard parameter cannot consume both a base positional
argument and a keyword: the comparison rejects an already occupied positional
slot or a collision with arbitrary base varargs, even if the override has
`**kwargs`. Positional-only parameters remain ineligible for a named match;
the existing real `**kwargs` fallback remains available. A `Never` varargs item
admits no additional positional value, so that empty variadic case does not
create a collision.

Thirty-five new strict tests verify exact error lines: 18 valid and 17 invalid
examples cover optional and required parameters, same and different orders,
additional optional arguments, static/class/generic methods, callable protocols,
plain Callable, type/default/name errors, positional-only restrictions and
multiple-value collisions. The 18 valid examples run as ordinary Python programs
under CPython 3.15.2t with the GIL naturally off. Eight invalid calls actually
raise TypeError in separate runtime controls.

Independent installed accepted Pyright 3 and Mypy 4 comparisons are preserved
outside the producer. Both reject the valid Never-varargs override; this candidate
accepts it because a value of Never cannot supply the conflicting position.
The other 17 positive cases agree with Mypy 4. All 17 negative cases are rejected
by Mypy 4. Accepted Pyright 3 also misses the actual occupied-position collision
when `**kwargs` exists; this candidate retains that error instead of weakening
the check. This report does not present agreement with another checker as a
substitute for Python call semantics or the specification.

All previous 1,768 test files and expectations are byte-identical. The complete
79-suite, 2,833-test local run passes, as do the original TypeScript, syncpack,
ESLint and Prettier checks. No typeshed, rules, per-project name exceptions,
Any, cast or diagnostic suppression is added. Remote CI, packaging and installed
consumers are separate acceptance gates; local success does not qualify a default
branch change.
