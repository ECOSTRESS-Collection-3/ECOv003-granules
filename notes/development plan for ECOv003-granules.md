# ECOv003-granules Collection 3 Compatibility Development Plan

**Status:** Proposed  
**Prepared:** 2026-11-09  
**Target repository:** `ECOSTRESS-Collection-3/ECOv003-granules`

## 1. Objective

Make the `ECOv003-granules` public API correctly recognize and open the Collection 3 granule products currently published through CMR, expose consistent product metadata and layer files, and support the on-disk formats used by Collection 3 download clients.

The package should return a valid granule object for each supported Collection 3 product, or raise a clear, actionable error for unsupported or malformed inputs. Existing supported products and ZIP-based workflows must continue to work.

## 2. Scope and Findings

The following compatibility gaps were observed in version 1.13.2:

| Area | Observed behavior | Desired behavior |
|---|---|---|
| `L1CT_RAD` dispatch | `open_granule.py` checks for `L1CT_RED`, while current CMR granule names use `L1CT_RAD`. | Dispatch current `L1CT_RAD` names to the appropriate granule implementation. |
| `L3T_ETAUX` support | The dispatcher has no `L3T_ETAUX` route. | Add a suitable granule implementation or adapter with valid metadata and layer-file access. |
| STARS product metadata | The generic product-name parser assumes the standard tiled granule ID layout and produces an incorrect value for STARS IDs. | Return the canonical `L2T_STARS` product name for STARS granules. |
| Directory-backed granules | `tiled_granule.filenames` always attempts to open the product path as a ZIP archive. | Support granules stored as directories, while retaining ZIP support if it is part of the public interface. |
| Unsupported dispatch and messages | Unknown names can return `None`; some dispatcher log messages still refer to Collection 2. | Report unsupported input explicitly and use accurate Collection 3 terminology. |

These are package-level findings. Standard-product metadata parsed from normal granule directory names was not found to be incorrect. Passing an individual TIFF path as the granule identifier was not established as a supported input and should not be treated as a confirmed defect without checking the documented API contract.

## 3. Implementation Phases

### Phase 1: Confirm the Public Contract

- [ ] Document accepted inputs to `open_granule`: ZIP archive, extracted granule directory, or other supported form.
- [ ] Confirm the expected return type and metadata properties for each supported product.
- [ ] Confirm whether `filenames`, `variables`, and layer filename/path properties must behave identically for ZIP and directory inputs.
- [ ] Record representative current CMR granule IDs and expected product metadata for all seven products: `L1CT_RAD`, `L2T_LSTE`, `L2T_STARS`, `L3T_ETAUX`, `L3T_JET`, `L4T_ESI`, and `L4T_WUE`.

### Phase 2: Correct Product Dispatch and Metadata

- [ ] Correct `L1CT_RAD` dispatch and add regression coverage for the exact Collection 3 prefix.
- [ ] Implement `L3T_ETAUX` support using the appropriate existing base class or a dedicated class; verify its metadata and layer discovery.
- [ ] Override STARS product metadata so its canonical product name is returned independently of the standard tiled ID parser.
- [ ] Make unknown or malformed product names raise the package-standard explicit exception rather than returning `None`.
- [ ] Update stale Collection 2 log messages and messages affected by the new dispatch behavior.

### Phase 3: Support Directory and Archive File Discovery

- [ ] Update file discovery to enumerate TIFF layers from an extracted granule directory.
- [ ] Preserve ZIP-backed behavior if ZIP archives are a supported input.
- [ ] Ensure `filenames`, `variables`, and layer path properties agree on the available files for both supported storage forms.
- [ ] Define and test behavior for missing directories, empty granules, and malformed archives with clear errors.

### Phase 4: Tests and Documentation

- [ ] Add focused dispatcher tests for all seven supported product prefixes, including `L1CT_RAD` and `L3T_ETAUX`.
- [ ] Add a STARS regression test asserting its canonical product metadata.
- [ ] Add directory-backed and ZIP-backed file-discovery tests using small fixtures; avoid network-dependent tests.
- [ ] Test explicit failures for unknown products and invalid granule paths.
- [ ] Document supported Collection 3 products, accepted input formats, and layer-discovery behavior.
- [ ] Run the package test suite, lint/type checks used by the repository, and packaging/build checks.

### Phase 5: Release and Integration Validation

- [ ] Confirm the supported Collection 3 behavior against representative CMR granule names.
- [ ] Validate opening at least one authenticated Collection 3 download for each newly supported product when access and representative data are available.
- [ ] Verify backward compatibility for existing product classes and ZIP users.
- [ ] Publish a release containing the fixes and note any input-format or error-behavior changes.
- [ ] Update dependent clients to use the released package version and remove local workarounds where appropriate.

## 4. Acceptance Criteria

The work is complete when:

1. `open_granule` recognizes all seven Collection 3 product names and returns a usable object for each.
2. `L1CT_RAD`, `L3T_ETAUX`, and STARS have regression tests covering dispatch and canonical product metadata.
3. Directory-backed granules expose their TIFF layers and variables without attempting to open a directory as a ZIP archive.
4. Existing supported ZIP workflows remain functional, or the documented input contract is intentionally changed with tests and release notes.
5. Unknown products and invalid inputs produce clear, explicit errors.
6. Tests and package build checks pass, and the supported API is documented.

## 5. Out of Scope and Risks

- This plan does not change `ECOv003-CMR` CMR search behavior or its point-sampling implementation.
- It does not assume that individual TIFF paths are valid granule inputs; that depends on the public API contract confirmed in Phase 1.
- ETAUX may have product-specific metadata or layer conventions that differ from the existing tiled products. Confirm those conventions before choosing a base class or exposing properties.
- Authenticated end-to-end downloads can be gated by credentials and data availability; fixture-based regression tests should remain the primary CI coverage.

## 6. Relevant Source Files

- `ECOv003_granules/open_granule.py` — product dispatch and unsupported-name handling.
- `ECOv003_granules/tiled_granule.py` — common tiled metadata and layer-file discovery.
- `ECOv003_granules/L2TSTARS.py` — STARS-specific metadata behavior.
