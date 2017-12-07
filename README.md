Given a list of <String name, Int score> pairs (‘data.csv’), return the top 10 names (ranked by score).

The CSV file is parsed to produce an index structure D.

A Query Server reads D and then accepts user queries (localhost:5000/s) such that for each query s, it responds with the top 10 names (ranked by score) that start with s or
contains ‘_s’ (so for example, both “service_arn” and “doc_service” match the prefix “ser”). Query answering runs in log time.
