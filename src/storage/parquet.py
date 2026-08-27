"""Parquet helper - fallback to CSV neu thieu pyarrow."""
from pathlib import Path
try:
    import pyarrow as pa
    import pyarrow.parquet as pq
    _HAS_PYARROW = True
except ImportError:
    _HAS_PYARROW = False
    pa = None
    pq = None

class ParquetStore:
    def __init__(self, base_path: str = "data/processed"):
        self.base = Path(base_path)

    def write(self, table, subpath: str):
        path = self.base / subpath
        path.parent.mkdir(parents=True, exist_ok=True)
        if _HAS_PYARROW and pa and hasattr(table, 'num_rows'):
            pq.write_table(table, str(path), compression="zstd")
            print(f"Wrote parquet {path} rows={table.num_rows}")
        else:
            # fallback: table la DataFrame
            import pandas as pd
            if hasattr(table, 'to_pandas'):
                df = table.to_pandas()
            else:
                df = table
            # luu csv neu khong co pyarrow
            csv_path = path.with_suffix('.csv')
            df.to_csv(csv_path, index=False)
            print(f"pyarrow missing - saved CSV {csv_path} rows={len(df)} (parquet would be {path})")

    def read(self, subpath: str):
        path = self.base / subpath
        if _HAS_PYARROW:
            return pq.read_table(str(path))
        else:
            import pandas as pd
            csv_path = path.with_suffix('.csv')
            if csv_path.exists():
                return pd.read_csv(csv_path)
            raise FileNotFoundError(f"pyarrow missing, parquet not available {path}")

    def append(self, df, subpath: str):
        if _HAS_PYARROW:
            table = pa.Table.from_pandas(df)
            self.write(table, subpath)
        else:
            # fallback csv
            self.write(df, subpath)
