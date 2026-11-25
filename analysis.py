from acquisition import comments_for_docket
import pandas as pd

# ADD DOCKETS HERE
docket_IDs = [
	# Revision to Regulations Regarding Oil and Gas Leasing; Stipulations and Information Notices
	"BLM-2025-0140",
	# Guidance on Eligible Investments for Trump Accounts
	"IRS-2026-1090"
]

docket_dfs = {docket_ID: comments_for_docket(docket_ID) for docket_ID in docket_IDs}

def merge_dockets(docket_dfs):
	if isinstance(docket_dfs, dict):
		dfs = [
			df.assign(docket_id=docket_id, docket_index=i) for i, (docket_id, df) in enumerate(docket_dfs.items())
		]

	elif isinstance(docket_dfs, list):
		dfs = [
			df.assign(docket_index=i) for i, df in enumerate(docket_dfs)
		]

	else:
		raise TypeError(
			"Expected a list or dictionary of DataFrames."
		)

	return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

merged_df = merge_dockets(docket_dfs)

# Net Neutrality FCC Comments (24MM)
# https://huggingface.co/datasets/slnader/fcc-comments/resolve/main/fcc.tar.gz

# fcc_df = pd.read_csv("data/fcc_comments.csv")
# print(fcc_df.head())
#
# for col in fcc_df.columns:
# 	print(fcc_df[col].value_counts())
#
