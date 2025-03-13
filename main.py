import math
import matplotlib.pyplot as plt


def sin_taylor(x, precision):
    if precision < 1:
        precision = 1

    if precision > 10:
        precision = 10

    y = 0
    for n in range(precision):
        sign = (-1) ** n
        power = pow(x, 2*n + 1)
        factorial = math.factorial(2*n + 1)

        y += sign * power / factorial
    return y

def my_sin(x, precision, is_rad=True):
    if not is_rad:
        x = x * math.pi / 180

    sign = 1

    x %= 2*math.pi  # sin(x) = sin(x+2kpi)
    # x in (-2pi, 2pi)

    if x < 0:  # sin(-x) = -sin(x)
        x = -x
        sign = -1
    # x in [0, 2pi)

    if x > math.pi/2:  # symmetry
        if x < math.pi:  # sin(pi-x) = sin(x)
            return sign * sin_taylor(math.pi-x, precision)
        elif x < 3*math.pi/2:  # sin(pi+x) = -sin(x)
            return -sign * sin_taylor(x-math.pi, precision)
        else:  # sin(2pi-x) = -sin(x)
            return -sign * sin_taylor(2*math.pi-x, precision)
    # x in [0, pi/2)

    return sign * sin_taylor(x, precision)

def draw_graphs_plot():
    fig, ax = plt.subplots(2, 5, figsize=(20, 5))
    x_values = [i * math.pi / 100 for i in range(-100, 100)]

    for pr in range(1, 11):
        index = int((pr - 1)/5), (pr - 1) % 5
        a = ax[index]

        sin_values = [math.sin(x) for x in x_values]
        my_sin_values = [my_sin(x, pr) for x in x_values]

        a.plot(x_values, sin_values, label=f"y = math.sin(x)", color='blue', linewidth=1)
        a.plot(x_values, my_sin_values, label=f"y = my_sin(x, {pr})", color='red', linewidth=1)

        a.set_title(f"precision={pr}")
        a.set_xlabel("x")
        a.set_ylabel("y")
        a.legend(bbox_to_anchor=(0.6, -0.2))

    plt.tight_layout()
    plt.savefig('graphs.png')

def draw_accuracy_plot():
    fig, ax = plt.subplots(2, 5, figsize=(20, 5))
    x_values = [i * math.pi / 100 for i in range(-100, 100)]

    for pr in range(1, 11):
        index = int((pr-1)/5), (pr-1) % 5
        a = ax[index]

        accuracy_values = [abs(math.sin(x) - my_sin(x, pr)) for x in x_values]

        a.plot(x_values, accuracy_values, label=f"accuracy", color='black', linewidth=1)

        a.set_title(f"precision={pr}")
        a.set_xlabel("x")
        a.set_ylabel(f"accuracy")
        a.legend(bbox_to_anchor=(0.4, -0.2))

    plt.tight_layout()
    plt.savefig('accuracy.png')


def main():
    for p in range(1, 11):
        print(f"Precision: {p}")
        val = 0.0

        for i in range(40):
            result = my_sin(val, p)
            print(f"sin({val:.16f}) ~ {result:.16f} [accuracy {abs(result - math.sin(val)):.16f}]")
            val += math.pi/10

    draw_graphs_plot()
    draw_accuracy_plot()


if __name__ == '__main__':
    main()
