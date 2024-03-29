# Home

AAOS means Analysis, Automation and Orchestration System. AAOS is a cloud native web application based on [Django Rest Framework] for different workloads, developed by [Ceruno AG].

[Django Rest Framework]: https://www.django-rest-framework.org/
[Ceruno AG]: https:/ceruno.ch

## Workloads

### Data Exports

Export data fetched from an API as json objects to a data lake from sources like SentinelOne, Jira, Freshservice or Postgres to Elastic, Grafana Loki or DataSet (SentinelOne).

### Data Analysis

Analyse the Activity stream of SentinelOne e.g create an alert if a an update request was sent to an agent and the update did not succeed between the next 60 minutes.

### Licensing Monitoring

Monitor the license usage and expiration dates of SentinelOne. Conditionally create or update corresponding Jira issues or Freshservice tickets.
