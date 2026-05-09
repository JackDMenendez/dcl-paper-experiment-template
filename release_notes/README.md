# release_notes/

One file per released version. Two files per release:

- `vX.Y.md` -- the **change log** for this release. Long-form,
  internal: what changed, why, what's deferred, bibliography
  additions, reproducibility instructions. This is the file the paper
  references from `release_notes/vX.Y.md`.
- `vX.Y-release-message.md` -- the **GitHub Release body**. The
  outward-facing version: headline change, audit-status delta, what's
  out of scope. Posted as the body of the GitHub Release alongside
  the tag.

Templates:

- `TEMPLATE.md` for the change log
- `TEMPLATE-release-message.md` for the Release body

## Release flow

1. Final commits land on `main`; CI green.
2. Update `CITATION.cff` (`version`, `date-released`).
3. Draft `release_notes/vX.Y.md` and `release_notes/vX.Y-release-message.md`.
4. **Deposit on Zenodo first to get the DOI.** Do not commit the
   version bump until the DOI is in hand -- the DOI lands in the
   `\thanks{}` block on the title page and in `CITATION.cff`.
5. Commit the version bump (DOI included) with the change log.
6. Tag `vX.Y` and push the tag.
7. Create the GitHub Release using the `vX.Y-release-message.md` body.

For the *prior* release flow record on the parent project, see the
git history of the source repository this template was derived from.
