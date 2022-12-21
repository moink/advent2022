from scipy.optimize import minimize_scalar

import advent_tools


def main():
    data = advent_tools.read_dict_from_input_file(sep=': ', key='left')
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def evaluate_expression(data, monkey_name):
    expression = data[monkey_name]
    try:
        number = float(expression)
    except ValueError:
        pass
    else:
        return number
    left_name, operator, right_name = expression.split()
    left = evaluate_expression(data, left_name)
    right = evaluate_expression(data, right_name)
    match operator:
        case "+":
            return left + right
        case "-":
            return left - right
        case "*":
            return left * right
        case "/":
            return left / right
        case "==":
            return (left - right) * (left - right)
    raise ValueError(f"Unknown operator '{operator}")


def run_part_1(data):
    return int(evaluate_expression(data, "root"))


def run_part_2(data):
    data["root"] = data["root"].replace("+", "==")

    def cost_function(human_number):
        data["humn"] = human_number
        cost = evaluate_expression(data, "root")
        return cost

    res = minimize_scalar(cost_function, tol=1e-16)
    return int(res.x)


if __name__ == '__main__':
    main()
