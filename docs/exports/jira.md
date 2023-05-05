This function fetches all the information from a Jira endpoint like `/rest/api/3/search` and exports it to any configured connector (Elastic, Grafana Loki, DataSet).

!!! note annotate "Endpoint"  

    ``` http
    GET /exports/jira
    ```

## Issues

To export all issues, the job item is `issues`. Use wether a jql query or a specific project. If you configured an Elastic connector you must set the index in which the data should be stored. 
Optionally you can set the Elastic pipeline to process the data further.

!!! example

    ``` json
    {
        "item": "issues",
        "jql": "",
        "project": "updated >= -30d AND project != TEMPL",
        "index": "jira-issues",
        "pipeline": "jira-issues-pipeline"
    }
    ```