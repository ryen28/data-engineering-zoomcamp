terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
# Credentials only needs to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS set
  credentials = file(var.credentials) # COULD use this (hardcode), or set the echo GOOGLE_CREDENTIALS
  project = var.project
  region  = var.region
}


# demo-bucket is a label / local name
# name attribute needs to be a very unique number (globally across all gcp)
resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true


  # Optional, but recommended settings:
  #storage_class = "STANDARD"
  #uniform_bucket_level_access = true

  #versioning {
   # enabled     = true
  #}

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }

  # force_destroy = true
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
  location = var.location

}
