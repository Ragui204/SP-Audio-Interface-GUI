# AudioLink Test Suite

This `tests/` directory contains all evaluation resources for verifying functionality, performance, and integration of the **AudioLink** system. It includes structured test plans, performance benchmarks, and log data collected during development.

## Contents

- `test_plans.md`  
  Detailed testing procedures for core modules including:
  - MIDI input
  - CAN bus integration
  - Guitar and piano audio effects
  - Latency measurement
  - System boot and UI response

- `performance_metrics.csv`  
  Quantitative data gathered during hardware/software tests, such as:
  - Latency (ms) across different input types
  - CPU usage on Raspberry Pi
  - Teensy DSP load
  - Audio throughput consistency

- `test_logs/`  
  Time-stamped logs from actual test runs, including:
  - Console output
  - Observed issues or anomalies
  - Notes on debugging steps taken

## Purpose

This testing archive supports:
- Regression testing as the system scales
- Verification of patent-relevant performance claims
- Future refinement of modules

> ⚠Some tests require specific hardware to be connected (e.g., Teensy 4.1, guitar input, MIDI keyboard).

---

### Status

| Area                   | Status       |
|------------------------|--------------|
| Audio Latency Tests    | Completed |
| CAN Bus Messaging      | Verified  |
| Reverb/Delay Accuracy  | Verified  |
| GUI Navigation Tests   | In Progress |

---

All team members contributed to tests based on their module responsibilities. These files are living documents and subject to updates as more results are collected.
