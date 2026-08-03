from pathlib import Path
import json

import pandas as pd


def normalize_data(data):

    """
    Convert supported formats into pandas DataFrame.
    """

    if isinstance(data, pd.DataFrame):
        return data


    try:
        import numpy as np

        if isinstance(data, np.ndarray):

            return pd.DataFrame(data)

    except ImportError:
        pass


    if isinstance(data, dict):

        return pd.DataFrame(data)


    if isinstance(data, list):

        return pd.DataFrame(data)


    raise TypeError(
        f"Unsupported data type: {type(data)}"
    )



def export_json(df, path):

    path.write_text(
        df.to_json(
            orient="records",
            indent=2
        ),
        encoding="utf-8"
    )



def export_csv(df, path):

    df.to_csv(
        path,
        index=False
    )



def export_html(df, path, title):

    table = df.to_html(
        index=False,
        classes="display",
        table_id="atlas-table"
    )


    html = f"""
<!DOCTYPE html>

<html>

<head>

<title>{title}</title>


<link rel="stylesheet"
href="https://cdn.datatables.net/2.0.0/css/dataTables.dataTables.min.css">


<style>

body {{

    font-family:
    Arial,
    sans-serif;

    padding:40px;

    background:#fafafa;

}}


h1 {{

    color:#1e3a8a;

}}


table {{

    background:white;

}}

</style>


</head>


<body>


<h1>{title}</h1>


{table}



<script src="https://code.jquery.com/jquery-3.7.1.min.js">
</script>


<script src="https://cdn.datatables.net/2.0.0/js/dataTables.min.js">
</script>


<script>

new DataTable(
    '#atlas-table'
);

</script>


</body>

</html>

"""

    path.write_text(
        html,
        encoding="utf-8"
    )



def export_datasets(
    simulation,
    export: bool = True,
):

    for item in simulation.datasets:

        data = item["object"]
        name = item["name"]


        df = normalize_data(
            data
        )


        if not export:

            print(
                f"\n=== {name} ==="
            )

            print(df)

            continue


        output = simulation.output


        export_json(
            df,
            output / f"{name}.json"
        )


        export_csv(
            df,
            output / f"{name}.csv"
        )


        export_html(
            df,
            output / f"{name}.html",
            name
        )


        print(
            f"✓ Exported dataset: {name}"
        )