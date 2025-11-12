import timeit
from google.cloud import bigquery
from steputil import StepArgs, StepArgsBuilder


def main(step: StepArgs):
    # Read input data
    records = step.input.readJsons()
    print(f"Read {len(records)} rows")

    # Initialize BigQuery client
    client = bigquery.Client(project=step.config.billingProject)

    # Map ifExists to BigQuery write disposition
    write_disposition_map = {
        'append': bigquery.WriteDisposition.WRITE_APPEND,
        'replace': bigquery.WriteDisposition.WRITE_TRUNCATE,
        'fail': bigquery.WriteDisposition.WRITE_EMPTY
    }

    write_disposition = write_disposition_map.get(step.config.ifExists)
    if write_disposition is None:
        raise ValueError(f"Invalid ifExists value: {step.config.ifExists}. Must be one of: append, replace, fail")

    # Configure load job
    job_config = bigquery.LoadJobConfig(
        write_disposition=write_disposition,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True  # Automatically detect schema from JSON
    )

    # Load data to BigQuery
    start_time = timeit.default_timer()
    print(f"Loading data to {step.config.tableId} (using project {step.config.billingProject} for billing)")

    load_job = client.load_table_from_json(
        records,
        step.config.tableId,
        job_config=job_config
    )

    # Wait for the job to complete
    load_job.result()

    execution_time = timeit.default_timer() - start_time

    # Get the loaded table to show statistics
    table = client.get_table(step.config.tableId)
    print(f"Uploaded {len(table.schema)} columns and {load_job.output_rows} rows in {execution_time:.1f} seconds.")

    print(f"Done")


if __name__ == "__main__":
    main(StepArgsBuilder()
         .input()
         .config("billingProject")
         .config("tableId")
         .config("ifExists", default_value="append")
         .build()
         )
