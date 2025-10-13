#!/usr/bin/env python3
"""
analyze_image.py  —  Foundational Rekognition pipeline

What it does (per your spec):
1) Scans ./images for .jpg/.jpeg/.png
2) Uploads each file to s3://$S3_BUCKET/rekognition-input/$STAGE/<filename>
3) Calls Rekognition detect_labels on that S3 object
4) Writes a record to DynamoDB table $DYNAMODB_TABLE with:
   {
     "filename": "rekognition-input/<stage>/<filename>",
     "labels": [{"Name":"...", "Confidence": 98.49}, ...],
     "timestamp": "2025-06-01T14:55:32Z",
     "branch": "<git or provided branch>"
   }

Environment variables (set locally or in GitHub Actions):
- AWS_REGION        (e.g., "us-east-1")
- S3_BUCKET         (e.g., "my-rekognition-input-bucket-jns")
- DYNAMODB_TABLE    (e.g., "beta_results" or "prod_results")
- STAGE             (e.g., "beta" or "prod"; default "beta")
- BRANCH_NAME       (optional; falls back to GHA vars or "unknown-branch")

IAM needed:
- s3:PutObject, s3:GetObject, s3:ListBucket on your bucket
- rekognition:DetectLabels
- dynamodb:PutItem on your results table
"""

import os
import sys
import json
import mimetypes
import pathlib
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

# ---------------- Config from env ----------------
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET")  # required
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")  # required
STAGE = os.getenv("STAGE", "beta").strip() or "beta"

# Try to infer a branch name sensibly (works in GitHub Actions too)
BRANCH_NAME = (
    os.getenv("BRANCH_NAME")
    or os.getenv("GITHUB_HEAD_REF")
    or os.getenv("GITHUB_REF_NAME")
    or "unknown-branch"
)

IMAGES_DIR = pathlib.Path("images")
VALID_EXTS = {".jpg", ".jpeg", ".png"}

# ---------------- Guardrails ----------------
if not S3_BUCKET:
    print("[ERROR] S3_BUCKET env var is required.", file=sys.stderr)
    sys.exit(1)

if not DYNAMODB_TABLE:
    print("[ERROR] DYNAMODB_TABLE env var is required.", file=sys.stderr)
    sys.exit(1)

# ---------------- AWS clients ----------------
session = boto3.Session(region_name=AWS_REGION)
s3 = session.client("s3")
rekog = session.client("rekognition")
dynamodb = session.resource("dynamodb", region_name=AWS_REGION)
ddb_table = dynamodb.Table(DYNAMODB_TABLE)

# ---------------- Helpers ----------------
def iso_utc_now() -> str:
    # produce strict Z-suffixed ISO8601 for your example
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def s3_key(filename: str) -> str:
    # rekognition-input/<stage>/<filename>
    return f"rekognition-input/{STAGE}/{filename}"

def put_file_to_s3(local: pathlib.Path, key: str):
    ctype, _ = mimetypes.guess_type(local.name)
    extra = {"ContentType": ctype} if ctype else {}
    s3.upload_file(str(local), S3_BUCKET, key, ExtraArgs=extra)

def detect_labels_for_key(key: str):
    resp = rekog.detect_labels(
        Image={"S3Object": {"Bucket": S3_BUCKET, "Name": key}},
        MaxLabels=20,
        MinConfidence=70.0,
    )
    labels = resp.get("Labels", [])
    # normalize conf to 2 decimals
    return [{"Name": l["Name"], "Confidence": round(float(l["Confidence"]), 2)} for l in labels]

def write_ddb_item(item: dict):
    ddb_table.put_item(Item=item)

def analyze_one_image(path: pathlib.Path):
    fname = path.name
    key = s3_key(fname)

    print(f"\n=== {fname} ===")
    print(f"Upload → s3://{S3_BUCKET}/{key}")
    put_file_to_s3(path, key)

    print("Rekognition → detect_labels …")
    labels = detect_labels_for_key(key)

    result = {
        "filename": key,
        "labels": labels,
        "timestamp": iso_utc_now(),
        "branch": BRANCH_NAME,
    }

    print(f"DynamoDB → {DYNAMODB_TABLE}")
    write_ddb_item(result)

    # Human-friendly preview
    print("Top labels:")
    for l in labels[:10]:
        print(f"  - {l['Name']}: {l['Confidence']}%")

def main():
    if not IMAGES_DIR.exists():
        print("[ERROR] ./images folder not found. Create it and add .jpg/.png files.", file=sys.stderr)
        sys.exit(1)

    files = [p for p in IMAGES_DIR.iterdir() if p.suffix.lower() in VALID_EXTS and p.is_file()]
    if not files:
        print("[ERROR] No .jpg/.jpeg/.png files found in ./images", file=sys.stderr)
        sys.exit(1)

    print(f"Region={AWS_REGION} | Bucket={S3_BUCKET} | Stage={STAGE} | Branch={BRANCH_NAME}")
    print(f"DynamoDB Table={DYNAMODB_TABLE}")

    try:
        for img in files:
            analyze_one_image(img)
    except ClientError as e:
        print(f"[AWS ERROR] {e}", file=sys.stderr)
        sys.exit(2)

    print("\nAll done ")

if __name__ == "__main__":
    main()