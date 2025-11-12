# bigquery-write-simple

Writing data to a bigquery table (simple version)

## Docker Image

This application is available as a Docker image on Docker Hub: `pipelining/bigquery-write-simple`

### Usage

```bash
docker run -v /path/to/config.json:/config.json \
           -v /path/to/input:/input \
           -v /path/to/credentials.json:/credentials.json \
           -e GOOGLE_APPLICATION_CREDENTIALS=/credentials.json \
           pipelining/bigquery-write-simple:latest \
           --config /config.json \
           --input /input/data.jsonl
```

To see this documentation, run without arguments:
```bash
docker run pipelining/bigquery-write-simple:latest
```

## Parameters

| Name           | Required | Description                                                    |
|----------------|----------|----------------------------------------------------------------|
| billingProject | X        | the GCP project id to be used as quota project                 |
| tableId        | X        | bigquery table to be written to (format project.dataset.table) |
| ifExists       |          | possible values: fail, replace, append (default is append)     |
| partitionField |          | name of the TIMESTAMP/DATE/DATETIME field to partition by (daily partitioning) |

**Notes:**
  * billingProject: the user/service account needs to have bigquery.jobs.create permission on this project
  * tableId: the user/service account needs to have bigquery.tables.updateData and (possibly) bigquery.tables.create permission on this table
  * ifExists: checks if the table already exists and acts correspondingly in this case (issue an error, replace table data with new data, append new data to table)
  * partitionField: if specified, the table will be partitioned by day using the specified field. The field must be of type TIMESTAMP, DATE, or DATETIME. Partitioning improves query performance and reduces costs when querying specific date ranges.

