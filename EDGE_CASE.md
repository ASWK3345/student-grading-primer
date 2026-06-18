# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified

> `GET /stats` may be called when there are no students in this database

2) How you have accounted for this in your implementation

> The API returns:

```json
jsonify({
    "count": 0,
    "average": None,
    "min": None,
    "max": None
}), 200
```

3) Reasons:

When there are no student marks, average, minimum and maximum cannot be calculated properly. Thus, we return a `null` instead of a `0`, because 0 can be misunderstood as a calculated result.