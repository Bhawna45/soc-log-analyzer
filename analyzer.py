import re
import ipaddress
from collections import defaultdict

FAILED_RE = re.compile(
    r"Failed password for (?:invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)"
)
ACCEPTED_RE = re.compile(
    r"Accepted password for (\S+) from (\d+\.\d+\.\d+\.\d+)"
)


def is_private(ip):
    return ipaddress.ip_address(ip).is_private


def analyze_ssh_log(text, brute_threshold=5, suspicious_threshold=3):
    failed_count = defaultdict(int)
    users_tried = defaultdict(set)
    alerts = []
    total_failed = 0
    total_success = 0

    for line in text.splitlines():
        failed = FAILED_RE.search(line)
        if failed:
            user, ip = failed.group(1), failed.group(2)
            failed_count[ip] += 1
            users_tried[ip].add(user)
            total_failed += 1
            continue

        accepted = ACCEPTED_RE.search(line)
        if accepted:
            user, ip = accepted.group(1), accepted.group(2)
            total_success += 1
            # Fail ke baad success = possible compromised login
            if failed_count[ip] > 0 and not is_private(ip):
                alerts.append({
                    "severity": "CRITICAL",
                    "type": "Possible compromised login",
                    "ip": ip,
                    "detail": f"User '{user}' logged in after {failed_count[ip]} failed attempt(s)",
                })

    for ip, count in failed_count.items():
        if count >= brute_threshold:
            severity, kind = "HIGH", "Brute force attack"
        elif count >= suspicious_threshold:
            severity, kind = "MEDIUM", "Suspicious repeated failures"
        else:
            continue
        alerts.append({
            "severity": severity,
            "type": kind,
            "ip": ip,
            "detail": f"{count} failed logins, usernames tried: {', '.join(sorted(users_tried[ip]))}",
        })

    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}
    alerts.sort(key=lambda a: order[a["severity"]])

    top_ips = sorted(failed_count.items(), key=lambda x: x[1], reverse=True)

    return {
        "total_failed": total_failed,
        "total_success": total_success,
        "unique_attackers": len(failed_count),
        "top_ips": top_ips,
        "alerts": alerts,
    }


if __name__ == "__main__":
    with open("sample_logs/auth.log") as f:
        result = analyze_ssh_log(f.read())

    print("Failed:", result["total_failed"])
    print("Success:", result["total_success"])
    print("IPs with failures:", result["unique_attackers"])
    print()
    for a in result["alerts"]:
        print(f"[{a['severity']}] {a['type']} | {a['ip']} | {a['detail']}")