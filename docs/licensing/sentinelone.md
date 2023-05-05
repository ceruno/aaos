This function fetches all the licensing information from SentinelOne accounts and sites.

!!! note annotate "Endpoint"  

    ``` http
    GET /licensing/s1
    ```

## Expiration

The expiration function discovers accounts and sites below the threshold and creates or updates therefore Jira issues or Freshservice tickets.

!!! info "Threshold"  

    The thresholds are currently hard coded and set to `30 days`.  

To check for the expiration, the job item is `expiration`. Use `jira` or `fresh` as target.  
The project key is used for `jira` only and case sensitive.

!!! example

    ``` json
    {
        "item": "expiration",
        "target": "jira",
        "project": "SENTINELONE"
    }
    ```

## Usage

The usage function discovers accounts and sites above the threshold and creates or updates therefore Jira issues or Freshservice tickets.

!!! info "Threshold"  

    The thresholds are currently hard coded and set to:  

    - Overprovisioning is larger than `5%` but at least `10 agents`.  
    - Overprovisioning is larger than `100 agents`.

To check for the usage, the job item is `usage`. Use `jira` or `fresh` as destination.  
The project key is used for `jira` only and case sensitive.

!!! example

    ``` json
    {
        "item": "usage",
        "target": "jira",
        "project": "SENTINELONE"
    }
    ```
