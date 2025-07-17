# 🛡️ Django IP Tracking & Security Middleware

This Django app enhances security by tracking incoming IP addresses, logging request metadata, applying rate limits, blocking blacklisted IPs, enriching logs with geolocation, and detecting suspicious activity using background tasks.

---

## 📦 Features

### ✅ Task 0: Basic IP Logging Middleware
- Logs every incoming request's:
  - IP Address
  - Timestamp
  - Request Path
- Stored in the `RequestLog` model.

### ✅ Task 1: IP Blacklisting
- Requests from blacklisted IPs are blocked with `403 Forbidden`.
- Add IPs to the `BlockedIP` model.
- CLI command to block IPs:
  ```bash
  python manage.py block_ip <ip_address>

## ✅ Task 2: IP Geolocation Analytics

- Uses IP geolocation via [`ip2geotools`](https://pypi.org/project/ip2geotools/) to enrich request logs with:
  - 🌍 **Country**
  - 🏙️ **City**
- Geolocation results are **cached for 24 hours** to minimize API usage and improve performance.

---

## ✅ Task 3: Rate Limiting by IP

- Protects sensitive views (e.g., login) using `django-ratelimit`.
- Rate limit configuration:
  - 🔐 **Authenticated users**: `10 requests per minute`
  - 👤 **Anonymous users**: `5 requests per minute`
- Exceeding the limit returns a **429 Too Many Requests** response to the client.

---

## ✅ Task 4: Anomaly Detection

- An **hourly Celery task** scans `RequestLog` entries to flag suspicious activity:
  - ⚠️ IPs with **more than 100 requests/hour**
  - 🔒 IPs accessing **sensitive paths** such as `/admin` or `/login`
- Flagged IPs are saved in the `SuspiciousIP` model with a description of the reason.

## 📁 Project Structure

ip_tracking/
├── middleware.py        # Middleware for IP logging and blocking
├── models.py            # RequestLog, BlockedIP, SuspiciousIP
├── tasks.py             # Celery task for anomaly detection
├── views.py             # Rate-limited views (e.g., login)
├── management/
│   └── commands/
│       └── block_ip.py  # CLI command to block IPs