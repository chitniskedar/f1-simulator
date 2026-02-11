import random

def simulate_qualifying(drivers, cars, track):
    results = []

    for driver, car in zip(drivers, cars):

        quali_score = (
            0.45 * driver.quali_skill +
            0.40 * car.raw_performance +
            0.10 * car.straight_line_speed +
            0.05 * random.uniform(-2, 2)
        )

        lap_time = (
            track.base_quali_time
            - quali_score * 0.015
            + random.uniform(0, 0.3)
        )

        results.append({
            "driver": driver.name,
            "lap_time": round(lap_time, 3)
        })

    results.sort(key=lambda x: x["lap_time"])
    return results
