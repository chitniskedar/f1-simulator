from models import Driver, Car, Track
from simulation import simulate_qualifying

drivers = [
    Driver("Verstappen", 96, 98, 92, 95, 97, 85),
    Driver("Leclerc", 94, 93, 88, 90, 89, 87),
    Driver("Norris", 92, 91, 87, 88, 90, 80),
]

cars = [
    Car("Red Bull", 97, 95, 93, 92),
    Car("Ferrari", 94, 92, 91, 88),
    Car("McLaren", 93, 90, 92, 90),
]

bahrain = Track("Bahrain", 90.0, 95.0, 1.4, 0.7, 0.35)

grid = simulate_qualifying(drivers, cars, bahrain)

print("=== Predicted Qualifying ===")
for pos, entry in enumerate(grid, start=1):
    print(f"P{pos}: {entry['driver']} - {entry['lap_time']}s")
