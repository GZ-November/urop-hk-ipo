# Security and data policy

This public repository contains code and research artifacts derived from public HKEX disclosures: cohort workbooks, CSV panels, extraction evidence, codebooks and reports. It is not a code-only repository.

Credentials, private research material, raw PDF/full-text caches, workbook backups, isolated collection workspaces and model run logs should remain local. `.gitignore` is a convenience, not an access-control or secret-detection mechanism; already tracked files remain tracked until explicitly removed from the index.

Schema, evidence and SHA-256 state gates verify extraction structure and the exact reviewed payload before writeback. They do not prove that an extracted economic interpretation is correct. Independent source review remains necessary.

Report a vulnerability through GitHub's private vulnerability reporting feature if it is available, or privately contact the repository maintainer through an established channel. Do not put secrets, private data or exploitable payloads in a public issue. Public issues can describe non-sensitive bugs.
