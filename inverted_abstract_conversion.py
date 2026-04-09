def convert_inverted_abstract(inv_abstract: dict) -> str:
    max_value = 0
    abstract = []

    for key, value in inv_abstract.items():
        current_max = max(value)
        if current_max > max_value:
            max_value = current_max

    abstract_len = max_value + 1

    for i in range(abstract_len):
        for key, value in inv_abstract.items():
            if i in value:
                abstract.append(key)
                break

    return " ".join(abstract)
