This function fetches all the information from a Postgres Database and exports it to any configured connector (Elastic, Grafana Loki, DataSet).

!!! note annotate "[Endpoint]"  

    ``` http
    GET /exports/postgres
    ```

    [Endpoint]: ../exports/postgres "Direct Link"

## Table

!!! example

    ``` json
    {
        "item": "table",
        "query": "SELECT * FROM public.Table",
        "index": "postgres-data",
        "pipeline": ""
    }
    ```