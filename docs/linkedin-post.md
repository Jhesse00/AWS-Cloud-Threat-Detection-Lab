🚨 I built an AWS Cloud Threat Detection Lab, and a single IP geolocated to Iran attempted to brute-force my server 786 times.

To observe real-world cloud attacks, I deployed an isolated Linux EC2 instance in AWS, deliberately exposed SSH on port 22 to the public internet, and forwarded system telemetry into CloudWatch to analyze attack patterns and extract IOCs.

📊 Lab results:

• 1,278 total failed SSH login events from 44 unique attacker IPs  
• Top attacker IP: 77.104.92.143, geolocated to Iran, with 786 brute-force attempts alone  
• 58 unique usernames guessed, heavily targeting default cloud/Linux accounts like “ubuntu”  
• Identified scanning infrastructure overlapping with state-sponsored threat regions, including China, Iran, and Russia  

⚠️ Key takeaway:

Cloud exposure is instant, and the public internet is hostile. Management ports like SSH should not be left open to the world.

Audit your AWS Security Groups, lock down port 22, and consider secure access methods like AWS Systems Manager Session Manager before automated scanners and botnets find your infrastructure first.

This was a great hands-on way to practice cloud log analysis, threat intelligence enrichment, IOC extraction, and SOC-style investigation.

Full writeup + CloudWatch queries on GitHub 👇

https://github.com/Jhesse00/aws-threat-detection-lab

#CyberSecurity #AWS #CloudSecurity #SOC #BlueTeam #ThreatDetection #Linux #CloudWatch #InfoSec
