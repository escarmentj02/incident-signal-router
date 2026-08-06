# Incident Signal Router

A dependency-free Python command-line tool that groups raw operational alerts into incidents, assigns a severity, and recommends an owner and first response.

## Why it exists

Alert volume is rarely actionable by itself. This small service translates a JSON stream of alerts into a compact incident queue using deterministic, auditable rules.

## Run

```powershell
python router.py --input examples/alerts.json
python -m unittest discover -s tests
```

## Design

- Groups alerts by `service` and a 15-minute time bucket.
- Scores severity from alert priority and customer impact.
- Emits an escalation recommendation and stable incident ID.
- Uses only the Python standard library so it can run in restricted environments.

## Example output

```json
{"incident_id":"payments-20260806T1200","severity":"SEV-1","owner":"payments-oncall","recommended_action":"Page primary on-call and open incident channel"}
```
