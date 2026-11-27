# gcloud reference

## Get environment information

Command to get the configuration of the environment:

```bash
gcloud composer environments describe {env_name} --project={env_project} --location={env_region} --format=yaml
```

## List files in the environment's bucket

Command to list the contents of `dags/` directory in the environment's bucket:

```bash
DAGS_FOLDER=$(gcloud composer environments describe {env_name} --project={env_project} --location={env_region} --format="value(config.dagGcsPrefix)")
gcloud storage ls $DAGS_FOLDER
```

## Fetch environment logs

Command to fetch log entries from Cloud Logging:

```bash
gcloud logging read {filter} --limit=50 --format="yaml(logName,severity,labels,textPayload,timestamp)"
```

**How to build the filter:**

1.  ALWAYS include these conditions:

```text
resource.type="cloud_composer_environment" AND
resource.labels.project_id={env_project} AND
resource.labels.location={env_region} AND
resource.labels.environment_name={env_name}
```

2.  Optionally include `AND logName={log_name}` to fetch logs of a specific
    component. `log_name` is one of:

    -   `projects/{env_project}/logs/airflow-scheduler`
    -   `projects/{env_project}/logs/airflow-triggerer`
    -   `projects/{env_project}/logs/airflow-webserver`
    -   `projects/{env_project}/logs/airflow-worker`
    -   `projects/{env_project}/logs/airflow-k8s-operator`
    -   `projects/{env_project}/logs/airflow-k8s-worker`
    -   `projects/{env_project}/logs/dag-processor-manager`
    -   `projects/{env_project}/logs/db-retention`
    -   `projects/{env_project}/logs/build-log`

3.  Optionally include condition like `AND timestamp <= "2026-01-01T00:00:00Z"`
    to fetch logs from a specific timeframe.
