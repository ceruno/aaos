This function fetches all the information from a Freshservice endpoint like `/tickets` and exports it to any configured connector (Elastic, Grafana Loki, DataSet).

!!! note annotate "[Endpoint]"  

    ``` http
    GET /exports/fresh
    ```

    [Endpoint]: ../exports/fresh "Direct Link"

## Tickets

To export all tickets, the job item is `tickets`. If you configured an Elastic connector you must set the index in which the data should be stored. 
Optionally you can set the Elastic pipeline to process the data further.

!!! example

    ``` json
    {
        "item": "tickets",
        "index": "fresh-tickets",
        "pipeline": "fresh-tickets-pipeline"
    }
    ```