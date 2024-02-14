def format(regex):
    all_operators = ["|", "+", "?", "*"]
    binary_operators = ["|"]
    res = ""

    for i in range(len(regex)):
        c1 = regex[i]

        if i + 1 < len(regex):
            c2 = regex[i + 1]

            res += c1

            if (
                c1 != "("
                and c2 != ")"
                and c2 not in all_operators
                and c1 not in binary_operators
            ):
                res += "."

    res += regex[-1]
    return res


def shunting_yard(regex):
    precedence = {"|": 1, ".": 2, "*": 3, "+": 3, "?": 3}
    queue = []
    stack = []

    regex = format(regex)
    print("regex", regex)

    for token in regex:
        if token.isalnum() or token in [
            "#",
            "ϵ",
        ]:
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


def is_balanced(expression):
    stack = []
    for char in expression:
        if char == "(":
            stack.append(char)
        elif char == ")":
            if not stack or stack.pop() != "(":
                print("\tError: Unbalanced expression")
                return False
    balanced = len(stack) == 0
    if balanced:
        return True
    else:
        print("\tError: Unbalanced expression")
        return False
    # return len(stack) == 0
