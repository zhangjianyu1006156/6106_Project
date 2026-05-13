"""
Data preparation for the Zomato delivery optimization project.

This script creates:
1. A cleaned full dataset with valid coordinates, key fields, city code, and time fields.
2. A main Jaipur optimization sample.
3. Two robustness samples for Mumbai and Hyderabad.
4. A compact summary table describing the generated datasets.

Run from the project folder:
    python3 scripts/member1_data_cleaning.py
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "Zomato Dataset.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

MAIN_CITY_CODE = "JAP"
ROBUSTNESS_CITY_CODES = {
    "MUM": "robustness_mumbai.csv",
    "HYD": "robustness_hyderabad.csv",
}

PEAK_START_HOUR = 17
PEAK_END_HOUR = 23
SAMPLE_SIZE = 50
RANDOM_SEED = 6106

COORD_COLUMNS = [
    "Restaurant_latitude",
    "Restaurant_longitude",
    "Delivery_location_latitude",
    "Delivery_location_longitude",
]

KEY_COLUMNS = [
    "ID",
    "Delivery_person_ID",
    "Restaurant_latitude",
    "Restaurant_longitude",
    "Delivery_location_latitude",
    "Delivery_location_longitude",
    "Order_Date",
    "Time_Orderd",
    "Time_Order_picked",
    "Weather_conditions",
    "Road_traffic_density",
    "City",
    "Type_of_vehicle",
    "Vehicle_condition",
    "multiple_deliveries",
    "Time_taken (min)",
]


def extract_city_code(delivery_person_id: object) -> str | None:
    """Extract real city code from IDs such as JAPRES14DEL02."""
    if pd.isna(delivery_person_id):
        return None
    match = re.match(r"^([A-Z]+)RES", str(delivery_person_id))
    return match.group(1) if match else None


def clean_raw_data(raw_file: Path) -> pd.DataFrame:
    """Clean the raw Zomato dataset and add fields needed for optimization."""
    df = pd.read_csv(raw_file)
    df = df.copy()

    initial_rows = len(df)

    df = df.dropna(
        subset=[
            "Time_Orderd",
            "Weather_conditions",
            "Road_traffic_density",
            "City",
        ]
    )

    df = df[~df[COORD_COLUMNS].eq(0).any(axis=1)].copy()

    df["city_code"] = df["Delivery_person_ID"].apply(extract_city_code)
    df = df.dropna(subset=["city_code"])

    df["order_date"] = pd.to_datetime(
        df["Order_Date"],
        format="%d-%m-%Y",
        errors="coerce",
    )
    df["order_time"] = pd.to_datetime(
        df["Time_Orderd"],
        format="%H:%M",
        errors="coerce",
    ).dt.time
    df["pickup_time"] = pd.to_datetime(
        df["Time_Order_picked"],
        format="%H:%M",
        errors="coerce",
    ).dt.time
    df["order_hour"] = pd.to_datetime(
        df["Time_Orderd"],
        format="%H:%M",
        errors="coerce",
    ).dt.hour

    df["time_taken_min"] = pd.to_numeric(df["Time_taken (min)"], errors="coerce")
    df["multiple_deliveries"] = pd.to_numeric(
        df["multiple_deliveries"],
        errors="coerce",
    )

    df = df.dropna(subset=["order_date", "order_hour", "time_taken_min"])

    useful_columns = KEY_COLUMNS + [
        "city_code",
        "order_date",
        "order_time",
        "pickup_time",
        "order_hour",
        "time_taken_min",
    ]
    useful_columns = [col for col in useful_columns if col in df.columns]
    df = df[useful_columns].copy()

    df.attrs["initial_rows"] = initial_rows
    df.attrs["cleaned_rows"] = len(df)
    return df


def select_peak_day_sample(
    cleaned: pd.DataFrame,
    city_code: str,
    sample_size: int = SAMPLE_SIZE,
) -> tuple[pd.DataFrame, dict[str, object]]:
    """
    Select one city, one date, and the evening peak period.

    The selected date is the available date with the largest number of
    valid peak-hour records for that city. If more than sample_size records
    are available, a reproducible random sample is used.
    """
    city_peak = cleaned[
        (cleaned["city_code"] == city_code)
        & (cleaned["order_hour"].between(PEAK_START_HOUR, PEAK_END_HOUR))
    ].copy()

    if city_peak.empty:
        raise ValueError(f"No peak-hour records available for city {city_code}.")

    date_counts = city_peak.groupby("Order_Date").size().sort_values(ascending=False)
    selected_date = date_counts.index[0]
    selected_date_count = int(date_counts.iloc[0])

    scenario = city_peak[city_peak["Order_Date"] == selected_date].copy()
    if len(scenario) > sample_size:
        scenario = scenario.sample(n=sample_size, random_state=RANDOM_SEED)

    scenario = scenario.sort_values(["Order_Date", "Time_Orderd", "ID"]).reset_index(
        drop=True
    )
    scenario.insert(0, "scenario_order_id", range(1, len(scenario) + 1))

    summary = {
        "city_code": city_code,
        "selected_date": selected_date,
        "available_peak_orders_on_selected_date": selected_date_count,
        "sample_orders": len(scenario),
        "peak_start_hour": PEAK_START_HOUR,
        "peak_end_hour": PEAK_END_HOUR,
        "suggested_riders": 5,
        "suggested_capacity_per_rider": "8-10 orders",
    }

    return scenario, summary


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Cannot find raw file: {RAW_FILE}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    cleaned = clean_raw_data(RAW_FILE)
    cleaned_path = OUTPUT_DIR / "cleaned_zomato_full.csv"
    cleaned.to_csv(cleaned_path, index=False)

    summaries: list[dict[str, object]] = []

    main_sample, main_summary = select_peak_day_sample(cleaned, MAIN_CITY_CODE)
    main_path = OUTPUT_DIR / "main_optimization_jaipur.csv"
    main_sample.to_csv(main_path, index=False)
    main_summary["dataset_type"] = "main_optimization"
    main_summary["output_file"] = str(main_path)
    summaries.append(main_summary)

    for city_code, filename in ROBUSTNESS_CITY_CODES.items():
        sample, summary = select_peak_day_sample(cleaned, city_code)
        output_path = OUTPUT_DIR / filename
        sample.to_csv(output_path, index=False)
        summary["dataset_type"] = "robustness"
        summary["output_file"] = str(output_path)
        summaries.append(summary)

    global_summary = {
        "dataset_type": "cleaned_full",
        "city_code": "ALL",
        "selected_date": "ALL",
        "available_peak_orders_on_selected_date": "",
        "sample_orders": len(cleaned),
        "peak_start_hour": "",
        "peak_end_hour": "",
        "suggested_riders": "",
        "suggested_capacity_per_rider": "",
        "output_file": str(cleaned_path),
        "raw_rows": cleaned.attrs.get("initial_rows"),
    }

    summary_df = pd.DataFrame([global_summary] + summaries)
    summary_path = OUTPUT_DIR / "member1_data_summary.csv"
    summary_df.to_csv(summary_path, index=False)

    print("Member 1 data preparation complete.")
    print(f"Cleaned full dataset: {cleaned_path} ({len(cleaned)} rows)")
    print(f"Main optimization dataset: {main_path} ({len(main_sample)} rows)")
    for item in summaries[1:]:
        print(f"Robustness dataset: {item['output_file']} ({item['sample_orders']} rows)")
    print(f"Summary file: {summary_path}")


if __name__ == "__main__":
    main()
