python
# ==============================================================================
# Evaluation Pipeline for Llama-3 Patwa Audit
# Reference Implementation for Appendix D
# ------------------------------------------------------------------------------
# This script processes human annotations, calculates dimension-level means,
# and computes 95% Bootstrapped Confidence Intervals.
# ==============================================================================
‌
import json
import numpy as np
import pandas as pd
from pathlib import Path
‌
def bootstrap_ci(values, n_boot=2000, alpha=0.05, seed=123):
"""
Calculates the mean and 95% confidence interval using bootstrapping.
This method is used to ensure statistical robustness across stochastic runs.
"""
rng = np.random.default_rng(seed)
values = np.asarray(values, dtype=float)
# Remove NaN values to avoid calculation errors
values = values[~np.isnan(values)]
‌
if len(values) == 0:
return np.nan, np.nan, np.nan
‌
# Generate bootstrap samples
boots = [np.mean(rng.choice(values, size=len(values), replace=True)) for _ in range(n_boot)]
boots = np.array(boots)
‌
# Return Mean, Lower Bound, and Upper Bound
return float(np.mean(values)), float(np.quantile(boots, alpha/2)), float(np.quantile(boots, 1 - alpha/2))
‌
def run_audit_evaluation():
"""
Main pipeline to aggregate scores across the 5 dimensions of the rubric.
"""
print("🚀 Starting Evaluation Pipeline...")
‌
try:
# Load the human annotations file
# In a real scenario, this file contains the scores (0-2) for each prompt/run.
ann = pd.read_csv("annotations.csv")
‌
# Define the 5 dimensions based on the scoring rubric (Appendix C)
score_cols = ["D1_grammar", "D2_fidelity", "D3_deficit", "D4_stereo", "D5_uncertainty"]
‌
if not all(col in ann.columns for col in score_cols):
print("❌ Error: The annotations.csv file must contain columns: D1_grammar, D2_fidelity, D3_deficit, D4_stereo, D5_uncertainty")
return
‌
# Calculate results for each dimension
results = []
for col in score_cols:
mean_val, lo, hi = bootstrap_ci(ann[col])
results.append({
"dimension": col,
"mean": mean_val,
"ci_lower": lo,
"ci_upper": hi
})
‌
# Create a summary DataFrame
df_res = pd.DataFrame(results)
‌
# Save the results to the 'out' directory
Path("out").mkdir(exist_ok=True)
df_res.to_csv("out/results_summary.csv", index=False)
‌
print("\n✅ Evaluation Complete!")
print("--- Summary Table ---")
print(df_res)
print("\nDetailed results saved to: out/results_summary.csv")
‌
except FileNotFoundError:
print("⚠️ Note: 'annotations.csv' not found. This script is a reference implementation.")
print("To run this, please upload your 'annotations.csv' to the root folder.")
‌
if __name__ == "__main__":
run_audit_evaluation()
