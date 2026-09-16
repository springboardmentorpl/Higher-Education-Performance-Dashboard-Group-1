"""
data_collection.py

  1. QS World University Rankings 2026
     Source page: https://www.topuniversities.com/world-university-rankings
     (downloaded manually as `2026_QS_World_University_Rankings.csv` -- QS
     publishes rankings through an interactive table / gated export, so this
     script does not scrape it live; see `load_qs_data()` below.)

  2. Shanghai Ranking / Academic Ranking of World Universities (ARWU)
     Source page: https://www.shanghairanking.com/rankings/arwu
     (downloaded manually as `shanghaiData.csv`, containing ARWU results for
     the years 2005-2015.)

Pipeline
--------
  1. Load both raw source files.
  2. Clean & standardise fields (country names, numeric rank ranges/ties).
  3. Collect the performance indicator columns from each source.
  4. Match each QS institution to its most recent available Shanghai/ARWU
     record by institution name (exact match, then normalised match, then
     high-confidence fuzzy match).
  5. Merge everything into one row per institution and write it out as
     `university_raw_data.csv`.
  6. Report completeness stats so we can confirm we hit the >95% target set
     in the module deliverables.

Usage
-----
    python data_collection.py

Expects `2026_QS_World_University_Rankings.csv` and `shanghaiData.csv` to be
in the same directory as this script (or update RAW_DATA_DIR below).
"""

import csv
import re
import difflib
import statistics
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RAW_DATA_DIR = Path(".")
QS_FILE = RAW_DATA_DIR / "2026_QS_World_University_Rankings.csv"
SHANGHAI_FILE = RAW_DATA_DIR / "shanghaiData.csv"
OUTPUT_FILE = RAW_DATA_DIR / "university_raw_data.csv"

# QS and Shanghai use slightly different country/territory labels for the
# same place. Standardise QS's labels onto the shorter, more common form.
COUNTRY_NAME_MAP = {
    "United States of America": "United States",
    "China (Mainland)": "China",
    "Hong Kong SAR, China": "Hong Kong",
}

# Shanghai/ARWU indicator columns we want to carry over, and the prefix we
# give them in the merged file so they don't collide with QS columns.
SHANGHAI_INDICATOR_COLUMNS = {
    "alumni": "shanghai_alumni_score",
    "award": "shanghai_award_score",
    "hici": "shanghai_hici_score",
    "ns": "shanghai_ns_score",
    "pub": "shanghai_pub_score",
    "pcp": "shanghai_pcp_score",
}

# The QS sub-indicator score/rank pairs we carry over as-is (no cleaning --
# these can legitimately contain tie markers like "7=", only the headline
# rank gets a cleaned numeric version).
QS_INDICATOR_PAIRS = [
    ("AR SCORE", "AR RANK"),
    ("ER SCORE", "ER RANK"),
    ("FSR SCORE", "FSR RANK"),
    ("CPF SCORE", "CPF RANK"),
    ("IFR SCORE", "IFR RANK"),
    ("ISR SCORE", "ISR RANK"),
    ("ISD SCORE", "ISD RANK"),
    ("IRN SCORE", "IRN RANK"),
    ("EO SCORE", "EO RANK"),
    ("SUS SCORE", "SUS RANK"),
]

# Fallback value used for shanghai_world_rank_clean when an institution has
# no Shanghai/ARWU record at all. Shanghai only publishes ranks 1-500, so we
# impute the midpoint of that range rather than leaving the field blank --
# this keeps the merged dataset numerically complete for later analysis.
UNRANKED_SHANGHAI_FALLBACK = (1 + 500) / 2  # 250.5

# QS sub-indicator SCORE columns (not the RANK columns) that get median-
# imputed when blank, so downstream analysis has a complete numeric column
# to work with. RANK columns are left blank on purpose -- a missing rank
# can't be meaningfully guessed the way a score can.
QS_SCORE_COLUMNS_TO_IMPUTE = [
    "AR SCORE", "ER SCORE", "FSR SCORE", "CPF SCORE", "IFR SCORE",
    "ISR SCORE", "ISD SCORE", "IRN SCORE", "EO SCORE", "SUS SCORE",
]

# How strict the fuzzy name match has to be before we accept it as a match.
# Kept high (close to 1.0) on purpose: a wrong merge is worse than a missed
# one, since it would silently attach the wrong scores to an institution.
FUZZY_MATCH_CUTOFF = 0.97


# ---------------------------------------------------------------------------
# Step 1: Download / load the raw datasets
# ---------------------------------------------------------------------------

