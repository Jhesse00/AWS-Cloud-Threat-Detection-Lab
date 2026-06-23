# Linux Log Collection Commands

## Watch SSH logs live

```bash
sudo journalctl -u sshd -f
```

## Extract source IP counts

```bash
echo "src_ip,attempts" > attacker_ips.csv

sudo journalctl -u sshd --since "24 hours ago" \
| grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' \
| grep -vE '^(0\.0\.0\.0|127\.0\.0\.1|10\.|172\.16\.|192\.168\.)' \
| sort \
| uniq -c \
| sort -nr \
| awk '{{print $2","$1}}' >> attacker_ips.csv
```

## Extract source IP and attempted username pairs

```bash
echo "src_ip,username,attempts" > ssh_usernames_by_ip.csv

sudo journalctl -u sshd --since "24 hours ago" \
| sed -nE '
s/.*Invalid user ([^ ]+) from ([0-9.]+) port.*/\2,\1/p
s/.*Failed password for invalid user ([^ ]+) from ([0-9.]+) port.*/\2,\1/p
s/.*Failed password for ([^ ]+) from ([0-9.]+) port.*/\2,\1/p
' \
| sort \
| uniq -c \
| sort -nr \
| awk '{{print $2","$1}}' >> ssh_usernames_by_ip.csv
```
