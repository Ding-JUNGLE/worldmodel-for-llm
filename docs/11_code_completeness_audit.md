# Code Completeness Audit (GitHub Package)

Branch: `repro-tutorial-memory-guide-20260617`  
Date: 2026-06-17  
Repository: `/mnt/data1/dgw/github_upload/worldmodel-for-llm`

## Diagnosis

`PASS_CODE_REPRO_READY`

Static review of the checked files shows runnable implementations for all required scripts on this branch without visible TODO placeholders or missing-local-path references.

## 1) `scripts/external_memory/*.py` status

| Script | Classification |
| --- | --- |
| `scripts/external_memory/extract_keyframes.py` | runnable implementation |
| `scripts/external_memory/build_memory_bank.py` | runnable implementation |
| `scripts/external_memory/build_landmark_memory.py` | runnable implementation |
| `scripts/external_memory/retrieve_memory.py` | runnable implementation |
| `scripts/external_memory/rerank_candidates.py` | runnable implementation |
| `scripts/external_memory/evaluate_contact_sheet.py` | runnable implementation |
| `scripts/external_memory/effectiveness_utils.py` | wrapper only |
| `scripts/external_memory/memory_utils.py` | wrapper only |

- No `template only` status found.
- No hard `missing dependency` import failures found from local path inventory.

## 2) `scripts/run/*.sh` status

| Script | Clear CLI usage section | TODO/FIXME placeholders |
| --- | --- | --- |
| `scripts/run/run_gta_smoke_template.sh` | yes | none |
| `scripts/run/run_templerun_smoke_template.sh` | yes | none |
| `scripts/run/run_gta_landmark_memory_v1_template.sh` | yes | none |
| `scripts/run/run_gta_roadsign_memory_v3_template.sh` | yes | none |
| `scripts/run/reproduce_gta_roadsign_memory.sh` | yes | none |

## 3) Docs path check

- `docs/04_run_memory_experiments.md` points to:
  - `scripts/run/run_gta_smoke_template.sh`
  - `scripts/run/run_gta_landmark_memory_v1_template.sh`
  - `scripts/run/reproduce_gta_roadsign_memory.sh`

  All three exist in repo.

- `docs/05_memory_module_where_we_changed.md` script map points to:
  - `scripts/external_memory/extract_keyframes.py`
  - `scripts/external_memory/build_memory_bank.py`
  - `scripts/external_memory/build_landmark_memory.py`
  - `scripts/external_memory/retrieve_memory.py`
  - `scripts/external_memory/rerank_candidates.py`
  - `scripts/external_memory/evaluate_contact_sheet.py`
  - `scripts/external_memory/effectiveness_utils.py`
  - `scripts/run/run_gta_smoke_template.sh`
  - `scripts/run/run_templerun_smoke_template.sh`
  - `scripts/run/run_gta_landmark_memory_v1_template.sh`
  - `scripts/run/run_gta_roadsign_memory_v3_template.sh`
  - `scripts/run/reproduce_gta_roadsign_memory.sh`

  All listed paths exist in repo.

## 4) Missing / partial items

Code is not partial for the audited scope. No teammate-blocking missing scripts were found.

## Current teammate interpretation

The repository now includes a main reproduction entrypoint:

```text
scripts/run/reproduce_gta_roadsign_memory.sh
```

The repo should still be treated as an external memory overlay, not a full Matrix-Game-2 mirror.

A teammate must install Matrix-Game-2 and checkpoints separately.
