#!/usr/bin/env bash

#####
## ## CRAWLER INGEST JOB CONFIG
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

JOB_NAME="NGA_S3_UPLOAD"
JOB_SCRIPT="${REPO_DIR}/paasJobs/jobs/s3_upload.sh"
SEND_NOTIFICATIONS="${SEND_NOTIFICATIONS:-yes}"
UPLOAD_LOGS="${UPLOAD_LOGS:-yes}"
SLACK_HOOK_CHANNEL="${SLACK_HOOK_CHANNEL}"
SLACK_HOOK_URL="${SLACK_HOOK_URL}"
S3_BASE_LOG_PATH_URL="${S3_BASE_LOG_PATH_URL:-s3://advana-raw-zone/gamechanger/data-pipelines/orchestration/logs/NGA-s3-upload}"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-gov-west-1}"
CLEANUP="${CLEANUP:-yes}"
TMPDIR="${TMPDIR:-/data/tmp}"
VENV_ACTIVATE_SCRIPT="${VENV_ACTIVATE_SCRIPT:-/opt/gc-venv-current/bin/activate}"
# PYTHONPATH="${PYTHONPATH:-$REPO_DIR}"

## JOB SPECIFIC CONF

export ES_INDEX_NAME="NGA_20210803"
export ES_ALIAS_NAME="NGA"

export S3_RAW_INGEST_PREFIX="advana-raw-zone/gamechanger-test/pdf" #pdf and metadata path
export S3_PARSED_INGEST_PREFIX=""

export MAX_OCR_THREADS_PER_FILE="${MAX_OCR_THREADS_PER_FILE:-2}"
export MAX_PARSER_THREADS="${MAX_PARSER_THREADS:-16}"
export MAX_NEO4J_THREADS=""

export S3_BUCKET_NAME="${S3_BUCKET_NAME:-advana-raw-zone}"

export SKIP_NEO4J_UPDATE="yes"
export SKIP_SNAPSHOT_BACKUP="no"
export SKIP_DB_BACKUP="yes"
export SKIP_DB_UPDATE="yes"
export SKIP_REVOCATION_UPDATE="yes"
export SKIP_THUMBNAIL_GENERATION="yes"
export FORCE_OCR="no"

export CURRENT_SNAPSHOT_PREFIX="gamechanger/projects/nga/"
export BACKUP_SNAPSHOT_PREFIX="gamechanger/projects/nga/backup/"
export LOAD_ARCHIVE_BASE_PREFIX="gamechanger/projects/nga/load-archive/"
export DB_BACKUP_BASE_PREFIX="gamechanger/projects/nga/backup/db/"

export CLONE_OR_CORE="clone"

export RELATIVE_CRAWLER_OUTPUT_LOCATION="${RELATIVE_CRAWLER_OUTPUT_LOCATION:-raw_docs/crawler_output.json}"

