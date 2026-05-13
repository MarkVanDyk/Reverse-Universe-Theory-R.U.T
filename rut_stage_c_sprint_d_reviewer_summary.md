RUT/M1a Reviewer Summary: Stage C + Sprint D

Status: Preliminary research summary for review, replication, and falsification-oriented development.
Model: Reverse Universe Theory / M1a frozen late-time bridge
Author: Mark “Question Mark” Van Dyk
Archive context: GitHub / OSF research packet

1. Purpose

This summary documents the current reviewer-facing status of the RUT/M1a perturbation program after Stage C and Sprint D. The goal is not to claim proof of Reverse Universe Theory, but to show that the M1a bridge has moved from background-only compatibility into a perturbation-health and action-to-power testing pipeline.

The core frozen background parameters carried forward are:

z
t
	​

=0.35,width=0.03,dG=−0.159,
H
0
	​

=73.6,Ω
m
	​

=0.248,r
d
	​

=146.7Mpc.
2. Stage C Result: Frozen-Background Perturbation Survival

Stage C tested whether the frozen M1a background could survive growth, lensing consistency, and k-dependent perturbation health checks without retuning the background.

The leading Stage C corridor was:

μ
0
	​

=0.15,Σ
0
	​

=0.10,k
c
	​

=0.30h/Mpc,n=4.0.

The primary growth result was weak but stable: M1a was slightly BIC-favored over the matched LCDM comparison, but the difference was not strong enough to claim decisive evidence. The stronger Stage C result was robustness: leave-one-out and subset diagnostics did not favor LCDM, and the k-dependent perturbation scan found a large healthy region with no hard failures across the tested parameter combinations.

Conservative Stage C interpretation:
The frozen M1a bridge survives first-contact perturbation pressure. It is not proven, but it is not immediately ruled out by the tested growth, lensing, or perturbation-health diagnostics.

3. Sprint D Result: First Action-to-Power Bridge

Sprint D asked whether the Stage C corridor could be connected to an internal response structure rather than remaining a purely phenomenological healthy region.

The resulting pipeline was:

D
RG
	​

→M
AB
−1
	​

→μ(k,z),Σ(k,z)→P(k,z).

Sprint D1/D1b introduced a regularized radiation–gravity diagnostic response. Sprint D2/D2b then replaced the direct response with an inverse field-response matrix. The strongest result came from D2b, where explicit nonzero phase–bridge mixing remained healthy and reproduced the Stage C corridor.

The selected D2b nonzero-mixing model used:

m
ϕ
2
	​

=2.0,m
χ
2
	​

=2.0,λ
mix
	​

=0.05.

It produced small mean deviations:

⟨∣Δμ∣⟩≈0.00143,
⟨∣ΔΣ∣⟩≈0.00095,

with no determinant instability.

Sprint D3/D3b then propagated the D2b response into a CAMB-lite matter-power bridge. This is not full CAMB or MGCAMB. It is a controlled diagnostic using the frozen background, D2b-derived μ(k,z), and a linear growth equation.

The early-normalized D3b result found:

max∣ΔP/P∣
full
	​

≈0.00960,
max∣ΔP/P∣
k=0.2−0.3
	​

≈0.00693.

This indicates a sub-1% late-time matter-power signature near:

k∼0.2–0.3h/Mpc.
4. Conservative Interpretation

Stage C shows that the frozen M1a bridge survives first-pass perturbation checks. Sprint D provides a first mechanism-linked scaffold showing how the Stage C corridor may arise from a regularized radiation–gravity response, a stable inverse matrix response with nonzero phase–bridge mixing, and a controlled CAMB-lite matter-power signal.

This does not prove RUT/M1a. It does not replace covariance-aware datasets, full likelihood analysis, or a full Boltzmann-code implementation. The correct claim is narrower:

RUT/M1a now has a preliminary action-to-power bridge that connects a healthy perturbation corridor to a stable nonzero-mixing response and a small, testable P(k,z)-level signature.

5. Next Falsification Step

The next technical step is to map the D2b response into an MGCAMB/EFTCAMB-style μ(k,a), Σ(k,a) parameterization or compare the D3b CAMB-lite ratio against compressed DESI/Euclid-like constraints.

A clean failure at this stage would require revising or rejecting the current corridor. A clean survival would move RUT/M1a closer to a serious modified-gravity candidate model.
