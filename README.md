# Currency Rate Logger — Azure Function App

A serverless Python application that automatically fetches USD exchange rates every hour from a public API and stores them as timestamped JSON files in Azure Blob Storage.

## Tech Stack

- **Compute:** Azure Functions (Consumption plan, Python 3.11)
- **Storage:** Azure Blob Storage
- **Monitoring:** Application Insights
- **Trigger:** Timer (CRON: `0 0 * * * *` — top of every hour)
- **External API:** open.er-api.com (free, no key required)

## What It Does

1. The timer trigger fires at the top of every hour.
2. The function calls the public exchange rates API for USD.
3. The response is wrapped into a clean JSON payload with a UTC timestamp.
4. The payload is written to Blob Storage as `rates-YYYY-MM-DD-HHMM.json`.
5. All steps are logged to Application Insights for observability.

## Sample Output

```json
{
  "fetched_at_utc": "2026-05-27T14:00:01.234567+00:00",
  "base_currency": "USD",
  "rates": {
    "EUR": 0.92,
    "GBP": 0.79,
    "INR": 83.12,
    "JPY": 156.45
  },
  "source": "https://open.er-api.com/v6/latest/USD"
}
```
## Local Development

```bash
# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally (requires Azure Functions Core Tools + Azurite)
func start
```

## Deployment

Deployed to Azure resource group `sahana-learn` (region: centralus) via VS Code Azure Functions extension.



