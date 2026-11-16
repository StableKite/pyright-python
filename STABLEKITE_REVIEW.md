# StableKite descriptor assignment review 7

This branch bundles source-built Pyright `1.1.414-stablekite.7`; the Python wrapper is `1.1.414+stablekite.7`. Engine source: `7cf26624313966738e0496741b6c7b4bb5332b43`, based on accepted engine6 `8f587d5ba8d7b5e98973460348c18c57493f7593`. Wrapper base: accepted6 `e15b94c28abd7392b8a040c783ea099e5db5bf3a`.

An instance assignment shadows a non-data descriptor. Subsequent reads return the replacement directly, without binding a stored function again. Previously Pyright compared replacements with the raw descriptor, rejecting a compatible bound method while accepting an incompatible unbound method.

The evaluator now checks replacements against the specialized instance `__get__` result and supplies this type for contextual inference. Data descriptors, delete-only descriptors, properties, class writes, frozen classes, slots, ClassVar and Final retain their separate restrictions. A non-data descriptor cannot be shadowed without an instance dictionary, including when it hides an inherited slot.

Local source checks passed 81 suites / 2840 tests, full TypeScript and full style checks. All original2837 cases remain. One explicitly reviewed false expectation changed: MemberAccess6 originally expected two errors for valid str replacements of Column[str]; it now expects zero. Its Python statements/declarations are AST-identical. Four separate strict negatives check incompatible int replacements of declared/inferred fields and invalid class writes, including exact diagnostic lines and rules. Every other original expectation is unchanged.

All52 accepted external programs retain their complete diagnostic objects. New controls cover original bound/unbound reproductions, inherited generics, contextual lambdas, wrong returns/arguments, real setter/deleter boundaries, properties, ClassVar, Final, frozen instances and slots. Actual Python3.15t programs retain natural GIL-disabled state.

All accepted6 engine fixes remain. All5410 bundled typeshed files match the accepted capsule byte for byte. The standard build helper verifies the production npm archive and every bundled file. Full original CI and installed-form qualification have independent receipts; this local source result alone does not establish their completion.

This remains a review branch. Existing defaults, accepted6 packages, package indexes and Root SDK remain unchanged until independent acceptance. Earlier engine changes remain documented in STABLEKITE_NATIVE_TYPING_V2.md, STABLEKITE_KEYWORD_ONLY_OVERRIDES.md and STABLEKITE_CONSTRUCTOR_RESULTS.md.
