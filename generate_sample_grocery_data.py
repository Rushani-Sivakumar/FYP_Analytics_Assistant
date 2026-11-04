
from pathlib import Path
import random
import pandas as pd

from src.data_gen.generate_tables import generate_source_table, make_headers

# -----------------------------------
# Configuration
# -----------------------------------

SEED = 42
NUM_TABLES_PER_TYPE = 10

TABLE_TYPES = ["sales", "inventory", "purchases"]
HEADER_STYLES = ["canonical", "alias", "missing", "generic"]

# Project root directory
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def generate_and_save():
    rng = random.Random(SEED)

    for table_type in TABLE_TYPES:

        # Create a folder for each table type
        output_dir = DATA_DIR / table_type
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\nGenerating {table_type} tables...")

        for i in range(1, NUM_TABLES_PER_TYPE + 1):

            # 1. Generate clean and dirty tables
            clean_df, dirty_df, level = generate_source_table(
                rng, table_type
            )

            # 2. Select a header style
            header_style = rng.choice(HEADER_STYLES)

            # 3. Generate headers
            labels = list(dirty_df.columns)

            headers = make_headers(
                rng,
                labels,
                header_style,
                split="train"
            )

            # 4. Apply the same headers to both tables
            clean_df.columns = headers
            dirty_df.columns = headers

            # 5. Create output filenames
            filename = f"{table_type}_{i:03d}"

            clean_path = output_dir / f"{filename}_clean.csv"
            dirty_path = output_dir / f"{filename}_dirty.csv"

            # 6. Save CSV files
            clean_df.to_csv(
                clean_path,
                index=False,
                encoding="utf-8-sig"
            )

            dirty_df.to_csv(
                dirty_path,
                index=False,
                encoding="utf-8-sig"
            )

            print(
                f"Saved {filename} | "
                f"Rows: {len(clean_df)} | "
                f"Corruption level: {level} | "
                f"Headers: {header_style}"
            )

    print("\nAll tables generated successfully!")
    print(f"Output directory: {DATA_DIR}")


if __name__ == "__main__":
    generate_and_save()
