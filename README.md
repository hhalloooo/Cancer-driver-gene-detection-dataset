# Cancer driver gene detection datasets

Processed MCF7, AML, K562 and Pan-cancer datasets, including gene features, labels, PPI networks and shared C2/C5 functional-hypergraph data.

## Download

Download all six `benchmark_data.zip.part001`–`benchmark_data.zip.part006` files and `restore_data.py` into the same folder, then run:

```bash
python restore_data.py
```

The six files are consecutive parts of one ZIP archive, not six separate datasets. The script joins and extracts them without a checksum manifest. The archive contains data only; the restoration script is outside it.

## Folders

```text
benchmark_data/
├── datasets/
│   ├── MCF7/
│   ├── AML/
│   ├── K562/
│   └── Pan-cancer/
└── hypergraph/
    └── shared/
```

Each dataset includes its PPI network in `benchmark.npz` (`edge_index`). Pan-cancer additionally includes the original feature and PPI text files and the stored GenePT/Geneformer features.

All datasets use the shared functional-hypergraph resource in `hypergraph/shared/`: C2/C5 incidence matrices and gene-set names. The supplied matrices contain 13,627 gene rows, identified by `gene_order.csv`; align by gene identifiers before use with a dataset's node order.

## Sources

The cell-specific benchmarks follow [CGMega](https://github.com/NBStarry/CGMega); Pan-cancer follows EMOGI (Schulte-Sasse et al., 2021). PPI data originate from ConsensusPathDB. CGMega's license is retained in `CGMega-LICENSE.txt`.

C2/C5 data originate from MSigDB, copyright Broad Institute, Massachusetts Institute of Technology and Regents of the University of California. The [MSigDB terms](https://www.gsea-msigdb.org/gsea/msigdb_license_terms.jsp), including additional terms for KEGG (Kanehisa Laboratories), BioCarta and legacy STKE gene sets, continue to apply.
