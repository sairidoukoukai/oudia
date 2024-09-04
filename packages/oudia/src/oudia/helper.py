def snake_case_to_CamelCase(snake_case: str) -> str:
    return "".join(word.title() for word in snake_case.split("_"))
