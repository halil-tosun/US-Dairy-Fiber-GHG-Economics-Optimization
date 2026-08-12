"""
run_all.py -- Runs the full analytical pipeline (scripts 01-07) in order.

Usage:
    cd code
    python run_all.py
"""
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS = [
    "01_ingredient_library.py",
    "02_diet_optimization.py",
    "03_external_validation.py",
    "04_sensitivity_analysis.py",
    "05_alfalfa_constraint.py",
    "06_ingredient_library_robustness.py",
    "07_make_figures.py",
]

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    t0 = time.time()
    for i, script in enumerate(SCRIPTS, start=1):
        print(f"\n{'=' * 70}\n[{i}/{len(SCRIPTS)}] Running {script}\n{'=' * 70}")
        result = subprocess.run([sys.executable, str(HERE / script)], cwd=HERE)
        if result.returncode != 0:
            print(f"\nFAILED at {script} (exit code {result.returncode}). Stopping.")
            sys.exit(result.returncode)
    print(f"\n{'=' * 70}\nAll {len(SCRIPTS)} scripts completed successfully in {time.time() - t0:.1f}s\n{'=' * 70}")
    print("\nOutputs written to:")
    print("  output/   Table1-Table6 (.csv)")
    print("  figures/  Figure1_frontier.png, Figure2_composition.png (300 DPI)")
    print("  data/processed/  frontier_5ingredient.json, frontier_7ingredient.json")
