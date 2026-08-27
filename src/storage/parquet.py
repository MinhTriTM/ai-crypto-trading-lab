"""Parquet helper."""
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

class ParquetStore:
    def __init__(self, base_path: str = "data/processed"):
        self.base = Path(base_path)

    def write(self, table: pa.Table, subpath: str):
        path = self.base / subpath
        path.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(table, str(path), compression="zstd")
        print(f"Wrote parquet {path} rows={table.num_rows}")

    def read(self, subpath: str) -> pa.Table:
        path = self.base / subpath
        return pq.read_table(str(path))

    def append(self, df, subpath: str):
        import pandas as pd
        table = pa.Table.from_pandas(df)
        self.write(table, subpath)
