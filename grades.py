import statistics


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def data_into_buckets(data):
    buckets = [0, 0, 0, 0, 0, 0, 0]
    # ["<50", "50-59", "60-69", "70-79", "80-89", ">=90", "NaN"]
    for grade in data:
        if not is_int(grade):
            buckets[6] += 1
            continue
        grade = int(grade)
        if grade < 50:
            buckets[0] += 1
        elif grade < 60:
            buckets[1] += 1
        elif grade < 70:
            buckets[2] += 1
        elif grade < 80:
            buckets[3] += 1
        elif grade < 90:
            buckets[4] += 1
        else:
            buckets[5] += 1
    return buckets


def get_dist_stats(data):
    int_data = [int(x) for x in data if is_int(x)]
    stdev = "0"
    if len(int_data) > 1:
        stdev = str(round(statistics.stdev(int_data), 1))
    return '\n'.join((
        "Total: " + str(len(data)),
        "Mean: " + str(round(statistics.mean(int_data), 1)),
        "Median: " + str(round(statistics.median(int_data), 1)),
        "Mode: " + str(round(statistics.mode(int_data), 1)),
        "Stdev: " + stdev,
        "Min: " + str(round(min(int_data), 1)),
        "Max: " + str(round(max(int_data), 1)),
        "Dist: [" + ", ".join(str(x) for x in data_into_buckets(data)) + "]"
    ))
