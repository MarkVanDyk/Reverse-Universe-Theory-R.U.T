# README_repro

## RUT acoustic-horizon reproducibility packet

This packet reproduces the `rd190` soft-cap rerun discussed in the submission-style draft.

### Included files

- `RUT_Acoustic_Horizon_Submission_Style_with_Repro_Appendix.pdf`
- `RUT_Acoustic_Horizon_Merged_rd190_Equations_Draft.pdf`
- `results_JOINT_BplusC_expanded_rd190_softcap.json`
- `strict_test_v1.zip`
- `run_rd190_softcap.py`

## What this packet is for

This packet is intended to let an external reader rerun the stabilized `rd190` result and inspect the exact output used in the current RUT acoustic-horizon note.

## Expected result

The rerun should produce a best-fit point near:

- `r_d ≈ 181.75`
- `BIC ≈ 1485.44`

The local support band from the final scan should be approximately:

- `179.75 <= r_d <= 183.75` for `ΔBIC <= 2`

## Input packet

Use:

- `strict_test_v1.zip`

Extract it so that the script can access the `strict_test_v1` directory and its datasets.

## Main rerun script

Use:

- `run_rd190_softcap.py`

This script should:
- load the strict packet
- use the frozen-omega reference
- run the JOINT(B+C) expanded 10-parameter fit
- apply the soft-cap `rd190` setup
- save the output JSON

## Expected output file

The main output should be:

- `results_JOINT_BplusC_expanded_rd190_softcap.json`

## Notes on the rd190 setup

The `rd190` rerun differs from earlier cap-limited runs in two ways:

1. the upper `r_d` cap is relaxed from `180` to `190`
2. the hard boundary behavior is replaced by a smooth quadratic penalty

This is important because it tests whether the enlarged `r_d` preference is a real interior minimum or just a wall-chasing artifact.

## Suggested release asset names

Use a simple, explicit naming scheme:

- `RUT_Acoustic_Horizon_Submission_Style_with_Repro_Appendix.pdf`
- `RUT_Acoustic_Horizon_Merged_rd190_Equations_Draft.pdf`
- `RUT_rd190_stability_methods_results_and_L_prediction.pdf`
- `results_JOINT_BplusC_expanded_rd190_softcap.json`
- `strict_test_v1.zip`
- `run_rd190_softcap.py`
- `README_repro.md`

## Suggested short repository/release description

Reproducibility materials for the RUT acoustic-horizon rd190 soft-cap rerun, including the strict test packet, rerun script, expected JSON output, and paper-facing draft notes.

## Suggested commit message

Add rd190 soft-cap reproducibility packet, stability note, merged acoustic-horizon draft, and submission-style appendix.

## Suggested release title

RUT Acoustic Horizon Repro Packet — rd190 Soft-Cap Stability Run

## Suggested release notes

This release contains the current reproducibility packet for the RUT acoustic-horizon note.

Included:
- submission-style paper draft
- merged rd190 equations draft
- stability note
- strict test packet
- rerun script
- expected output JSON
- README with expected best-fit region

Key stabilized result:
- best-fit `r_d ≈ 181.75`
- support interval `≈ 179.75–183.75`
- enlarged-`r_d` preference remains after relaxed-cap and soft-penalty rerun
