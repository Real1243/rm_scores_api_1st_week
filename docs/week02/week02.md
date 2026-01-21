## Week 2 – Region-based RM Score Analysis

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
- Achieved a stable working query integrated with Python.
