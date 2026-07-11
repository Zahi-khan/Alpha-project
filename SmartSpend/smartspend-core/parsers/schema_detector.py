from parsers.column_mapper import map_columns


def detect_schema(df):

    mapping = map_columns(
        list(df.columns)
    )

    if "date" not in mapping:
        raise ValueError(
            "No date column detected."
        )

    if "amount" not in mapping:
        raise ValueError(
            "No amount column detected."
        )

    return mapping