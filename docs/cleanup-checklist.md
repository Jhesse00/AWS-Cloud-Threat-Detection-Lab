# Cleanup Checklist

After completing the lab, remove or lock down all exposed resources.

- Remove `0.0.0.0/0` from inbound SSH/22.
- Stop or terminate the EC2 instance.
- Release unused Elastic IPs.
- Delete unused EBS volumes.
- Delete CloudWatch log groups if no longer needed.
- Disable lab-only GuardDuty, EventBridge, SNS, VPC Flow Logs, or CloudTrail resources.
- Verify AWS Billing and Cost Explorer.
- Keep only sanitized screenshots, charts, and exported CSVs in the public repository.
