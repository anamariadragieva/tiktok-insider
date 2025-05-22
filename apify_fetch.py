import requests
import time

APIFY_API_TOKEN = "apify_api_pa78v1CI9Ar6L549BDXDpF4eCI4wGu1pzIrO"
ACTOR_ID = "OtzYfK1ndEGdwWFKQ"

def run_actor(searchQueries):

    url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={APIFY_API_TOKEN}"
    
    input_json = {
        "searchQueries": searchQueries,
        "resultsLimit": 5
    }
    response = requests.post(url, json=input_json)
    response.raise_for_status()
    run_data = response.json()
    run_id = run_data["data"]["id"]
    print(f"Started run: {run_id}")

    # Poll for completion
    while True:
        status_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs/{run_id}"
        status_response = requests.get(status_url, params={"token": APIFY_API_TOKEN})
        status_response.raise_for_status()
        status_data = status_response.json()["data"]
        if status_data["status"] == "SUCCEEDED":
            break
        elif status_data["status"] in ["FAILED", "ABORTED"]:
            raise Exception(f"Actor failed with status: {status_data['status']}")
        time.sleep(5)

    # Get dataset items
    dataset_id = status_data["defaultDatasetId"]
    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
    result_response = requests.get(items_url, params={"token": APIFY_API_TOKEN, "format": "json"})
    result_response.raise_for_status()
    return result_response.json()