import logging
import json
import os
from datetime import datetime, timezone
import azure.functions as func
import requests
from azure.storage.blob import BlobServiceClient


def main(mytimer: func.TimerRequest) -> None:
    utc_now = datetime.now(timezone.utc)
    logging.info(f"CurrencyRateLogger started at {utc_now.isoformat()}")

    # --- 1. Fetch exchange rates from public API ---
    api_url = "https://open.er-api.com/v6/latest/USD"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        rates_data = response.json()
        logging.info(f"Fetched rates for {len(rates_data.get('rates', {}))} currencies.")
    except Exception as e:
        logging.error(f"Failed to fetch exchange rates: {e}")
        raise

    # --- 2. Build a clean payload to store ---
    payload = {
        "fetched_at_utc": utc_now.isoformat(),
        "base_currency": rates_data.get("base_code", "USD"),
        "rates": rates_data.get("rates", {}),
        "source": api_url
    }

    # --- 3. Save to Azure Blob Storage ---
    connection_string = os.environ["AzureWebJobsStorage"]
    container_name = "currency-rates"
    blob_name = f"rates-{utc_now.strftime('%Y-%m-%d-%H%M')}.json"

    try:
        blob_service = BlobServiceClient.from_connection_string(connection_string)

        container_client = blob_service.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
            logging.info(f"Created container: {container_name}")

        blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(json.dumps(payload, indent=2), overwrite=True)
        logging.info(f"Saved blob: {container_name}/{blob_name}")

    except Exception as e:
        logging.error(f"Failed to save to Blob Storage: {e}")
        raise

    logging.info("CurrencyRateLogger completed successfully.")