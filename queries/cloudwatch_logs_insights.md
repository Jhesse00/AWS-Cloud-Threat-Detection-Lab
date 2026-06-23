# CloudWatch Logs Insights Queries

## Recent SSH authentication activity

```sql
fields @timestamp, @message
| filter @message like /sshd/
| filter @message like /Connection closed|Disconnected|Invalid user|Failed password|kex_exchange/
| sort @timestamp desc
| limit 200
```

## Top source IPs

```sql
fields @timestamp, @message
| filter @message like /sshd/
| parse @message "* from * port *" as prefix, src_ip, src_port
| filter ispresent(src_ip)
| stats count(*) as attempts by src_ip
| sort attempts desc
| limit 20
```

## Attempted usernames by source IP

```sql
fields @timestamp, @message
| filter @message like /Invalid user/
| parse @message "Invalid user * from * port *" as username, src_ip, src_port
| filter ispresent(username)
| filter ispresent(src_ip)
| stats count(*) as attempts by src_ip, username
| sort attempts desc
| limit 100
```

## SSH activity over time

```sql
fields @timestamp, @message
| filter @message like /sshd/
| filter @message like /Connection closed|Disconnected|Invalid user|Failed password|kex_exchange/
| stats count(*) as attempts by bin(30m)
| sort bin(30m) asc
```
