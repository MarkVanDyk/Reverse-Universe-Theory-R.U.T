# JOINT(B+C) bS-priority near-frozen dynamic-ω result

This release documents the current strongest controlled numerical result in the JOINT(B+C) pipeline.

## Summary
In the present test setup, the best-performing model is a **near-frozen dynamic-ω formulation** with:

- **bS-priority freedom**
- **bC anchored near the frozen-reference value**
- **small, smooth ω evolution**
- **local robustness around the best-fit basin**

Within this pipeline, this configuration outperforms the tested benchmark models by BIC.

## Current comparison
- **ΛCDM**: 1691.76
- **w0waCDM**: 1693.21
- **Frozen-ω RUT**: 1717.43
- **Dynamic-ω, bS-priority near-frozen full refit**: 1513.09

## Best-fit point
- **H0** = 89.6086
- **Ωm** = 0.2840
- **rd** = 169.9994
- **σ8,0** = 0.4689
- **bC** = 0.004743
- **bS** = 0.119588
- **μ** = 0.099521
- **ω0** = 26.3438
- **ωinit** = 26.2996
- **ω′init** = -0.00429

## Local robustness
A local robustness test around the best-fit point repeatedly returned the same numerical basin.

- **Reference BIC**: 1513.0878
- **Best local BIC**: 1513.0391
- **Worst local BIC**: 1513.5919
- **Mean local BIC**: 1513.0979
- **Std. dev.**: 0.1407

## Interpretation
The current numerical pattern across the test ladder is coherent:

- frozen ω appears too rigid
- fully free dynamics appear too loose
- a near-frozen dynamic-ω regime performs best
- the strongest controlled improvement currently appears when the **sine-channel freedom** is allowed to move more than the cosine-channel freedom

## Caveat
This is a **controlled pipeline result**, not final proof. Remaining work includes:

- boundary-sensitivity testing
- stronger growth/RSD treatment
- fresh-environment replication
- additional cross-checks on priors and parameter bounds

## Files in this release
- reviewer summary PDF
- reviewer/layman summary PDFs
- local robustness summary text
