## PDF document ladder
Current reviewer-facing set: Quick Reviewer Brief v6, Reviewer Packet v4, and Full Scientific Summary v7. Older reviewer summaries are retained in archive_old_versions for version history and should not be used as the active reviewer set.

## Current Benchmark Status — May 2026

Reverse Universe Theory (R.U.T.) is currently best described as a **structured, benchmark-facing research program** with a reproducible pilot signal in the growth-lensing sector.

The strongest current result comes from the **Sprint A+B+C / Sprint C-H E_G replication packet**. In that packet, the fixed neutral-lensing RUT bridge,

\[
B(a)=\frac12\left[1+\tanh\left(\frac{a-a_t}{\Delta a}\right)\right],
\]

\[
\mu(a)=1+\mu_0B(a),
\]

\[
\Sigma(a)=1,
\]

shows a weak but hardened pilot advantage over LambdaCDM in E_G-style growth-lensing comparisons.

### Key benchmark results

| Stage | Test | Result | Interpretation |
|---|---|---:|---|
| Sprint A | Background real data | ΔBIC ≈ +3.7 | LambdaCDM preferred |
| Sprint B | Joint background + growth | ΔBIC ≈ +3.63; μ₀ ≈ 0.173 | Mild growth hint, not BIC-supported |
| Sprint C | Pilot multi-point E_G | ΔBIC ≈ -2.108 | First weak RUT advantage |
| Sprint C-H | One-per-family E_G | ΔBIC ≈ -1.926 | Survives family reduction |
| Sprint C-H | Family-weighted E_G | ΔBIC ≈ -1.963 | Survives weighting |
| Sprint C-H | Leave-one-point-out jackknife | Win fraction = 1.0; worst ΔBIC ≈ -1.266 | No single point carries the result |

### Current strongest reviewer-facing claim

Fixed neutral-lensing RUT shows a reproducible pilot advantage over LambdaCDM in E_G-style growth-lensing comparisons within the documented benchmark setting. This is treated as a **bounded pilot result**, not a claim of final cosmological replacement.

### Current interpretation

The current E_G result suggests a possible **growth-lensing asymmetry**:

\[
\mu(a)>1,\qquad \Sigma(a)\approx1.
\]

In plain terms, the pilot signal points toward **enhanced matter-growth response with near-neutral lensing response**. RUT interprets this as a possible bridge-regulated separation between the matter-response channel and the light-path/lensing channel.

### Current evidence level

This is **not a confirmed detection**. The current E_G compilation uses diagonal errors only. Some measurements may overlap in survey data or methodology, and full covariance matrices have not yet been incorporated.

Current conservative status:

> **Tier-4-style testing pipeline with weak but hardened pilot evidence emerging in the E_G / growth-lensing sector.**

### Next required test

The next benchmark gate is:

> **Sprint C-H2: covariance-clean E_G / holdout test**

A stronger result would require the fixed neutral-lensing RUT bridge to remain favored after covariance control, survey-family auditing, and frozen-model holdout testing.

### Replication

The replication packet includes stored result tables and a verification script:

