# StableKite ctypes contract review

This branch bundles the source-built Pyright `1.1.414-stablekite.1` engine
with a correction to the vendored `ctypes.CFuncPtr.errcheck` contract.
The Python package version is `1.1.414+stablekite.1`.

The handler receives the converted Python result, the ctypes function,
and a tuple of Python arguments. It can return an arbitrary Python object.
Its callable shape remains checked. The default getter returns `None`;
assigning `None` is rejected, while deleting the handler restores the default.

`vendor/PYRIGHT_NODE.json` records the exact source commit, archive hash,
and every bundled file hash. The normal setuptools build verifies this
archive and includes its files in both wheel and sdist. Normal execution
uses the bundled engine; no installed SDK file is patched.

The upstream checker engine and original tests are unchanged. The local
source producer passed the original style checks, workspace typechecks,
and all 77 Jest suites (2,793 tests), retaining the upstream `--forceExit`
option and its original process cleanup warnings. Real ctypes callback
consumers are qualified separately from those checker unit tests.

This remains a review branch. The required remote CI and ordinary default
delivery have not been declared complete while GitHub Actions capacity is
blocked. No upstream issue, pull request, package index release, or Root
SDK modification is part of this review.
