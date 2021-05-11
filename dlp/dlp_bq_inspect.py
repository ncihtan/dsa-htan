from google.cloud import bigquery
from google.cloud import dlp_v2

project_name = "htan-dcc"
source_dataset = "combined_assays"
dest_dataset = "cloud_dlp_test"
inspect_template = "projects/htan-dcc/locations/global/inspectTemplates/dcc-phi"

client = dlp_v2.DlpServiceClient()

tables = [
    'ClinicalDataTier1',
    'ClinicalDataTier2',
    'BreastCancerTier3',
    'LungCancerTier3',
    'Biospecimen',
    'BulkRNA-seqLevel1',
    'BulkWESLevel1',
    'ImagingLevel2',
    'ScRNA-seqLevel1',
    'ScRNA-seqLevel2',
    'ScRNA-seqLevel3',
    'ScRNA-seqLevel4'
]

for table in tables:
  inspect_job = {
      "actions": [
        {
          "save_findings": {
            "output_config": {
              "table": {
                "project_id": project_name,
                "table_id": '{}_DLP'.format(table),
                "dataset_id": dest_dataset
              }
            }
          }
        }
      ],
      "inspect_template_name": inspect_template,
      "storage_config": {
        "big_query_options": {
          "table_reference": {
            "project_id": project_name,
            "table_id": table,
            "dataset_id": source_dataset
            }
          }
    }
  }

  client.create_dlp_job(parent='projects/'+project_name, inspect_job=inspect_job)
















