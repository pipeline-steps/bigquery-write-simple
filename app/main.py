import timeit
import pandas
import pandas_gbq
from steputil import StepArgs, StepArgsBuilder


def main(step: StepArgs):
    # Loading dataframe
    df = pandas.DataFrame(step.input.readJsons())
    print(f"Read {len(df)} rows with {len(df.columns)} columns")

    # Writing to BQ table
    start_time = timeit.default_timer()
    print(f"Loading data to {step.config.tableId} (using project {step.config.billingProject} for billing)")
    pandas_gbq.to_gbq(df, step.config.tableId, project_id=step.config.tableId, if_exists=step.config.tableId.ifExists)
    execution_time = timeit.default_timer() - start_time
    print(f"Uploaded {len(df.columns)} columns and {len(df)} rows in in {execution_time:.1f} seconds.")

    print(f"Done")


if __name__ == "__main__":
    main(StepArgsBuilder()
         .input()
         .config("billingProject")
         .config("tableId", optional=True)
         .config("ifExists", default_value="append")
         .build()
         )
