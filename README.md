# Download and restore the benchmark data

Download this repository as a ZIP and extract it, or download all `benchmark_data.zip.part*` files together with `download_manifest.json` and `restore_data.py` into one directory. Run:

```bash
python restore_data.py
```

The script uses only the Python standard library. It verifies all chunk checksums, reassembles the archive, verifies the complete archive, and extracts `benchmark_data/`. Then follow the data-loading and verification instructions below from that directory. The chunks are each below 8 MB for compatibility with the anonymous mirror. All chunks are required. No author paths, logs, or credentials are included inside the archive; binary archives are served unchanged by the mirror.

---

# Cancer-gene benchmark data

Data-only repository prepared for anonymous peer review. This package contains the processed MCF7, AML, K562 and Pan-cancer benchmarks, their PPI graphs, and the available Pan-cancer functional-hypergraph inputs. `dataset_summary.csv` reports statistics computed from the exported files.

## Contents and array conventions

- `datasets/{MCF7,AML,K562}/benchmark.npz`: lossless NumPy exports of all tensor fields in the benchmark PyG files, plus gene symbols and explicit labels. `x` contains the omics features; `edge_index` is the original 2-by-E zero-based PPI edge array. `edge_attr` is retained as supplied. `y` is the original two-column label encoding; `labels` uses 1=positive, 0=negative, -1=unlabeled. `pos` preserves node positions. The original train, validation, test and unlabeled masks are preserved.
- For the three cell-specific benchmarks, the ten train/validation partitions share a fixed test set. These are not ten independent test folds.
- `datasets/Pan-cancer/benchmark.npz`: portable omics, PPI edges, labels and gene symbols. The original feature CSV, gene list, PPI text and positive/negative lists are also retained. PPI edge orientation and multiplicity are preserved; undirected counts in the summary count unique unordered pairs.
- `datasets/Pan-cancer/foundation_features_pca64.npy`: the model's stored input with 48 omics dimensions, 64 GenePT dimensions and 64 Geneformer dimensions, in that order. The supplied PCA metadata is retained; no PCA is refitted for this release.
- `datasets/Pan-cancer/splits/biological_validation`: the existing 5-seed by 5-fold splits. `splits/feature_matched` contains the five outer folds and inner validation indices used for feature-matched comparisons. All indices refer to rows of the gene list, not positions within the labeled subset.
- `hypergraph/Pan-cancer`: original C2/C5 sparse gene-by-set incidence matrices and corresponding column names. Rows follow `datasets/Pan-cancer/geneList.txt`. These matrices precede cancer-set filtering and training-label-dependent hyperedge selection.
- `scripts/build_pan_hypergraph.py`: constructs the filtered and weighted Pan-cancer incidence matrix for a supplied training split. It records its random seed and isolation-repair convention.

## Load data

Requires Python, NumPy and SciPy. No PyTorch installation is required to read the portable exports.

```python
import numpy as np
data = np.load('datasets/MCF7/benchmark.npz', allow_pickle=False)
x, edge_index, labels = data['x'], data['edge_index'], data['labels']
train_mask = data['train_mask'][:, 0]
```

```bash
python scripts/build_pan_hypergraph.py --split datasets/Pan-cancer/splits/biological_validation/seed0_fold0.npz --output rebuilt_hypergraph --seed 42
python scripts/verify_release.py
```

## Hypergraph reproducibility and current completeness

The original Pan-cancer procedure removes C2 sets containing the underscore-delimited tokens CANCER, TUMOR or NEOPLASM, and C5 sets beginning with HP that contain those tokens. It retains sets with at least three positive genes from the training partition and assigns each retained set the fraction of member genes that are training positives. Validation/test labels must not be used in this step.

The original training code gives isolated nodes a tiny incidence (0.0001) in a randomly selected retained hyperedge. Its choices depend on the Python RNG state at the point of construction. The standalone script uses an explicit local RNG seed, so its repair choices are reproducible but are not claimed to be bitwise identical to every historical training run. The unpatched incidence matrix and weights are also saved.

**Pending:** the original MCF7, AML and K562 functional-hypergraph inputs have not yet been located. The Pan-cancer matrices have 13,627 rows and must not be reused directly for the 16,165-node cell benchmarks. No replacement or newly inferred cell hypergraphs are represented as historical experiment inputs. The exact MSigDB release is not recorded in the available matrix metadata.

## Sources and third-party terms

MCF7, AML and K562 are processed benchmarks based on [CGMega](https://github.com/NBStarry/CGMega). The original project's GPL-3.0 license is retained under `third_party/`; this notice does not grant additional rights to upstream datasets. Pan-cancer follows the EMOGI benchmark (Schulte-Sasse et al., *Integration of multiomics data with graph convolutional networks to identify new cancer genes and their associated molecular mechanisms*, 2021). PPI data originate from ConsensusPathDB (Kamburov et al., 2011).

The C2/C5 matrices are processed MSigDB gene-set data. MSigDB contents are copyright Broad Institute, Massachusetts Institute of Technology, and Regents of the University of California. See the [MSigDB license terms](https://www.gsea-msigdb.org/gsea/msigdb_license_terms.jsp). These terms include additional conditions for certain KEGG, BioCarta and legacy STKE sets. KEGG-derived sets retain copyright Kanehisa Laboratories; BioCarta-derived sets retain copyright BioCarta. Applicable source terms and attribution requirements continue to apply; the package is not placed under a blanket new data license. The local matrices' precise MSigDB version remains unverified.

Public upstream-source citations are retained for scientific attribution. Author-specific local paths, repository history, credentials and experiment logs are excluded. This repository contains processed gene-level benchmarks, not patient-level clinical records.
