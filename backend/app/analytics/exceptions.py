class DatasetError(Exception):
    """Base error for dataset ingestion."""


class DatasetLoadError(DatasetError):
    """A dataset directory or parquet file could not be read."""


class DatasetValidationError(DatasetError):
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__(
            "Dataset validation failed:\n" + "\n".join(f"- {error}" for error in errors)
        )
