"""Turn a stream of monitoring alerts into actionable incident summaries."""
import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone

PRIORITY_POINTS = {"critical": 5, "high": 3, "medium": 1, "low": 0}


def parse_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def bucket_start(moment):
    minute = moment.minute - (moment.minute % 15)
    return moment.replace(minute=minute, second=0, microsecond=0)


def classify(score):
    if score >= 8:
        return "SEV-1", "Page primary on-call and open incident channel"
    if score >= 4:
        return "SEV-2", "Notify on-call and start investigation"
    return "SEV-3", "Create a ticket and review during business hours"


def summarize(alerts):
    groups = defaultdict(list)
    for alert in alerts:
        moment = parse_time(alert["timestamp"])
        groups[(alert["service"], bucket_start(moment))].append(alert)

    incidents = []
    for (service, start), grouped in sorted(groups.items()):
        score = sum(PRIORITY_POINTS.get(a.get("priority", "low"), 0) for a in grouped)
        score += 3 if any(a.get("customer_impact") for a in grouped) else 0
        severity, action = classify(score)
        incidents.append({
            "incident_id": f"{service}-{start.strftime('%Y%m%dT%H%M')}",
            "service": service,
            "window_start": start.isoformat().replace("+00:00", "Z"),
            "alert_count": len(grouped),
            "severity": severity,
            "owner": f"{service}-oncall",
            "recommended_action": action,
        })
    return incidents


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    with open(args.input, encoding="utf-8") as source:
        print(json.dumps(summarize(json.load(source)), indent=2))
