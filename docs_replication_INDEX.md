# Replication Index — STRICT v2.1

DOI (Zenodo snapshot): https://doi.org/10.5281/zenodo.18854340  
Git tag: strict-v2-2026-03-01.1  

## What to read first
1) Replication packet: Replication_Packet_v1_RUT_Strict_Test_v2.pdf  
2) Must-match checklist: STRICTv2_MustMatch_Checklist_1page.pdf  
3) Falsifiers: RUT_Falsifiers.pdf  

## What to download / where the data is
- Preferred: download the STRICT v2.1 release asset zip (contains strict_test_v1/)
- In the zip, key files:
  - strict_test_v1/frozen_params.json
  - strict_test_v1/results_datasetB/*.json
  - strict_test_v1/results_datasetC/*.json
  - strict_test_v1/results_joint/*.json
  - strict_test_v1/datasetB_CC_data.dat
  - strict_test_v1/datasetB_BAO_sdss4_aniso.csv
  - strict_test_v1/datasetB_RSD_sdss4_fs8.csv
  - strict_test_v1/datasetC_lensing_h0licow5.csv

## Decision rule
Primary metric: BIC.  
Convention: ΔBIC = BIC_LCDM − BIC_RUT (positive favors RUT).  
Stop rule: if you cannot reproduce the must-match table within tolerance, treat replication as failed until discrepancy is explained.
