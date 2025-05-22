import boto3
import sagemaker
from sagemaker.session import Session
from sagemaker import get_execution_role
from sagemaker.inputs import TrainingInput
from sagemaker.estimator import Estimator
boto_session = boto3.Session(region_name="us-east-1")
sagemaker_session = Session(boto_session=boto_session)
# ---- SETUP ---- #
s3_bucket = "giovanna-ml-models-bucket"
s3_prefix = "cicids2017"
s3_uri = f"s3://{s3_bucket}/{s3_prefix}"

# NOTE: Replace this with your actual SageMaker execution role ARN (from Terraform)
role = "arn:aws:iam::713881788173:role/sagemaker-execution-role"

# ---- DATASET ---- #
# CICIDS2017 pre-hosted by AWS Labs: https://registry.opendata.aws/cicids2017/
# For demo, we point to a simplified version of the dataset in CSV format
# You could download and preprocess locally, then upload to your own bucket if needed
input_data = "s3://giovanna-ml-models-bucket/cicids2017/binary_cleaned_ddos.csv"

# ---- ESTIMATOR SETUP ---- #
xgboost_container = sagemaker.image_uris.retrieve("xgboost", boto_session.region_name, "1.5-1")

xgb = Estimator(
    image_uri=xgboost_container,
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=s3_uri,
    sagemaker_session=sagemaker_session
)

xgb.set_hyperparameters(
    max_depth=5,
    eta=0.2,
    gamma=4,
    min_child_weight=6,
    subsample=0.8,
    objective="binary:logistic",
    num_round=100
)

# ---- INPUT ---- #
train_input = TrainingInput(
    input_data,
    content_type="csv"
)

# ---- TRAIN ---- #
xgb.fit({"train": train_input})

print("Training complete. Model saved to:", s3_uri)

