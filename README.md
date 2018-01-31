Given a list of <String name, Int score> pairs (‘data.csv’), returns the top 10 names containing a query substring ‘sub’. Input list contains ~100k pairs <name, score>.

Server accepts user queries at localhost:5000/s such that for each query s (string), it responds with the top 10 names (ranked by score) that start with ‘sub’ or contains ‘_sub’ (for example, both “service_arn” and “doc_service” match the prefix “ser”).
