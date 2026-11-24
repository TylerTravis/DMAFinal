from acquisition import comments_for_docket

dockets = [
	# Revision to Regulations Regarding Oil and Gas Leasing; Stipulations and Information Notices
	"BLM-2025-0140",
	# Guidance on Eligible Investments for Trump Accounts
	"IRS-2026-1090"
]

dfs = {}

for docket in dockets:
	dfs[docket] = comments_for_docket(docket)

# Net Neutrality FCC Comments (24MM)
# https://huggingface.co/datasets/slnader/fcc-comments/resolve/main/fcc.tar.gz



