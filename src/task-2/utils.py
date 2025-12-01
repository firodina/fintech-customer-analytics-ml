# src/task-2/utils.py
from pathlib import Path
import pandas as pd

# Absolute path to project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data directories
DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"


def load_reviews(filename=None):
    """
    Load reviews CSV. Auto-detect if filename not provided.
    """
    if filename:
        file_path = DATA_DIR / filename
        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} does not exist.")
    else:
        csv_files = list(DATA_DIR.glob("*.csv"))
        if len(csv_files) == 0:
            raise FileNotFoundError(f"No CSV files found in {DATA_DIR}")
        elif len(csv_files) > 1:
            raise FileExistsError(
                f"Multiple CSV files found: {csv_files}. Specify filename explicitly."
            )
        file_path = csv_files[0]

    print(f"Loading CSV: {file_path}")
    return pd.read_csv(file_path)
