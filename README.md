# dataintegration_parquet2adw
oracle functions used with python to trigger a data integration 

The function assumes that a data integration flow and application are created. Function will trigger the integration to run - e.g. in a case where new parquet files are added to object storage and need to be moved into the Autonomous Data Warehouse. 

The task which is triggered does not necessary need to be parquet to ADW. It could be any predefined data integration flow. 

To run the function requires a tast_key, application_id, workspace_id to be referencable 

