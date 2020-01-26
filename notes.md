# 135 document test times for just querying TAGME API

32 threads: 76 seconds
* Diminishing returns here....*

40 threads: 54 seconds
48 threads: 53 seconds
64 threads: 55 seconds
96 threads: 57 seconds

Choose 40 threads as that appears the safest. Other optimization could be removing the script tags and its contents from the code.
Test corpus -> 297.259000063 seconds (average .5 secs per document, fairly fast)
250,000 docs * .5 secs/doc -> 125,000 seconds (aka 35 hours to finish the whole querying job)

This is due to the TAGME API itself.

# Next steps
Finish the document comparison task, and code it in a way that the process runs while we wait for the TAGME service to respond.

Idea: 1 core for TAGME.
1 core for taking the:
[
	{
		"clueweb09-en0000-00-00175": {
			"Canada": 4,
			"Geoscience Australia": 2,
            ...
			"History of cartography": 1,
		}
	},
    {
		"clueweb09-en0000-00-00175": {
			"Canada": 4,
			"Geoscience Australia": 2,
            ...
			"History of cartography": 1,
		}
	}
    ....
]

List of Dictionary of Dictionary -> Need to make it a DICTIONARY OF DICTIONARY