
def shunting_yard(regex):
    precedence = {"|": 1, ".": 2, "*": 3}
    queue = []
    stack = []

    regex = add_concat(regex)

    for token in regex:
        if token.isalpha() or token == "#":
            queue.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                queue.append(stack.pop())
            stack.pop()
        else:
            while (
                stack
                and stack[-1] != "("
                and precedence[token] <= precedence[stack[-1]]
            ):
                queue.append(stack.pop())
            stack.append(token)

    while stack:
        queue.append(stack.pop())

    return "".join(queue)


def add_concat(regex):
    output = ""
    operators = set([".", "|", "*", "(", ")"])  # regex operators
    for i in range(len(regex) - 1):
        output += regex[i]
        if (
            (regex[i] not in operators and regex[i + 1] not in operators)
            or (regex[i] not in operators and regex[i + 1] == "(")
            or (regex[i] == ")" and regex[i + 1] not in operators)
            or (regex[i] == "*" and regex[i + 1] not in operators)
            or (regex[i] == "*" and regex[i + 1] == "(")
        ):
            output += "."
    output += regex[-1]
    return output
  
