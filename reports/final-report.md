# AWS Cloud Threat Detection Lab: Final Report

## Executive Summary

This project built an AWS cloud threat detection lab using an isolated Linux EC2 instance as a controlled SSH honeypot. SSH on port 22 was deliberately exposed to the public internet to observe real-world automated scanning and failed login activity.

System telemetry was forwarded into CloudWatch, exported, parsed, enriched, and visualized to simulate a SOC-style investigation workflow.

## Key Results

| Metric | Result |
|---|---:|
| Total failed SSH login events | 1,278 |
| Unique attacker/source IPs | 44 |
| Top IP | 77.104.92.143 |
| Top IP failed login events | 786 |
| Username attempts analyzed | 541 |
| Unique usernames guessed | 58 |
| Top IP/username pair | 77.104.92.143 → ubuntu (87 attempts) |

## Main Visualization

![Global SSH Attack Map](../visualizations/global-ssh-attack-map.png)

The attack map shows failed SSH login activity against the AWS EC2 honeypot. Source locations are based on IP geolocation and represent infrastructure location, not confirmed physical actor attribution.

## Methodology

1. Deployed an isolated Linux EC2 instance in AWS.
2. Temporarily exposed SSH on port 22 through a Security Group.
3. Collected SSH authentication telemetry using Linux logs and CloudWatch.
4. Parsed failed SSH login activity into source IP and username datasets.
5. Enriched source IPs with BulkIPLab/VirusTotal-style reputation data.
6. Built charts, IOC tables, and a global attack map.
7. Documented findings, queries, and cleanup guidance.

## Defensive Takeaways

- Cloud exposure is immediate once a public IP and open management port are available.
- Management ports such as SSH/22 should not be left open to the world.
- Security Groups should be restricted to trusted IP addresses.
- AWS Systems Manager Session Manager can reduce the need for exposed SSH.
- Logging and monitoring are required to detect and investigate this activity.
- IP geolocation is useful for context, but it should not be treated as confirmed actor attribution.

## Tools Used

AWS EC2, Security Groups, CloudWatch Logs, Linux, journalctl, Python, pandas, matplotlib, Kepler.gl, BulkIPLab, and VirusTotal.
