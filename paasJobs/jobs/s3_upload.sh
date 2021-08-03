#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

#####
## ## MAIN COMMANDS
#####

function run_core_ingest() {

  local job_dir="$LOCAL_TMP_DIR"
  local job_ts="$JOB_TS"

  local bucket_name="$S3_BUCKET_NAME"

  local es_index_name="$ES_INDEX_NAME"
  local es_alias_name="${ES_ALIAS_NAME:-}"

  local skip_neo4j_update="$SKIP_NEO4J_UPDATE"
  local skip_snapshot_backup="$SKIP_SNAPSHOT_BACKUP"
  local skip_db_backup="$SKIP_DB_BACKUP"
  local skip_db_update="$SKIP_DB_UPDATE"
  local skip_revocation_update="$SKIP_REVOCATION_UPDATE"
  local skip_thumbnail_generation="$SKIP_THUMBNAIL_GENERATION"
  local force_ocr="$FORCE_OCR"

  local max_ocr_threads="${MAX_OCR_THREADS_PER_FILE:-4}"
  local max_parser_threads="${MAX_PARSER_THREADS:-16}"
  local max_neo4j_threads="${MAX_PARSER_THREADS:-16}"

  local s3_raw_ingest_prefix="${S3_RAW_INGEST_PREFIX}"
  local s3_parsed_ingest_prefix="${S3_PARSED_INGEST_PREFIX}"

  local current_snapshot_prefix="${CURRENT_SNAPSHOT_PREFIX:-gamechanger/}"
  local backup_snapshot_prefix="${BACKUP_SNAPSHOT_PREFIX:-gamechanger/backup/}"
  local load_archive_base_prefix="${LOAD_ARCHIVE_BASE_PREFIX:-gamechanger/load-archive/}"
  local db_backup_base_prefix="${DB_BACKUP_BASE_PREFIX:-gamechanger/backup/db/}"
  local metadata_creation_group="${METADATA_CREATION_GROUP:-}"
  local clone_or_core="${CLONE_OR_CORE:-core}"

  python -m dataPipelines.gc_ingest pipelines $clone_or_core ingest \
    --skip-neo4j-update="$skip_neo4j_update" \
    --skip-snapshot-backup="$skip_snapshot_backup" \
    --skip-db-backup="$skip_db_backup" \
    --skip-db-update="$skip_db_update" \
    --current-snapshot-prefix="$current_snapshot_prefix" \
    --backup-snapshot-prefix="$backup_snapshot_prefix" \
    --db-backup-base-prefix="$db_backup_base_prefix" \
    --load-archive-base-prefix="$load_archive_base_prefix" \
    --bucket-name="$bucket_name" \
    --job-dir="$job_dir" \
    --batch-timestamp="$job_ts" \
    --index-name="$es_index_name" \
    --alias-name="$es_alias_name" \
    --max-threads="$max_parser_threads" \
    --max-threads-neo4j="$max_neo4j_threads" \
    --max-ocr-threads="$max_ocr_threads" \
    s3 \
    --s3-raw-ingest-prefix="$s3_raw_ingest_prefix" \
    --s3-parsed-ingest-prefix="$s3_parsed_ingest_prefix" \
    --metadata-creation-group="$metadata_creation_group"
}

##### ##### #####
## ## ## ## ## ## ACTUAL EXEC FLOW
##### ##### #####

SECONDS=0
cat <<EOF

  STARTING PIPELINE RUN
  $(date "+DATE: %Y-%m-%d TIME: %H:%M:%S")

EOF

# main
run_core_ingest

cat <<EOF

  SUCCESSFULLY FINISHED PIPELINE RUN
  $(date "+DATE: %Y-%m-%d TIME: %H:%M:%S")

EOF

# how long?
duration=$SECONDS
echo -e "\n $(( $SECONDS / 3600 ))h $(( ($SECONDS % 3600)/60 ))m $(($SECONDS % 60))s elapsed."
