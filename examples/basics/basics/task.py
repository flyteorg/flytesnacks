from flytekit import task


# Create a task that computes the slope of a regression line
@task
def slope(x: list[int], y: list[int]) -> float:
    sum_xy = sum([x[i] * y[i] for i in range(len(x))])
    sum_x_squared = sum([x[i] ** 2 for i in range(len(x))])
    n = len(x)
    return (n * sum_xy - sum(x) * sum(y)) / (n * sum_x_squared - sum(x) ** 2)


# Run the task locally like a Python function
if __name__ == "__main__":
    print(slope(x=[-3, 0, 3], y=[7, 4, -2]))
