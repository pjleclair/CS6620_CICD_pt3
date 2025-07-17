import boto3
import json
import uuid
from botocore.exceptions import ClientError
import os
from typing import Any

LOCALSTACK_ENDPOINT = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
TABLE_NAME = "items"
BUCKET_NAME = "items-bucket"

dynamodb: Any = boto3.resource(
    "dynamodb",
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

s3 = boto3.client(
    "s3",
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)


async def initialize_services():
    """Initialize DynamoDB table and S3 bucket"""
    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        table.wait_until_exists()
    except ClientError as e:
        if e.response["Error"]["Code"] != "ResourceInUseException":
            raise

    try:
        s3.create_bucket(Bucket=BUCKET_NAME)
    except ClientError as e:
        if e.response["Error"]["Code"] != "BucketAlreadyExists":
            raise


async def get_all():
    """Get all items from DynamoDB"""
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    return response.get("Items", [])


async def get(item_id: str):
    """Get single item from DynamoDB"""
    table = dynamodb.Table(TABLE_NAME)
    response = table.get_item(Key={"id": item_id})
    if "Item" not in response:
        raise ValueError("Item not found")
    return response["Item"]


async def post(item_data: dict):
    """Create new item in DynamoDB and S3"""
    if "id" not in item_data:
        item_data["id"] = str(uuid.uuid4())

    item_id = item_data["id"]
    table = dynamodb.Table(TABLE_NAME)

    try:
        existing = table.get_item(Key={"id": item_id})
        if "Item" in existing:
            raise ValueError("Item already exists")
    except ClientError:
        pass

    table.put_item(Item=item_data)

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f"{item_id}.json",
        Body=json.dumps(item_data),
        ContentType="application/json",
    )

    return item_data


async def put(item_id: str, item_data: dict):
    """Update existing item in DynamoDB and S3"""
    if not item_data:
        raise ValueError("Item data cannot be empty")

    table = dynamodb.Table(TABLE_NAME)

    try:
        existing = table.get_item(Key={"id": item_id})
        if "Item" not in existing:
            raise ValueError("Item not found")
    except ClientError:
        raise ValueError("Item not found")

    item_data["id"] = item_id

    table.put_item(Item=item_data)

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f"{item_id}.json",
        Body=json.dumps(item_data),
        ContentType="application/json",
    )

    return item_data


async def delete(item_id: str):
    """Delete item from DynamoDB and S3"""
    table = dynamodb.Table(TABLE_NAME)

    try:
        existing = table.get_item(Key={"id": item_id})
        if "Item" not in existing:
            raise ValueError("Item not found")
    except ClientError:
        raise ValueError("Item not found")

    table.delete_item(Key={"id": item_id})

    s3.delete_object(Bucket=BUCKET_NAME, Key=f"{item_id}.json")

    return {"message": f"Item {item_id} deleted successfully"}
