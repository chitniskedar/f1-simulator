from data_fetch import fetch_qualifying, fetch_race
from prediction import simulate_2026_quali

df_quali_24 = fetch_qualifying(2024)
df_quali_25 = fetch_qualifying(2025)

df_race_24 = fetch_race(2024)
df_race_25 = fetch_race(2025)

print(df_quali_25["circuit"].unique())

track = input("Enter track name: ")

results = simulate_2026_quali(
    df_quali_24,
    df_quali_25,
    df_race_24,
    df_race_25,
    track,
    simulations=4000
)
results = results.rename(columns={
    "pole_probability_%": "pole_probability"
})


print("\n ---QUALI PREDICTIONS--- \n")

for pos, row in enumerate(results.itertuples(), start=1):
    print(
        f"P{pos:>2} | "
        f"{row.driver:<22} "
        f"{row.team:<12} | "
        f"Pole: {row.pole_probability:>6.2f}% | "
        f"Avg Grid: {row.avg_quali_position:>4.2f}"
    )
