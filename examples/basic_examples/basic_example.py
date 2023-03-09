import csv


def path_from_shot_number(shot_number):
    return f"shot_{shot_number:02d}.csv"


def write_synthetic_oscilloscope_data(path, t_1, t_2, t_max, n_pts=101):
    with open(path, "w") as f:
        writer = csv.writer(f)
        for i in range(n_pts):
            t = i / (n_pts - 1) * t_max
            s_1 = 0 if t < t_1 else 1
            s_2 = 0 if t < t_2 else 1
            writer.writerow([t, s_1, s_2])


def read_oscilloscope_data(path):
    t_1 = None
    t_2 = None
    with open(path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            t, s_1, s_2 = row
            if t_1 is None and s_1 == "1":
                t_1 = float(t)
            if t_2 is None and s_2 == "1":
                t_2 = float(t)
            if (t_1 is not None) and (t_2 is not None):
                break
    return t_1, t_2


def calculate_velocity(shot_number, seperation):
    path = path_from_shot_number(shot_number)
    t_1, t_2 = read_oscilloscope_data(path)
    return seperation / (t_2 - t_1)


if __name__ == "__main__":
    n = 1
    path = path_from_shot_number(n)
    write_synthetic_oscilloscope_data(path, 2, 5, 10)
    velocity = calculate_velocity(n, 50)
    print(velocity)
