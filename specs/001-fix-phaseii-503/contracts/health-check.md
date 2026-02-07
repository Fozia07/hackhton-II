# API Contract: GET /health

**Endpoint**: `GET /health`
**Purpose**: Check the health status of the application and its dependencies
**Authentication**: Not required
**Implementation**: `phaseII/backend/app/main.py:62-86`

---

## Request

### Headers

No special headers required.

### Query Parameters

None

### Example Request

```bash
curl -X GET http://localhost:8001/health
```

---

## Response

### Current Implementation

#### Success Response (200 OK)

**Status Code**: `200 OK`

**Body Schema**:

```json
{
  "status": "ok",
  "database": "connected",
  "timestamp": "2026-02-07T12:00:00.123456Z"
}
```

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | Overall application status ("ok" or "error") |
| `database` | String | Database connection status ("connected", "disconnected", "not configured") |
| `timestamp` | String (ISO 8601) | Current server timestamp (UTC) |

#### Error Response (200 OK with error status)

**Status Code**: `200 OK` (Note: Should be 503 for unhealthy state)

**Body Schema**:

```json
{
  "status": "error",
  "error": "Database connection failed",
  "timestamp": "2026-02-07T12:00:00.123456Z"
}
```

**Issues with Current Implementation**:
1. Returns 200 OK even when unhealthy (should return 503)
2. Doesn't actually test database connectivity (just checks if engine exists)
3. Limited information for monitoring and debugging

---

## Enhanced Implementation (Proposed)

### Success Response (200 OK)

**Status Code**: `200 OK`

**Body Schema**:

```json
{
  "status": "ok",
  "timestamp": "2026-02-07T12:00:00.123456Z",
  "version": "0.1.0",
  "database": {
    "status": "connected",
    "latency_ms": 15
  },
  "endpoints": {
    "auth": "available",
    "todos": "available"
  }
}
```

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | Overall status ("ok", "degraded", "error") |
| `timestamp` | String (ISO 8601) | Current server timestamp (UTC) |
| `version` | String | Application version from settings |
| `database.status` | String | Database connection status ("connected", "disconnected") |
| `database.latency_ms` | Integer | Database query latency in milliseconds |
| `endpoints.auth` | String | Auth endpoints availability ("available", "unavailable") |
| `endpoints.todos` | String | Todo endpoints availability ("available", "unavailable") |

### Example Success Response

```json
{
  "status": "ok",
  "timestamp": "2026-02-07T12:00:00.123456Z",
  "version": "0.1.0",
  "database": {
    "status": "connected",
    "latency_ms": 15
  },
  "endpoints": {
    "auth": "available",
    "todos": "available"
  }
}
```

---

### Degraded Response (200 OK)

**Status Code**: `200 OK`

**Body Schema**:

```json
{
  "status": "degraded",
  "timestamp": "2026-02-07T12:00:00.123456Z",
  "version": "0.1.0",
  "database": {
    "status": "connected",
    "latency_ms": 250
  },
  "endpoints": {
    "auth": "available",
    "todos": "available"
  }
}
```

**Degraded Conditions**:
- Database latency between 100-500ms
- All services operational but performance degraded

---

### Error Response (503 Service Unavailable)

**Status Code**: `503 Service Unavailable`

**Body Schema**:

```json
{
  "status": "error",
  "timestamp": "2026-02-07T12:00:00.123456Z",
  "version": "0.1.0",
  "database": {
    "status": "disconnected",
    "error": "Connection timeout"
  },
  "endpoints": {
    "auth": "unavailable",
    "todos": "unavailable"
  }
}
```

**Error Conditions**:
- Database connection failed
- Database latency > 500ms
- Critical service unavailable

---

## Status Determination Logic

### Status Levels

| Status | Conditions | HTTP Code |
|--------|-----------|-----------|
| `ok` | All services operational, DB latency < 100ms | 200 |
| `degraded` | All services operational, DB latency 100-500ms | 200 |
| `error` | Database disconnected OR DB latency > 500ms | 503 |

### Health Check Algorithm

```python
async def health_check():
    try:
        # Test database connectivity
        start_time = time.time()
        async with AsyncSession(engine) as session:
            await session.execute(select(1))
        latency_ms = int((time.time() - start_time) * 1000)

        # Determine status
        if latency_ms < 100:
            status = "ok"
        elif latency_ms < 500:
            status = "degraded"
        else:
            status = "error"

        return {
            "status": status,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": settings.app_version,
            "database": {
                "status": "connected",
                "latency_ms": latency_ms
            },
            "endpoints": {
                "auth": "available",
                "todos": "available"
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": settings.app_version,
            "database": {
                "status": "disconnected",
                "error": str(e)
            },
            "endpoints": {
                "auth": "unavailable",
                "todos": "unavailable"
            }
        }, 503
```

---

## Use Cases

### 1. Load Balancer Health Check

**Purpose**: Load balancer checks if backend instance is healthy

