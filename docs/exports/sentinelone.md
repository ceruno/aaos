This function fetches all the information from a SentinelOne endpoint like `/web/api/v2.1/agents` and exports it to any configured connector (Elastic, Grafana Loki, DataSet).

!!! note annotate "Endpoint"  

    ``` http
    GET /exports/s1
    ```

## Agents

To export all agents, the job item is `agents`. If you configured an Elastic connector you must set the index in which the data should be stored. 
Optionally you can set the Elastic pipeline to process the data further.

!!! example

    ``` json
    {
        "item": "agents",
        "index": "sentinelone-agents",
        "pipeline": "sentinelone-agents-pipeline",
        "limit": "",
        "timedelta": ""
    }
    ```

## Activities

To export all activities, the job item is `activities`. If you configured an Elastic connector you must set the index in which the data should be stored. 
Optionally you can set the Elastic pipeline to process the data further.

!!! example

    ``` json
    {
        "item": "activities",
        "index": "sentinelone-activities",
        "pipeline": "",
        "limit": "",
        "timedelta": "2"
    }
    ```