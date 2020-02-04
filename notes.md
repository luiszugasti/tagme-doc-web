# Tests Notes

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

## Next steps
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

This has been completed.

## New Tests

I am trying to see whats a reasonable lower bound for processing each document in exponential time,
when comparing tags.

For the tagging process, 10 docs takes 7 seconds (So hovering the .5 secs per doc mark)

For the comparison process, I am still playing around with the threads.
at 40 threads, 10 docs (assumed 10 * 10 ops, 100 total ops!):

I also have to keep in mind, that I have not yet gotten tag values for ALL documents!

```
40 threads
Job to get edges completed in 69.7820000648 seconds
# of Operations: 90
```
yuck....


```
30 threads
Job to get edges completed in 78.1769998074 seconds
# of Operations: 90
```

relatively the same amount, I will try 10 threads. What's the max?

```
10 threads
Job to get edges completed in 146.937000036 seconds
# of Operations: 90
```

```
60 threads
Job to get edges completed in 71.0390000343 seconds
# of Operations: 90
```

Sweet spot is basically 40 threads, so I will keep 60 for now.
## Thought
If I want to allow for constant complexity for access, by reversing the node entries,
Then I don't need to waste time waiting for the TAGME API.
I can allow for a tag on each document that sets it to be "found".
Therefore, It won't be iterated over.

Then, to allow for O(n) time, I go through all the edges and reverse them, and assign
them to the opposite node.

This will hopefully halve the execution time of the process - and run the re-org process separately
or in the same place as I wish
However, this can still lead to issues as the threads themselves are operating on non-
thread safe space. Thus, even if I make this enhancement, I really don't know _how_ to ensure
that this optimization does not incur double edges!
