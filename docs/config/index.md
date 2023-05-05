## Connectors & Workloads

To create some workloads you need to configure some connectors first. The `config` endpoint aggregates the available connectors and also the available settings to schedule any of the available workloads.

!!! note annotate "Endpoint"  

    ``` http
    GET /config/
    ```

## Users

In case you want to create additional users use the `users` endpoint.

!!! note annotate "Endpoint"  

    The users endpoint contains the user and group settings.

    ``` http
    GET /users/
    ```