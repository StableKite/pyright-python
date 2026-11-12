# StableKite native type contract review

This branch bundles the source-built Pyright `1.1.414-stablekite.4` engine
with compatible callable instance overrides, nominal metaclass class-object
bounds and correct super binding, while
preserving precise native ctypes and standard pickle contracts.
The Python package version is `1.1.414+stablekite.4`.

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

The checker engine now validates known nominal metaclass owner bounds,
looks up super through the metaclass MRO while preserving the class object,
and rejects invalid custom getter binding. Broad Enum bounds that do not
guarantee the custom metaclass remain rejected. The producer implementation
returning super().__getitem__(key.upper()) is unchanged.

All original Pyright tests and expectations are unchanged. The preceding
five metaclass tests remain intact. Twenty-eight additional strict tests
cover callable instance overrides, full parameter and result contracts,
polymorphic Self, generics, overloads, and descriptor counterexamples.
The source passed all 79 Jest suites (2,826 tests), TypeScript, syncpack,
ESLint and Prettier checks. Original process cleanup warnings are retained.
The original remote workflow and fresh installed consumers remain separate
gates for this exact source and bundle.

This remains a review branch while the required original remote CI and
ordinary consumers are qualified for these exact sources. No upstream issue,
pull request, package index release, default promotion, or Root SDK change
is part of this review.
