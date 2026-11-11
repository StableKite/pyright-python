# StableKite native type contract review

This branch bundles the source-built Pyright `1.1.414-stablekite.2` engine
with precise native ctypes and standard pickle contracts.
The Python package version is `1.1.414+stablekite.2`.

The handler receives the converted Python result, the ctypes function,
and a tuple of Python arguments. It can return an arbitrary Python object.
Its callable shape remains checked. The default getter returns `None`;
assigning `None` is rejected, while deleting the handler restores the default.

The real `byref` result retains the concrete CData owner type through a
read-only covariant owner property. Other ctypes converters retain the safe
`object` default because their owners can be bytes or None. The standard
pickle reduction includes its sixth state-setter argument and the
`NotImplemented` result of `reducer_override`.

`vendor/PYRIGHT_NODE.json` records the exact source commit, archive hash,
and every bundled file hash. The normal setuptools build verifies this
archive and includes its files in both wheel and sdist. Normal execution
uses the bundled engine; no installed SDK file is patched.

The upstream checker engine and original tests are unchanged. The local
source producer passed the original style checks, workspace typechecks,
and all 77 Jest suites (2,793 tests), retaining the upstream `--forceExit`
option and its original process cleanup warnings. Real ctypes callback
consumers are qualified separately from those checker unit tests.

This remains a review branch while the required original remote CI and
ordinary consumers are qualified for these exact sources. No upstream issue,
pull request, package index release, default promotion, or Root SDK change
is part of this review.
