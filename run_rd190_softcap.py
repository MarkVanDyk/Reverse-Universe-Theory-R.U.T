import os, glob, zipfile, shutil, json, time
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

# ============================================================
# run_rd190_softcap.py
# SELF-CONTAINED EXPANDED JOINT(B+C) REFIT WITH rd CAP = 190
# SOFT rd PENALTY VERSION
# ============================================================

RD_CAP = 190.0
RD_SOFT_PENALTY = 1.0e4
USE_SOFT_RD_CAP = True

# ------------------------------------------------------------
# 1) Recover ROOT and extract strict zip if needed
# ------------------------------------------------------------
hits = glob.glob("./**/frozen_params.json", recursive=True)

if not hits:
    zip_candidates = glob.glob("./**/*.zip", recursive=True)
    strict_zips = [z for z in zip_candidates if "strict" in os.path.basename(z).lower()]
    print("strict zip candidates:", strict_zips)

    if not strict_zips:
        raise FileNotFoundError("No strict zip found. Place strict_test_v1.zip or equivalent in the working directory.")

    zip_path = strict_zips[0]
    print("Using zip:", zip_path)

    shutil.rmtree("./RUT_REPO", ignore_errors=True)
    os.makedirs("./RUT_REPO", exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall("./RUT_REPO")

    hits = glob.glob("./RUT_REPO/**/frozen_params.json", recursive=True)

if not hits:
    raise FileNotFoundError("Could not find frozen_params.json after extraction.")

ROOT = os.path.dirname(hits[0])
print("ROOT =", ROOT)

# ------------------------------------------------------------
# 2) Load omega + datasets
# ------------------------------------------------------------
with open(f"{ROOT}/frozen_params.json", "r") as f:
    frozen = json.load(f)

OMEGA_REF = float(frozen["omega_frozen"])
print("Using omega_frozen =", OMEGA_REF)

cc = np.loadtxt(f"{ROOT}/datasetB_CC_data.dat", delimiter=",", comments="#", usecols=(0, 1, 2))
zCC, HCC, sHCC = cc[:, 0], cc[:, 1], cc[:, 2]

bao = pd.read_csv(f"{ROOT}/datasetB_BAO_sdss4_aniso.csv")
zBAO = bao["z_eff"].to_numpy(float)
DMo = bao["DM_over_rd"].to_numpy(float)
sDM = bao["sDM"].to_numpy(float)
DHo = bao["DH_over_rd"].to_numpy(float)
sDH = bao["sDH"].to_numpy(float)

rsd = pd.read_csv(f"{ROOT}/datasetB_RSD_sdss4_fs8.csv")
zRSD = rsd["z_eff"].to_numpy(float)
fs8o = rsd["fs8"].to_numpy(float)
sfs8 = rsd["sfs8"].to_numpy(float)

lens = pd.read_csv(f"{ROOT}/datasetC_lensing_h0licow5.csv")
zL = lens["z_l"].to_numpy(float)
zS = lens["z_s"].to_numpy(float)
Ddt_obs = lens["Ddt_Mpc_mu"].to_numpy(float)
sDdt = lens["Ddt_Mpc_sig"].to_numpy(float)

Nobs = len(zCC) + 2 * len(zBAO) + len(zRSD) + len(zL)
print("Nobs_total =", Nobs)

# ------------------------------------------------------------
# 3) Load baseline JOINT(B+C) result
# ------------------------------------------------------------
joint_json = f"{ROOT}/results_joint/results_JOINT_BplusC_omegaLocked.json"
if not os.path.exists(joint_json):
    raise FileNotFoundError(f"Missing baseline joint result JSON: {joint_json}")

with open(joint_json, "r") as f:
    joint = json.load(f)

pR = np.array(joint["rut"]["values"], dtype=float)
bicL = float(joint["lcdm"]["BIC"])
bicR = float(joint["rut"]["BIC"])

print("\nRecovered baseline pR =", pR.tolist())
print("Baseline bicL =", bicL, "bicR =", bicR)

# ------------------------------------------------------------
# 4) Load prior expanded result if available
# ------------------------------------------------------------
prior_candidates = [
    f"{ROOT}/results_joint/results_JOINT_BplusC_expanded_rd190_softcap.json",
    f"{ROOT}/results_joint/results_JOINT_BplusC_expanded_rd180.json",
    f"{ROOT}/results_joint/results_JOINT_BplusC_expanded_rd176.json",
]

prior_best_p = None
prior_best_bic = None
prior_source = None

for cand in prior_candidates:
    if os.path.exists(cand):
        with open(cand, "r") as f:
            prev = json.load(f)
        prior_best_p = np.array(prev["best_expanded_fit"]["values"], dtype=float)
        prior_best_bic = float(prev["best_expanded_fit"]["BIC"])
        prior_source = cand
        break

if prior_best_p is not None:
    print("\nLoaded prior expanded best_p from", prior_source)
    print("prior_best_p =", prior_best_p.tolist())
    print("prior_best_BIC =", prior_best_bic)
else:
    prior_best_p = np.array([
        88.0, 0.28, 179.0, 0.47, pR[4], 0.14, 0.09,
        OMEGA_REF - 0.05, OMEGA_REF - 0.02, -0.01
    ], dtype=float)
    print("\nNo prior expanded JSON found. Using fallback prior seed.")

# ------------------------------------------------------------
# 5) Helpers
# ------------------------------------------------------------
c_km_s = 299792.458

def phi_frozen_of_a(a):
    return -OMEGA_REF * np.log(a)

z_all_probe = np.unique(np.concatenate([zCC, zBAO, zRSD, zS]))
a_all_probe = 1.0 / (1.0 + z_all_probe)
phi_frozen_probe = phi_frozen_of_a(a_all_probe)

def E(z, Om):
    return np.sqrt(Om * (1.0 + z) ** 3 + (1.0 - Om))

def H_lcdm(z, H0, Om):
    return H0 * E(z, Om)

def Dc(z, H0, Om, n=3000):
    zz = np.linspace(0.0, z, n)
    return (c_km_s / H0) * np.trapezoid(1.0 / E(zz, Om), zz)

def Ddt_lcdm(zl, zs, H0, Om):
    Dc_l = Dc(zl, H0, Om)
    Dc_s = Dc(zs, H0, Om)
    Dl = Dc_l / (1.0 + zl)
    Ds = Dc_s / (1.0 + zs)
    Dls = (Dc_s - Dc_l) / (1.0 + zs)
    if np.any(np.asarray(Dls) <= 0):
        return np.nan
    return (1.0 + zl) * Dl * Ds / Dls

def E2_bg(a, Om):
    return Om * a ** (-3) + (1.0 - Om)

def dlnH_dN_bg(a, Om):
    e2 = E2_bg(a, Om)
    de2_dN = -3.0 * Om * a ** (-3)
    return 0.5 * de2_dN / np.maximum(e2, 1e-14)

def solve_omega_phase_background(a_min, a_max, Om, mu, omega0, omega_init, omegaN_init, n_grid=800):
    N_min = np.log(a_min)
    N_max = np.log(a_max)

    def rhs(N, y):
        omega, omegaN = y
        a = np.exp(N)
        e2 = E2_bg(a, Om)
        dlnH = dlnH_dN_bg(a, Om)
        domega_dN = omegaN
        domegaN_dN = -(3.0 + dlnH) * omegaN - (mu ** 2) * (omega - omega0) / np.maximum(e2, 1e-14)
        return [domega_dN, domegaN_dN]

    sol = solve_ivp(
        rhs,
        (N_min, N_max),
        [omega_init, omegaN_init],
        dense_output=True,
        rtol=1e-7,
        atol=1e-9,
        max_step=0.05,
    )

    if not sol.success:
        raise RuntimeError(sol.message)

    N_grid = np.linspace(N_min, N_max, n_grid)
    Y = sol.sol(N_grid)
    omega_grid = Y[0]
    omegaN_grid = Y[1]
    a_grid = np.exp(N_grid)

    phi_grid = np.zeros_like(N_grid)
    for i in range(len(N_grid) - 2, -1, -1):
        dN = N_grid[i + 1] - N_grid[i]
        phi_grid[i] = phi_grid[i + 1] + 0.5 * (omega_grid[i] + omega_grid[i + 1]) * dN

    return {
        "a_grid": a_grid,
        "omega_grid": omega_grid,
        "omegaN_grid": omegaN_grid,
        "phi_grid": phi_grid,
    }

def rut_factor_dynamic(z, dyn):
    z = np.asarray(z, dtype=float)
    a = 1.0 / (1.0 + z)
    phi = np.interp(a, dyn["a_grid"], dyn["phi_grid"])
    return np.cos(phi), np.sin(phi)

# ------------------------------------------------------------
# 6) Objective
# ------------------------------------------------------------
def chi2_joint_rut_full_dynamic_bS_expanded_rd190(p):
    H0, Om, rd, s80, bC, bS, mu, omega0, omega_init, omegaN_init = p

    if not (40 < H0 < 95): return 1e99
    if not (0.05 < Om < 0.6): return 1e99
    if not (120 < rd < 260): return 1e99
    if not (0.4 < s80 < 1.4): return 1e99
    if not (pR[4] - 0.06 < bC < pR[4] + 0.06): return 1e99
    if not (-0.20 < bS < 0.20): return 1e99
    if not (1e-4 < mu < 0.1): return 1e99
    if not (OMEGA_REF - 2.0 < omega0 < OMEGA_REF + 2.0): return 1e99
    if not (omega0 - 0.5 < omega_init < omega0 + 0.5): return 1e99
    if not (-0.2 < omegaN_init < 0.2): return 1e99

    try:
        dyn = solve_omega_phase_background(1e-3, 1.0, Om, mu, omega0, omega_init, omegaN_init)
    except Exception:
        return 1e99

    if not np.all(np.isfinite(dyn["omega_grid"])) or not np.all(np.isfinite(dyn["phi_grid"])):
        return 1e99
    if float(np.min(dyn["omega_grid"])) < OMEGA_REF - 4.0 or float(np.max(dyn["omega_grid"])) > OMEGA_REF + 4.0:
        return 1e99
    if np.max(np.abs(dyn["omegaN_grid"])) > 1.0:
        return 1e99

    Cc, Sc = rut_factor_dynamic(zCC, dyn)
    fCC = 1.0 + bC * Cc + bS * Sc
    rCC = (HCC - H_lcdm(zCC, H0, Om) * fCC) / sHCC
    chi2 = np.sum(rCC * rCC)

    Cb, Sb = rut_factor_dynamic(zBAO, dyn)
    fBAO = 1.0 + bC * Cb + bS * Sb
    DcBAO = np.array([Dc(z, H0, Om) for z in zBAO], dtype=float)
    DM = (1.0 + zBAO) * DcBAO * fBAO
    DH = (c_km_s / H_lcdm(zBAO, H0, Om)) * fBAO
    rDM = (DM / rd - DMo) / sDM
    rDH = (DH / rd - DHo) / sDH
    chi2 += np.sum(rDM * rDM) + np.sum(rDH * rDH)

    Cr, Sr = rut_factor_dynamic(zRSD, dyn)
    fRSD = 1.0 + bC * Cr + bS * Sr
    rfs = (fs8o - s80 * fRSD) / sfs8
    chi2 += np.sum(rfs * rfs)

    Cl, Sl = rut_factor_dynamic(zS, dyn)
    fL = 1.0 + bC * Cl + bS * Sl
    Dpred = np.array([Ddt_lcdm(zL[i], zS[i], H0, Om) for i in range(len(zL))], dtype=float) * fL
    if not np.all(np.isfinite(Dpred)):
        return 1e99
    rD = (Ddt_obs - Dpred) / sDdt
    chi2 += np.sum(rD * rD)

    phi_dyn_probe = np.interp(a_all_probe, dyn["a_grid"], dyn["phi_grid"])
    dphi_probe = phi_dyn_probe - phi_frozen_probe
    rms_dphi = np.sqrt(np.mean(dphi_probe ** 2))

    chi2 += 0.5 * ((omega0 - OMEGA_REF) / 1.0) ** 2
    chi2 += 0.5 * ((omega_init - omega0) / 0.25) ** 2
    chi2 += 0.5 * (omegaN_init / 0.1) ** 2
    chi2 += 0.1 * rms_dphi ** 2
    chi2 += 0.5 * ((bC - pR[4]) / 0.02) ** 2
    chi2 += 0.05 * ((bS - pR[5]) / 0.10) ** 2

    if USE_SOFT_RD_CAP and rd > RD_CAP:
        chi2 += RD_SOFT_PENALTY * (rd - RD_CAP) ** 2

    return float(chi2) if np.isfinite(chi2) else 1e99

# ------------------------------------------------------------
# 7) Bounds + seeds
# ------------------------------------------------------------
bounds = [
    (40.0, 95.0), (0.05, 0.6), (120.0, RD_CAP + 10.0), (0.4, 1.4),
    (float(pR[4] - 0.06), float(pR[4] + 0.06)), (-0.12, 0.20),
    (1e-4, 0.1), (OMEGA_REF - 2.0, OMEGA_REF + 2.0),
    (OMEGA_REF - 2.0, OMEGA_REF + 2.0), (-0.2, 0.2),
]

def clip_to_bounds(x, bounds):
    y = np.array(x, dtype=float).copy()
    for i, (lo, hi) in enumerate(bounds):
        y[i] = min(max(y[i], lo + 1e-8), hi - 1e-8)
    return y

seed_list = [
    prior_best_p,
    np.array([prior_best_p[0], prior_best_p[1], 179.5, prior_best_p[3], prior_best_p[4], prior_best_p[5], prior_best_p[6], prior_best_p[7], prior_best_p[8], prior_best_p[9]], dtype=float),
    np.array([prior_best_p[0], prior_best_p[1], 181.0, prior_best_p[3], prior_best_p[4], 0.15, prior_best_p[6], prior_best_p[7], prior_best_p[8], prior_best_p[9]], dtype=float),
    np.array([prior_best_p[0], prior_best_p[1], 183.0, prior_best_p[3], prior_best_p[4], 0.16, 0.095, prior_best_p[7], prior_best_p[8], prior_best_p[9]], dtype=float),
    np.array([88.0, 0.28, 185.0, 0.47, prior_best_p[4], 0.16, 0.095, OMEGA_REF - 0.05, OMEGA_REF - 0.02, -0.01], dtype=float),
    np.array([87.5, 0.27, 188.0, 0.47, prior_best_p[4], 0.17, 0.098, OMEGA_REF - 0.08, OMEGA_REF - 0.03, -0.015], dtype=float),
]

# ------------------------------------------------------------
# 8) Stage 1
# ------------------------------------------------------------
results_stage1 = []
for i, seed in enumerate(seed_list, start=1):
    x0 = clip_to_bounds(seed, bounds)
    print(f"\n----- Stage 1 Seed {i} / {len(seed_list)} -----")
    print("x0 =", x0.tolist())

    t0 = time.time()
    res = minimize(
        chi2_joint_rut_full_dynamic_bS_expanded_rd190,
        x0,
        method="L-BFGS-B",
        bounds=bounds,
        options={"maxiter": 700, "ftol": 1e-11},
    )
    dt = time.time() - t0

    chi2_val = float(res.fun)
    bic_val = chi2_val + 10.0 * np.log(Nobs)
    row = {
        "stage": "stage1",
        "seed_index": i,
        "success": bool(res.success),
        "message": str(res.message),
        "nfev": int(getattr(res, "nfev", -1)),
        "nit": int(getattr(res, "nit", -1)),
        "time_sec": float(dt),
        "chi2": chi2_val,
        "BIC": float(bic_val),
        "values": [float(v) for v in res.x],
    }
    results_stage1.append(row)
    print("success =", row["success"])
    print("message =", row["message"])
    print("chi2    =", row["chi2"])
    print("BIC     =", row["BIC"])
    print("values  =", row["values"])

valid1 = [r for r in results_stage1 if np.isfinite(r["chi2"]) and r["chi2"] < 1e98]
if not valid1:
    raise RuntimeError("No valid expanded fit was found in stage 1.")

best1 = sorted(valid1, key=lambda r: r["BIC"])[0]
best1_p = np.array(best1["values"], dtype=float)
best1_bic = float(best1["BIC"])

print("\n================ STAGE 1 BEST (rd cap 190, soft cap) ================")
print("best1_BIC =", best1_bic)
print("best1_p   =", best1_p.tolist())
print("ΔBIC vs baseline RUT =", best1_bic - bicR)
print("ΔBIC vs baseline LCDM =", best1_bic - bicL)

# ------------------------------------------------------------
# 9) 1D rd probe
# ------------------------------------------------------------
H0_ref, Om_ref, rd_ref, s80_ref, bC_ref_fit, bS_ref_fit, mu_ref, omega0_ref, omega_init_ref, omegaN_init_ref = best1_p
rd_probe_lo = max(170.0, rd_ref - 4.0)
rd_probe_hi = min(RD_CAP + 2.0, rd_ref + 4.0)
rd_probe = np.linspace(rd_probe_lo, rd_probe_hi, 65)

probe_rows = []
print("\n================ 1D rd PROBE AROUND STAGE 1 BEST ================")
for rd_test in rd_probe:
    p_test = np.array([H0_ref, Om_ref, rd_test, s80_ref, bC_ref_fit, bS_ref_fit, mu_ref, omega0_ref, omega_init_ref, omegaN_init_ref], dtype=float)
    chi2_test = chi2_joint_rut_full_dynamic_bS_expanded_rd190(p_test)
    bic_test = chi2_test + 10.0 * np.log(Nobs)
    delta_bic = bic_test - best1_bic
    row = {
        "rd": float(rd_test),
        "chi2": float(chi2_test),
        "BIC": float(bic_test),
        "delta_bic_from_stage1_best": float(delta_bic),
    }
    probe_rows.append(row)
    print(f"rd={rd_test:.6f}   chi2={chi2_test:.6f}   BIC={bic_test:.6f}   ΔBIC={delta_bic:.6f}")

best_probe = sorted(probe_rows, key=lambda r: r["BIC"])[0]
best_probe_rd = float(best_probe["rd"])
print("\nBest 1D rd probe point =", best_probe)

# ------------------------------------------------------------
# 10) Stage 2 polish
# ------------------------------------------------------------
polish_seed = best1_p.copy()
polish_seed[2] = best_probe_rd
polish_seed = clip_to_bounds(polish_seed, bounds)

print("\n================ STAGE 2 POLISH SEED ================")
print("polish_seed =", polish_seed.tolist())

t0 = time.time()
res2 = minimize(
    chi2_joint_rut_full_dynamic_bS_expanded_rd190,
    polish_seed,
    method="L-BFGS-B",
    bounds=bounds,
    options={"maxiter": 900, "ftol": 1e-12},
)
dt2 = time.time() - t0

chi2_2 = float(res2.fun)
bic_2 = chi2_2 + 10.0 * np.log(Nobs)
stage2 = {
    "stage": "stage2_polish",
    "seed_index": 1,
    "success": bool(res2.success),
    "message": str(res2.message),
    "nfev": int(getattr(res2, "nfev", -1)),
    "nit": int(getattr(res2, "nit", -1)),
    "time_sec": float(dt2),
    "chi2": chi2_2,
    "BIC": float(bic_2),
    "values": [float(v) for v in res2.x],
}
print("stage2 success =", stage2["success"])
print("stage2 message =", stage2["message"])
print("stage2 chi2    =", stage2["chi2"])
print("stage2 BIC     =", stage2["BIC"])
print("stage2 values  =", stage2["values"])

all_valid = valid1.copy()
if np.isfinite(stage2["chi2"]) and stage2["chi2"] < 1e98:
    all_valid.append(stage2)

best_final = sorted(all_valid, key=lambda r: r["BIC"])[0]
best_p = np.array(best_final["values"], dtype=float)
best_bic = float(best_final["BIC"])
best_chi2 = float(best_final["chi2"])

print("\n================ FINAL BEST EXPANDED FIT (rd cap 190, soft cap) ================")
print("winner_stage =", best_final["stage"])
print("best_chi2    =", best_chi2)
print("best_BIC     =", best_bic)
print("best_p       =", best_p.tolist())
print("ΔBIC vs prior expanded =", (best_bic - prior_best_bic) if prior_best_bic is not None else None)
print("ΔBIC vs baseline RUT =", best_bic - bicR)
print("ΔBIC vs baseline LCDM =", best_bic - bicL)

# ------------------------------------------------------------
# 11) Final local rd scan
# ------------------------------------------------------------
H0_ref, Om_ref, rd_ref, s80_ref, bC_ref_fit, bS_ref_fit, mu_ref, omega0_ref, omega_init_ref, omegaN_init_ref = best_p
rd_lo = max(170.0, rd_ref - 4.0)
rd_hi = min(RD_CAP + 2.0, rd_ref + 4.0)
rd_grid = np.linspace(rd_lo, rd_hi, 61)

scan_rows = []
print("\n================ FINAL LOCAL rd SCAN ================")
for rd_test in rd_grid:
    p_test = np.array([H0_ref, Om_ref, rd_test, s80_ref, bC_ref_fit, bS_ref_fit, mu_ref, omega0_ref, omega_init_ref, omegaN_init_ref], dtype=float)
    chi2_test = chi2_joint_rut_full_dynamic_bS_expanded_rd190(p_test)
    bic_test = chi2_test + 10.0 * np.log(Nobs)
    delta_bic = bic_test - best_bic
    row = {
        "rd": float(rd_test),
        "chi2": float(chi2_test),
        "BIC": float(bic_test),
        "delta_bic_from_best": float(delta_bic),
    }
    scan_rows.append(row)
    print(f"rd={rd_test:.6f}   chi2={chi2_test:.6f}   BIC={bic_test:.6f}   ΔBIC={delta_bic:.6f}")

best_scan = sorted(scan_rows, key=lambda r: r["BIC"])[:12]
print("\nTop final rd scan points:")
for row in best_scan:
    print(f"rd={row['rd']:.6f}   BIC={row['BIC']:.6f}   ΔBIC={row['delta_bic_from_best']:.6f}")

supported = [r for r in scan_rows if r["delta_bic_from_best"] <= 2.0]
if supported:
    rd_support_min = min(r["rd"] for r in supported)
    rd_support_max = max(r["rd"] for r in supported)
    print("\nΔBIC <= 2 support range:")
    print("rd_min =", rd_support_min)
    print("rd_max =", rd_support_max)
else:
    print("\nNo final scan points found within ΔBIC <= 2 of best.")

# ------------------------------------------------------------
# 12) Save output JSON
# ------------------------------------------------------------
os.makedirs(f"{ROOT}/results_joint", exist_ok=True)
out = {
    "root": ROOT,
    "omega_frozen": float(OMEGA_REF),
    "Nobs_total": int(Nobs),
    "baseline_joint_json": joint_json,
    "baseline_lcdm_BIC": bicL,
    "baseline_rut_BIC": bicR,
    "prior_expanded_json": prior_source,
    "prior_expanded_BIC": prior_best_bic,
    "expanded_fit_rd_cap": RD_CAP,
    "rd_soft_penalty": RD_SOFT_PENALTY if USE_SOFT_RD_CAP else None,
    "stage1_results": results_stage1,
    "stage2_polish_result": stage2,
    "best_expanded_fit": {
        "winner_stage": best_final["stage"],
        "chi2": best_chi2,
        "BIC": best_bic,
        "values": best_p.tolist(),
        "delta_BIC_vs_prior_expanded": (float(best_bic - prior_best_bic) if prior_best_bic is not None else None),
        "delta_BIC_vs_baseline_RUT": float(best_bic - bicR),
        "delta_BIC_vs_baseline_LCDM": float(best_bic - bicL),
    },
    "rd_probe_rows": probe_rows,
    "final_local_rd_scan": scan_rows,
    "best_final_rd_scan_points": best_scan,
    "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
}
out_path = f"{ROOT}/results_joint/results_JOINT_BplusC_expanded_rd190_softcap.json"
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)

print("\nSaved", out_path)
