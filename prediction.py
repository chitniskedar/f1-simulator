import pandas as pd
import random
from season_2026 import driver_team_2026

def simulate_2026_quali(df_quali_24, df_quali_25,
                        df_race_24, df_race_25,
                        track_name,
                        simulations=4000):

    # Combine seasons
    df_quali_all = pd.concat([df_quali_24, df_quali_25])
    df_race_all = pd.concat([df_race_24, df_race_25])

    # --------------------------
    # TRACK PERFORMANCE (both years)
    # --------------------------
    track_df = df_quali_all[
        df_quali_all["circuit"].str.lower() == track_name.lower()
    ]

    track_stats = track_df.groupby("driver").agg(
        avg_quali=("position", "mean")
    ).reset_index()

    track_stats["track_index"] = 1 / track_stats["avg_quali"]

    mean_track = track_stats["track_index"].mean()
    std_track = track_stats["track_index"].std()

    track_stats["track_index"] = (
        (track_stats["track_index"] - mean_track) / std_track
    )

    # --------------------------
    # SEASON 2025
    # --------------------------
    season_25 = df_quali_25.groupby("driver").agg(
        avg_quali=("position", "mean")
    ).reset_index()

    season_25["season25_index"] = 1 / season_25["avg_quali"]
    season_25["season25_index"] = (
        (season_25["season25_index"] - season_25["season25_index"].mean())
        / season_25["season25_index"].std()
    )

    # --------------------------
    # SEASON 2024
    # --------------------------
    season_24 = df_quali_24.groupby("driver").agg(
        avg_quali=("position", "mean")
    ).reset_index()

    season_24["season24_index"] = 1 / season_24["avg_quali"]
    season_24["season24_index"] = (
        (season_24["season24_index"] - season_24["season24_index"].mean())
        / season_24["season24_index"].std()
    )

    # --------------------------
    # MERGE DRIVER PERFORMANCE
    # --------------------------
    driver_stats = track_stats.merge(
        season_25[["driver", "season25_index"]],
        on="driver",
        how="left"
    ).merge(
        season_24[["driver", "season24_index"]],
        on="driver",
        how="left"
    )

    driver_stats = driver_stats.fillna(0)

    # Final blended driver index
    driver_stats["driver_index"] = (
        0.2 * driver_stats["track_index"] +
        0.5 * driver_stats["season25_index"] +
        0.3 * driver_stats["season24_index"]
    )

    driver_stats["team"] = driver_stats["driver"].map(driver_team_2026)

    # --------------------------
    # TEAM STRENGTH (both years)
    # --------------------------
    team_df = df_race_all.groupby("driver").agg(
        avg_finish=("position", "mean")
    ).reset_index()

    team_df["team"] = team_df["driver"].map(driver_team_2026)

    team_strength = team_df.groupby("team").agg(
        team_avg_finish=("avg_finish", "mean")
    ).reset_index()

    team_strength["team_index"] = 1 / team_strength["team_avg_finish"]
    team_strength["team_index"] = (
        (team_strength["team_index"] - team_strength["team_index"].mean())
        / team_strength["team_index"].std()
    )

    # --------------------------
    # MERGE FINAL GRID
    # --------------------------
    final = driver_stats.merge(
        team_strength[["team", "team_index"]],
        on="team",
        how="left"
    )

    all_drivers = pd.DataFrame({
        "driver": list(driver_team_2026.keys()),
        "team": list(driver_team_2026.values())
    })

    final = all_drivers.merge(final, on=["driver", "team"], how="left")
    final = final.fillna(0)

    # --------------------------
    # MONTE CARLO
    # --------------------------
    variance = 1.0

    pole_counts = {d: 0 for d in final["driver"]}
    avg_positions = {d: [] for d in final["driver"]}

    for _ in range(simulations):

        temp = final.copy()
        noise = [random.gauss(0, variance) for _ in range(len(temp))]

        temp["score"] = (
            0.6 * temp["driver_index"] +
            0.4 * temp["team_index"] +
            noise
        )

        temp = temp.sort_values("score", ascending=False).reset_index(drop=True)

        pole_counts[temp.loc[0, "driver"]] += 1

        for pos, row in enumerate(temp.itertuples(), start=1):
            avg_positions[row.driver].append(pos)

    results = []

    for driver in final["driver"]:
        results.append({
            "driver": driver,
            "team": driver_team_2026[driver],
            "pole_probability_%": round(100 * pole_counts[driver] / simulations, 2),
            "avg_quali_position": round(sum(avg_positions[driver]) / simulations, 2)
        })

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("pole_probability_%", ascending=False)

    return results_df
