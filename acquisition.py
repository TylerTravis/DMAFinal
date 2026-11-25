import os
import pandas as pd
import requests
from dotenv import load_dotenv
import time
from pathlib import Path

# Console Display
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)

# Env Vars
load_dotenv()
api_key = os.getenv("API_KEY")
api_root = os.getenv("API_ROOT")

# Path to Data
data_path = Path(__file__).resolve().parent / "data"

def get(endpoint, params=None):
	# API rejects requests that are too frequent
	time.sleep(4)
	response = requests.get(
	f"{api_root}{endpoint}",
	headers={
		"X-Api-Key": api_key},
		params=params
	)
	# Check valid response status
	response.raise_for_status()
	return response.json()

def get_all(endpoint, filters):
	records = {}
	page = 1
	expected = None

	while True:
		result = get(endpoint, {
			**filters, "page[size]": 250, "page[number]": page,
			"sort": "lastModifiedDate,documentId",
		})

		batch = result["data"]
		total = result["meta"]["totalElements"]

		if expected is None:
			expected = total

		records.update({item["id"]: item for item in batch})

		if page * 250 >= total:
			return list(records.values())

		# API Documentation recommends timestamping for bulk downloads
		if page == 20:
			stamp = pd.Timestamp(batch[-1]["attributes"]["lastModifiedDate"])
			local = stamp.tz_convert("America/New_York")
			boundary = local.strftime("%Y-%m-%d %H:%M:%S")
			filters = {**filters, "filter[lastModifiedDate][ge]": boundary}
			page = 0
		page += 1

def comments_for_docket(docket_id, allow_duplicates=False):
	csv_path = data_path / f"{docket_id}.csv"

	# Checks for stored data and exits request if it already exists
	if csv_path.is_file():
		return pd.read_csv(csv_path, dtype=str, keep_default_na=False)

	comments = {}

	for document in get_all("documents", {"filter[docketId]": docket_id}):

		summaries = get_all("comments", {
			"filter[commentOnId]": document["attributes"]["objectId"],
		})

		for summary in summaries:
			comment_id = summary["id"]

			if comment_id in comments and not allow_duplicates:
				continue

			detail = get(f"comments/{comment_id}", {"include": "attachments"})

			comments[comment_id] = {
				**detail["data"],
				"attachments": detail.get("included", []),
				"source_document": document,
				"search_result": summary,
				"response_metadata": {
					key: value for key, value in detail.items()
					if key not in ("data", "included")
				},
			}

	df = pd.json_normalize(list(comments.values()))

	if df.empty:
		df = pd.DataFrame(columns=["id"])

	df.to_csv(csv_path, index=False)
	return df
