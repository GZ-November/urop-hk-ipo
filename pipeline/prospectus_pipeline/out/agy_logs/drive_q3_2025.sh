#!/bin/bash
# 2025Q3 抽取战役驱动 v2：4 路并行 agy + 逐组 validate
cd "/Users/georgezhu/Desktop/UROP HK IPO/pipeline" || exit 1
export PIPELINE_CONFIG="$PWD/prospectus_pipeline/datasets/HKIPO_2025-07-01_2025-09-30_HKIPO-MB/cohort.yaml"
AGY="/Users/georgezhu/.local/bin/agy"
LOGS="$PWD/prospectus_pipeline/out/agy_logs"
PKTS="$PWD/prospectus_pipeline/datasets/HKIPO_2025-07-01_2025-09-30_HKIPO-MB/out/prompts"
CODES=(1828.HK 2259.HK 2525.HK 2543.HK 2580.HK 2583.HK 2590.HK 2591.HK 2592.HK 2595.HK 2597.HK 2627.HK 2631.HK 2648.HK 2651.HK 2656.HK 2889.HK 3858.HK 6090.HK 6613.HK 6960.HK 9887.HK 9973.HK)
echo "CODES (${#CODES[@]}): ${CODES[*]}"

for ((start = 0; start < ${#CODES[@]}; start += 4)); do
  batch=("${CODES[@]:start:4}")
  echo "=== BATCH start=$start: ${batch[*]} $(date +%H:%M:%S) ==="
  pids=()
  for code in "${batch[@]}"; do
    digits="${code%%.*}"
    P="$PKTS/HKIPO-MB${digits}.extract.prompt.md"
    if [[ ! -f "$P" ]]; then
      echo "SKIP $code: prompt 缺失 $P"
      continue
    fi
    "$AGY" -p "$(cat "$P")" --dangerously-skip-permissions --print-timeout 25m \
      > "$LOGS/${digits}.log" 2>&1 &
    pids+=($!)
  done
  for pid in "${pids[@]}"; do wait "$pid"; done
  for code in "${batch[@]}"; do
    digits="${code%%.*}"
    echo "--- validate $code $(date +%H:%M:%S) ---" >> "$LOGS/${digits}.log"
    python3 run.py validate --only "$code" >> "$LOGS/${digits}.log" 2>&1
  done
done
echo "ALL 23 EXTRACTION RUNS COMPLETE $(date +%H:%M:%S)"