```bash
python scripts/verify_results.py

- [Quick Reviewer Brief](docs/reviewer-packets/) — short first-contact overview
- [Reviewer Packet](docs/reviewer-packets/) — mid-length technical review version
- [Full Scientific Summary](docs/reviewer-packets/) — complete long-form scientific packet

## Reverse Universe Theory — JOINT(B+C) Benchmark Update

## Latest benchmark update
See the latest release: **RUT v7.1 — JOINT(B+C) Benchmark Update**
<img width="989" height="590" alt="output (21)" src="https://github.com/user-attachments/assets/78629236-9010-4c5e-98c4-1a87ab1d76b0" />

| Model | Best score |
|---|---:|
| Expanded RUT | 1485.4368 |
| Flat w0waCDM | 1584.8104 |
| LCDM | 1602.5264 |

## Latest benchmark update

The latest benchmark milestone is documented in the release:

**RUT v7.1 — JOINT(B+C) Benchmark Update**

### Refined benchmark summary

| Model | Best score |
|---|---:|
| Expanded RUT | 1485.4368 |
| Flat w0waCDM | 1584.8104 |
| LCDM | 1602.5264 |

In the current matched JOINT(B+C) pipeline, the refined expanded RUT solution is the strongest-performing tested model so far.

This should be interpreted as a matched pipeline benchmark result within the current setup, not yet as a final universal cosmology verdict.

This release documents the current JOINT(B+C) benchmark milestone for the constrained dynamic-omega / bS-priority pipeline.

### Main result
In the current matched JOINT(B+C) workflow, the refined expanded RUT solution currently outperforms the matched control models tested so far.

### Refined benchmark summary
- **Expanded RUT**: BIC ≈ **1485.4368**
- **Flat w0waCDM**: BIC ≈ **1584.8104**
- **LCDM**: BIC ≈ **1602.5264**

### Current preferred regions
- **RUT**: refined interior optimum near **r_d ≈ 181.72**
- **w0waCDM**: refined local optimum near **r_d ≈ 187.10**
- **LCDM**: refined local optimum near **r_d ≈ 186.05**

### Current interpretation
Within the present matched JOINT(B+C) pipeline, RUT is the strongest-performing tested model so far. This should be interpreted as a pipeline benchmark result, not yet as a final universal cosmology verdict.

### Included in this update
- JOINT(B+C) benchmark summaries
- release-facing result notes
- refined comparison writeups for RUT vs LCDM vs w0waCDM
- supporting notes for the current constrained dynamic-omega result
## Reviewer Quickstart (STRICT v2.1)
- Zenodo DOI: https://doi.org/10.5281/zenodo.18854340
- Git tag: strict-v2-2026-03-01.1
- What this is: penalty-aware ΛCDM vs RUT comparison with ω/bC/bS frozen from Dataset A and held on independent datasets.
- Start here: docs/replication/Replication_Packet_v1_RUT_Strict_Test_v2.pdf
- Must-match gate: docs/replication/STRICTv2_MustMatch_Checklist_1page.pdf
- Evidence archive: evidence/strict-v2-2026-03-01.1/ (or release asset zip)
- Outputs: strict_test_v1/results_datasetB/, results_datasetC/, results_joint/
- Falsifiers: docs/replication/RUT_Falsifiers.pdf
Reverse Universe Theory (RUT) is tested here using a skeptic-friendly, pre-registered pipeline. The
goal is not rhetorical persuasion; the goal is replication under locked rules.
What this repo contains
• A locked baseline + residual-domain search in ln(1+z), with a required cross-check in ln(a).
• A bounded structured term: f(z) = 1 + A·sin(ω·ln(1+z)+φ0), |A| ≤ 0.2.
• Penalty-aware evaluation (χ², AIC, BIC) and out-of-sample validation (k-fold CV / holdout).
• Cross-probe rule: infer ω on H(z), then fix ω when testing SNe (no ω retuning on SNe).
• Stability checks and null tests (shuffle/phase randomization).
Pass / Fail (pre-registered)
• Pass (provisional): cross-probe ω consistency + penalty-aware improvement + stability + nulls fail to
reproduce.
• Fail (hard): replication fails across probes and stability repeatedly fails. Stop tuning; record the run.
Quickstart
1) Run baseline fit → 2) compute residuals → 3) fit structured term → 4) stability + nulls → 5) OOS /
holdout → 6) log result.
- PDF: [Chapter12_Closing_and_Evidence_Master_v11_clean.pdf](docs/replication/Chapter12_Closing_and_Evidence_Master_v11_clean.pdf)
# Reverse-Universe-Theory-R.U.T
A novel cosmological framework linking the direction of time to light expansion and contraction.
Duality Claims v0.2 — DOI:10.17605/OSF.IO/Y6GZP
Claim Index Addendum v0.2 — DOI:10.17605/OSF.IO/Y6GZP
Add OSF DOIs for priority disclosures
Zenodo DOI: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18676060.svg)](https://doi.org/10.5281/zenodo.18676060)
  https://doi.org/10.5281/zenodo.18676060
  Replication Packet (Evidence Appendix) DOI: 10.5281/zenodo.18676786
## Replication Packet (Evidence Appendix) DOI: 10.5281/zenodo.18676786

**Chapter 12 – Closing + Evidence Summary (v11 clean):**  
- PDF: `docs/replication/Chapter12_Closing_and_Evidence_Master_v11_clean.pdf`

### What this contains
- Decision-grade result: **STRICT FULL-COV CC (BC03), ω locked (N=15)**
- Model comparison (BIC): **ΔBIC(M0 − M3E) = +3.578** (BIC favors M3E over M0)
- Included: dataset QR links (direct URLs) + BC03 subset table for exact replication

### Quickstart
1. Open the PDF above.
2. Scan/download the datasets from the QR links.
3. Run the STRICT FULL-COV pipeline (ω locked) on the BC03 CC subset (N=15).
4. Confirm the reported **ΔBIC** and residual behavior.

### DOI (Zenodo)
- Version DOI: https://doi.org/10.5281/zenodo.18676060
- Concept DOI: **(add after release)**
## Evidence Packet (Chapter 12)
Zenodo DOI (latest): https://doi.org/10.5281/zenodo.18677303

## Priority Note (Duality Laws)
Zenodo DOI: https://doi.org/10.5281/zenodo.18676060