**Configuration**:
- Endpoint: `GET /health`
- Interval: Every 10 seconds
- Timeout: 5 seconds
- Healthy threshold: 2 consecutive successes
- Unhealthy threshold: 3 consecutive failures

**Expected Behavior**:
- 200 OK → Instance is healthy, route traffic
- 503 Service Unavailable → Instance is unhealthy, stop routing traffic

---

### 2. Monitoring System

**Purpose**: Monitoring system tracks application health over time

**Metrics to Track**:
- Health check response time
- Database latency
- Status transitions (ok → degraded → error)
- Error frequency

**Alerting Rules**:
- Alert if status = "error" for > 5 minutes
- Alert if status = "degraded" for > 30 minutes
- Alert if database latency > 200ms for > 10 minutes

---

### 3. Deployment Verification

**Purpose**: Verify application is healthy after deployment

**Process**:
1. Deploy new version
2. Wait for application startup (10 seconds)
3. Call health check endpoint
4. Verify status = "ok" and database.status = "connected"
5. If unhealthy, rollback deployment

---

### 4. Developer Debugging

**Purpose**: Quickly check if local development environment is working

**Usage**:
```bash
# Check if backend is running and healthy
curl http://localhost:8001/health | jq

# Expected output:
# {
#   "status": "ok",
#   "timestamp": "2026-02-07T12:00:00Z",
#   "version": "0.1.0",
#   "database": {
#     "status": "connected",
#     "latency_ms": 15
#   },
#   "endpoints": {
#     "auth": "available",
#     "todos": "available"
#   }
# }
```

---

## Testing

### Test Cases

1. **Healthy System**: All services operational
   - Expected: 200 OK with status = "ok"

2. **Database Disconnected**: Database unavailable
   - Expected: 503 Service Unavailable with status = "error"

3. **Slow Database**: Database latency > 100ms
   - Expected: 200 OK with status = "degraded"

4. **Very Slow Database**: Database latency > 500ms
   - Expected: 503 Service Unavailable with status = "error"

### Example Test Script

```bash
#!/bin/bash

# Test 1: Healthy system
echo "Test 1: Healthy system"
curl -s http://localhost:8001/health | jq

# Test 2: Check response time
echo "\nTest 2: Check response time"
time curl -s http://localhost:8001/health > /dev/null

# Test 3: Continuous monitoring
echo "\nTest 3: Continuous monitoring (10 checks)"
for i in {1..10}; do
  STATUS=$(curl -s http://localhost:8001/health | jq -r '.status')
  LATENCY=$(curl -s http://localhost:8001/health | jq -r '.database.latency_ms')
  echo "Check $i: Status=$STATUS, DB Latency=${LATENCY}ms"
  sleep 5
done
```

---

## Performance

**Expected Response Time**: < 500ms

**Factors Affecting Performance**:
- Database query execution time
- Network latency to database
- Server load

**Optimization**:
- Use simple SELECT 1 query for database check
- Cache health status for 5 seconds (optional)
- Timeout database query after 1 second

---

## CORS Configuration

**Required Headers**:
- `Access-Control-Allow-Origin`: `*` (health check should be publicly accessible)
- `Access-Control-Allow-Methods`: `GET, OPTIONS`

**Note**: Health check endpoint doesn't require authentication, so CORS can be more permissive.

---

## Security Considerations

1. **Information Disclosure**:
   - Health check exposes application version
   - Consider limiting information in production
   - Don't expose sensitive configuration details

2. **DDoS Protection**:
   - Health check endpoint can be abused for DDoS
   - Consider rate limiting (e.g., 60 requests per minute per IP)
   - Use CDN or load balancer for protection

3. **Authentication**:
   - Health check should NOT require authentication
   - Load balancers and monitoring systems need unauthenticated access

---

## Comparison: Current vs Enhanced

| Feature | Current | Enhanced |
|---------|---------|----------|
| Database connectivity test | ❌ No (just checks if engine exists) | ✅ Yes (actual query) |
| Database latency | ❌ No | ✅ Yes |
| Proper HTTP status codes | ❌ No (always 200) | ✅ Yes (200/503) |
| Version information | ❌ No | ✅ Yes |
| Endpoint availability | ❌ No | ✅ Yes |
| Degraded state detection | ❌ No | ✅ Yes |
| Monitoring-friendly | ⚠️ Limited | ✅ Yes |

---

## Implementation Priority

**Phase 1** (Critical):
- Add actual database connectivity test
- Return 503 for unhealthy state
- Measure database latency

**Phase 2** (Important):
- Add version information
- Add endpoint availability status
- Implement degraded state detection

**Phase 3** (Nice to have):
- Add caching for health status
- Add detailed error messages
- Add metrics for monitoring

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-07 | 1.0 | Initial API contract documentation |
| 2026-02-07 | 2.0 | Proposed enhanced implementation |

---

**Contract Status**:
- Current Implementation: ✅ Implemented (basic)
- Enhanced Implementation: 📋 Proposed (not yet implemented)
