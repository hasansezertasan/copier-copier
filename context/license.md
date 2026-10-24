# License

## Keep LICENSE out of cobo

**Id:** 5324f2ab-c523-4084-8d0f-61b090c73393
**Type:** decision
**Status:** active
**Evidence:** confirmed
**Source:** `docs/adr/0003-license-is-not-managed-by-cobo.md`
**Revisit when:** cobo can write a license without a fence, or the license text stops being vendored in `template/LICENSE.jinja`

`LICENSE` stays a hand-maintained template (`template/LICENSE.jinja`, MIT or
Apache-2.0), unlike `.gitignore`, `.gitattributes` and `.editorconfig`, which
cobo generates and seals.

**Reason:** `cobo licenses dump` writes its fence into the license file, which
corrupts the text and can defeat license detection, and the MIT text arrives
with its year and copyright holders unfilled. Filling those in breaks the
seal, so the file could never pass `cobo check`. The copyright line now
carries the start year, the author and the contact, so there is nothing left
for cobo to manage.

**Rejected alternative:** strip the fence at generation time. Yields a clean
file, but the seal is gone, so cobo no longer manages it and the extra step
buys nothing.

**Rejected alternative:** use cobo only as a one-time source for the license
text. Possible, but the text changes rarely and is already vendored, and it
adds a manual regeneration step with no drift check.