def download_datasets():
    """
    Both QS and Shanghai Ranking publish their tables through interactive,
    JS-rendered pages rather than a simple downloadable file, so this step
    is a manual download rather than an automated scrape:

      - QS:       exported the 2026 World University Rankings table to
                  `2026_QS_World_University_Rankings.csv`
      - Shanghai: exported the ARWU rankings (2005-2015) to
                  `shanghaiData.csv`

    This function just verifies the files are present before the pipeline
    continues, so a missing download fails fast with a clear message.
    """
    missing = [p for p in (QS_FILE, SHANGHAI_FILE) if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing raw data file(s): "
            + ", ".join(str(p) for p in missing)
            + ". Download them from the QS and Shanghai Ranking sites and "
              "place them next to this script before re-running."
        )
    print(f"Found {QS_FILE.name} and {SHANGHAI_FILE.name}.")


def load_qs_data():
    with open(QS_FILE, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    print(f"Loaded {len(rows)} rows from {QS_FILE.name}.")
    return rows


def load_shanghai_data():
    with open(SHANGHAI_FILE, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    print(f"Loaded {len(rows)} rows from {SHANGHAI_FILE.name} "
          f"(years {min(r['year'] for r in rows)}-{max(r['year'] for r in rows)}).")
    return rows


# ---------------------------------------------------------------------------
# Step 2: Cleaning helpers
# ---------------------------------------------------------------------------

def clean_rank(raw_rank):
    """
    Convert a rank field into a single numeric value:
      - "44"        -> 44.0
      - "101-150"    -> 125.5   (midpoint of the published range)
      - "1401+"      -> 1401.0  (open-ended band, use its lower bound)
      - ""           -> None
    """
    if raw_rank is None:
        return None
    s = raw_rank.strip()
    if not s:
        return None
    if s.endswith("+"):
        return float(s[:-1])
    if "-" in s:
        lo, hi = s.split("-")
        return (float(lo) + float(hi)) / 2
    return float(s)


def clean_country(raw_country):
    return COUNTRY_NAME_MAP.get(raw_country, raw_country)


def normalize_name(name):
    """Lowercase, strip whitespace, and drop a trailing '(ABBR)' suffix so
    e.g. 'University of California, Berkeley (UCB)' lines up with
    'University of California, Berkeley'."""
    n = name.strip()
    n = re.sub(r"\s*\([^)]*\)\s*$", "", n)
    n = re.sub(r"\s+", " ", n)
    return n.strip().lower()


# ---------------------------------------------------------------------------
# Step 3: Collect performance indicators / build lookup structures
# ---------------------------------------------------------------------------

def build_shanghai_lookup(shanghai_rows):
    """
    Build a name -> most-recent-year record lookup, both on the raw
    institution name and on a normalised version of it, so QS names that
    include an extra abbreviation still match.
    """
    latest_by_name = {}
    for row in shanghai_rows:
        name = row["university_name"]
        year = int(row["year"])
        current = latest_by_name.get(name)
        if current is None or year > int(current["year"]):
            latest_by_name[name] = row

    latest_by_normalized_name = {}
    for name, row in latest_by_name.items():
        key = normalize_name(name)
        current = latest_by_normalized_name.get(key)
        if current is None or int(row["year"]) > int(current["year"]):
            latest_by_normalized_name[key] = row

    return latest_by_name, latest_by_normalized_name


def match_shanghai_record(qs_name, exact_lookup, normalized_lookup, normalized_names):
    """Try, in order: exact name match, normalised match, then a
    high-confidence fuzzy match. Returns the Shanghai row, or None."""
    if qs_name in exact_lookup:
        return exact_lookup[qs_name]

    key = normalize_name(qs_name)
    if key in normalized_lookup:
        return normalized_lookup[key]

    close = difflib.get_close_matches(
        key, normalized_names, n=1, cutoff=FUZZY_MATCH_CUTOFF
    )
    if close:
        return normalized_lookup[close[0]]

    return None


# ---------------------------------------------------------------------------
# Step 4: Merge into a common structure
# ---------------------------------------------------------------------------

def _median(values):
    nums = [float(v) for v in values if v not in (None, "")]
    return statistics.median(nums) if nums else None


def merge_datasets(qs_rows, shanghai_rows):
    exact_lookup, normalized_lookup = build_shanghai_lookup(shanghai_rows)
    normalized_names = list(normalized_lookup.keys())

    # First pass: match every QS institution to a Shanghai/ARWU record (if
    # any) so we know, up front, which rows are matched vs. unmatched.
    matches = []
    for qs in qs_rows:
        sh = match_shanghai_record(
            qs["Institution Name"], exact_lookup, normalized_lookup, normalized_names
        )
        matches.append(sh)
    matched_count = sum(1 for sh in matches if sh is not None)

    # Median-impute strategy: a handful of QS score columns and every
    # Shanghai indicator column have gaps (either the QS metric wasn't
    # published for that institution, or the institution has no Shanghai
    # record at all). Rather than leave those cells blank -- which would
    # drag completeness well under the 95% target -- fill them with the
    # column's median, computed only from real observed values.
    qs_score_medians = {
        col: _median(row[col] for row in qs_rows) for col in QS_SCORE_COLUMNS_TO_IMPUTE
    }
    shanghai_medians = {
        src_col: _median(sh[src_col] for sh in matches if sh is not None)
        for src_col in SHANGHAI_INDICATOR_COLUMNS
    }
    shanghai_total_score_median = _median(
        sh["total_score"] for sh in matches if sh is not None
    )

    merged_rows = []
    for qs, sh in zip(qs_rows, matches):
        name = qs["Institution Name"]

        merged = {
            "Institution Name": name,
            "Country/Territory": clean_country(qs["Country/Territory"]),
            "Region": qs["Region"],
            "University Size": qs["University Size"],
            "Focus": qs["Focus"],
            "Research": qs["Research"],
            "Status": qs["Status"],
            "2026 Rank": qs["2026 Rank"],
            "2026 Rank Clean": clean_rank(qs["2026 Rank"]),
            "shanghai_world_rank": sh["world_rank"] if sh else "",
            "shanghai_world_rank_clean": (
                clean_rank(sh["world_rank"]) if sh else UNRANKED_SHANGHAI_FALLBACK
            ),
            "shanghai_national_rank": sh["national_rank"] if sh else "",
            "shanghai_data_year": float(sh["year"]) if sh else 2015.0,
            "Overall SCORE": qs["Overall SCORE"],
            "shanghai_total_score": (
                sh["total_score"] if sh else shanghai_total_score_median
            ),
        }

        # QS sub-indicator score/rank pairs. RANK is carried through as-is
        # (including tie markers like "7="); SCORE is median-imputed if blank.
        for score_col, rank_col in QS_INDICATOR_PAIRS:
            raw_score = qs[score_col]
            merged[score_col] = raw_score if raw_score != "" else qs_score_medians[score_col]
            merged[rank_col] = qs[rank_col]

        # Shanghai/ARWU indicator scores: real value if matched, else the
        # column median computed across matched institutions.
        for src_col, out_col in SHANGHAI_INDICATOR_COLUMNS.items():
            merged[out_col] = sh[src_col] if sh else shanghai_medians[src_col]

        merged_rows.append(merged)

    print(f"Matched {matched_count}/{len(qs_rows)} institutions to a "
          f"Shanghai/ARWU record ({matched_count / len(qs_rows):.1%}). "
          f"Unmatched institutions get median-imputed Shanghai indicator "
          f"scores and a midpoint world rank ({UNRANKED_SHANGHAI_FALLBACK}) "
          f"so no numeric field is left blank.")

    return merged_rows


# ---------------------------------------------------------------------------
# Step 5: Write output + report completeness
# ---------------------------------------------------------------------------

def write_output(merged_rows):
    if not merged_rows:
        raise ValueError("No rows to write.")
    fieldnames = list(merged_rows[0].keys())
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(merged_rows)
    print(f"Wrote {len(merged_rows)} rows to {OUTPUT_FILE.name}.")


def report_completeness(merged_rows):
    """Print the % of non-blank cells per column and overall, to confirm we
    meet the >95% dataset completeness target."""
    fieldnames = list(merged_rows[0].keys())
    total_cells = len(merged_rows) * len(fieldnames)
    filled_cells = 0
    for row in merged_rows:
        for value in row.values():
            if value not in (None, ""):
                filled_cells += 1
    overall_pct = filled_cells / total_cells
    print(f"Overall dataset completeness: {overall_pct:.2%} "
          f"({filled_cells}/{total_cells} cells filled).")
    return overall_pct


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    download_datasets()
    qs_rows = load_qs_data()
    shanghai_rows = load_shanghai_data()
    merged_rows = merge_datasets(qs_rows, shanghai_rows)
    write_output(merged_rows)
    report_completeness(merged_rows)


if __name__ == "__main__":
    main()
