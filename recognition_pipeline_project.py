
import os, sys, json, boto3
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

def decimalize(x):
    if isinstance(x, list): return [decimalize(i) for i in x]
    if isinstance(x, dict): return {k: decimalize(v) for k, v in x.items()}
    if isinstance(x, float): return Decimal(str(x))
    return x

def main():
    if len(sys.argv) < 2:
        print("Usage: python recognition_pipeline_project.py <path-to-image>")
        sys.exit(1)

    file_path = Path(sys.argv[1]).expanduser().resolve()
    if not file_path.exists():
        raise FileNotFoundError(file_path)

    aws_region = os.environ["AWS_REGION"]
    bucket_name     = os.environ["S3_BUCKET"]
    table_name = os.environ["DYNAMODB_TABLE"]
    branch     = os.environ.get("BRANCH_NAME", "unknown")

    s3  = boto3.client("s3", region_name=aws_region)
    rek = boto3.client("rekognition", region_name=aws_region)
    ddb = boto3.resource("dynamodb", region_name=aws_region).Table(table_name)

    key = f"rekognition-input/{file_path.name}"
    s3.upload_file(str(file_path), bucket_name, key)

    resp = rek.detect_labels(
        Image={"S3Object": {"Bucket": bucket_name, "Name": key}},
        MaxLabels=25,
        MinConfidence=70.0
    )
    labels = [{"Name": L["Name"], "Confidence": L["Confidence"]} for L in resp.get("Labels", [])]

    item = {
        "filename": key,
        "labels": labels,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "branch": branch,
    }
    ddb.put_item(Item=decimalize(item))
    print(json.dumps(item, indent=2, default=str))

if __name__ == "__main__":
    main()
