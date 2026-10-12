"""Resolve evidence target paths without changing Main Board schema contracts."""
from __future__ import annotations

from copy import deepcopy

from boards import normalize_board


def target_paths(cfg, target):
    if target == "gem":
        if normalize_board(cfg.get("dataset", {}).get("board")) != "gem":
            raise ValueError("GEM extension target requires a GEM cohort config")
        output = cfg["paths"]["out"] / "gem"
        return cfg["_root"] / "schema/gem_fields.json", output, cfg["paths"].get("packets", cfg["_root"] / "data/packets")
    if target == "allot":
        return cfg["_root"] / "schema/allot_fields.json", cfg["paths"]["allot_out"], cfg["paths"].get("allot_packets", cfg["_root"] / "data/allot/packets")
    if target != "prospectus":
        raise ValueError(f"Unknown extraction target: {target}")
    schema = "gem_prospectus_fields.json" if normalize_board(cfg.get("dataset", {}).get("board")) == "gem" else "fields.json"
    return cfg["_root"] / "schema" / schema, cfg["paths"]["out"], cfg["paths"].get("packets", cfg["_root"] / "data/packets")


def target_config(cfg, target):
    if target != "gem":
        return cfg
    target_paths(cfg, target)  # verify board first
    result = deepcopy(cfg)
    result["sheet"] = "GEM_details"
    return result
