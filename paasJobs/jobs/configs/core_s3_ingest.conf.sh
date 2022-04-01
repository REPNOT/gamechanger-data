#!/usr/bin/env bash

#####
## ## S3 INGEST JOB CONFIG
#####
#
## USAGE (CRON or OTHERWISE):
#     env <envvar1=val1 envvar2=val2 ...> <path-to/job_runner.sh> <path-to/this.conf.sh>
#
## NOTE all env vars that don't have defaults must be exported ahead of time or passed via `env` command
#
## MINIMAL EXAMPLE:
#     env SLACK_HOOK_CHANNEL="#some-channel" SLACK_HOOK_URL="https://slack/hook" /app/job_runner.sh /app/somejob.conf.sh
#

readonly SCRIPT_PARENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
readonly REPO_DIR="$( cd "$SCRIPT_PARENT_DIR/../../../"  >/dev/null 2>&1 && pwd )"

## BASE JOB_CONF

JOB_NAME="${JOB_NAME:-S3_INGEST}"
JOB_SCRIPT="${REPO_DIR}/paasJobs/jobs/s3_ingest.sh"
SEND_NOTIFICATIONS="${SEND_NOTIFICATIONS:-yes}"
UPLOAD_LOGS="${UPLOAD_LOGS:-yes}"
SLACK_HOOK_CHANNEL="${SLACK_HOOK_CHANNEL}"
SLACK_HOOK_URL="${SLACK_HOOK_URL}"
S3_BASE_LOG_PATH_URL="${S3_BASE_LOG_PATH_URL:-s3://advana-data-zone/bronze/gamechanger/data-pipelines/orchestration/logs/core-s3-ingest}"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-gov-west-1}"
CLEANUP="${CLEANUP:-yes}"
TMPDIR="${TMPDIR:-/data/tmp}"
VENV_ACTIVATE_SCRIPT="${VENV_ACTIVATE_SCRIPT:-/opt/gc-venv-current/bin/activate}"
# PYTHONPATH="${PYTHONPATH:-$REPO_DIR}"

## JOB SPECIFIC CONF

export ES_INDEX_NAME="${ES_INDEX_NAME:-gamechanger_20210618}"
export ES_ALIAS_NAME="${ES_ALIAS_NAME:-}"

export METADATA_CREATION_GROUP="${METADATA_CREATION_GROUP:-}"

export S3_RAW_INGEST_PREFIX="${S3_RAW_INGEST_PREFIX:-}" #pdf and metadata path
export S3_PARSED_INGEST_PREFIX="${S3_PARSED_INGEST_PREFIX:-}"

export MAX_OCR_THREADS_PER_FILE="${MAX_OCR_THREADS_PER_FILE:-2}"
export MAX_PARSER_THREADS="${MAX_PARSER_THREADS:-16}"
export MAX_S3_THREADS="${MAX_S3_THREADS:-32}"

export S3_BUCKET_NAME="${S3_BUCKET_NAME:-advana-data-zone}"

export SKIP_NEO4J_UPDATE="${SKIP_NEO4J_UPDATE:-no}"
export SKIP_SNAPSHOT_BACKUP="${SKIP_SNAPSHOT_BACKUP:-yes}"
export SKIP_DB_BACKUP="${SKIP_DB_BACKUP:-no}"
export SKIP_DB_UPDATE="${SKIP_DB_UPDATE:-no}"
export SKIP_REVOCATION_UPDATE="${SKIP_REVOCATION_UPDATE:-no}"
export SKIP_THUMBNAIL_GENERATION="${SKIP_THUMBNAIL_GENERATION:-no}"

export CURRENT_SNAPSHOT_PREFIX="${CURRENT_SNAPSHOT_PREFIX:-bronze/gamechanger/}"
export BACKUP_SNAPSHOT_PREFIX="${BACKUP_SNAPSHOT_PREFIX:-bronze/gamechanger/backup/}"
export LOAD_ARCHIVE_BASE_PREFIX="${LOAD_ARCHIVE_BASE_PREFIX:-bronze/gamechanger/load-archive/}"
export DB_BACKUP_BASE_PREFIX="${DB_BACKUP_BASE_PREFIX:-bronze/gamechanger/backup/db/}"

export CLONE_OR_CORE="${CLONE_OR_CORE:-"core"}"