def generate_boolean_query(data):
    query_parts = []

    # Check each field in data and construct Boolean subqueries
    if data.get("symptoms"):
        query_parts.append(f'Symptoms:"{data["symptoms"]}"')

    if data.get("diagnosis"):
        query_parts.append(f'Diagnosis:"{data["diagnosis"]}"')

    if data.get("age"):
        query_parts.append(f'Age:"{data["age"]}"')

    if data.get("gender"):
        query_parts.append(f'Gender:"{data["gender"]}"')

    if data.get("lab_results"):
        lab_results_query = " OR ".join([f'"{result}"' for result in data["lab_results"]])
        query_parts.append(f'Lab_Results:({lab_results_query})')

    # Join all query parts with the "AND" operator to create a final Boolean query
    boolean_query = " AND ".join(query_parts)
    return f"({boolean_query})" if boolean_query else ""