<!-- ## Week 2 – Region-based RM Score Analysis

### Work Done
- Implemented region-based RM score aggregation
- Parsed mixed score formats (numeric and fractional like 13/20).
- Integrated SQL aggregation with psycopg2 in Python.

### Problems Faced
- psycopg2 raised errors due to `%` symbols in SQL LIKE clauses.
- Queries returned empty result sets due to strict filters.
- Import and execution path issues in project structure.

### Solution
- Escaped `%` as `%%` for psycopg2 compatibility
- Verified data correctness using pgAdmin before Python execution.
- Reorganized files to ensure correct module imports.


### Design Decision
Scores stored as `"x/y"` are aggregated using the numerator (`x`) only.
Fractional normalization was intentionally avoided to prevent ambiguity
and simplify regional comparisons.

### Outcome
- Successfully computed average, best, and worst RM scores per region.
- Achieved a stable working query integrated with Python. -->


## Week 2 – Region-wise RM Score Aggregation (Python-based)

### Objective
Compute region-level RM performance metrics (average, best, worst score)
using Python-only processing, with SQL restricted to data retrieval.

---

### Work Done
- Retrieved RM score data using SQL joins across:
  - `transaction_info`
  - `user_master`
  - `recorded_info`
- Parsed `score_json` in Python
- Handled mixed score formats (e.g., `13/20`, `15`)
- Computed:
  - Average score
  - Best score
  - Worst score

---

### Technical Decisions
- SQL used only for filtering and joins
- All score calculation logic implemented in Python
- JSON parsing handled using Python `json` module

---

### Problems Faced
- `score_json` stored as text instead of JSON
- Inconsistent key naming (`summery_score`)
- Silent failures due to broad exception handling

---

### Solution
- Explicit JSON parsing in Python
- Defensive `.get()` access for nested keys
- Removed SQL aggregation to meet project constraints

---

### Output
- Region-wise average score
- Best and worst RM score for the region

---

### Evidence
- SQL output verified in pgAdmin
- Python execution verified via terminal

Screenshots available in `docs/screenshots/`
