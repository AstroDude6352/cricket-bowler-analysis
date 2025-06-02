import json
import matplotlib.pyplot as plt

with open('335982.json', 'r') as f:
    data = json.load(f)

total_overs = data['info']['overs']
innings_list = data['innings']

for innings in innings_list:
    team = innings.get('team', 'Unknown team')
    print(f"\nInnings: {team}")

    wickets_lost = 0
    total_runs = 0
    balls_bowled = 0

    # Batter stats: runs & balls
    batter_stats = {}

    # Bowler stats with per-over data for plotting
    bowler_stats = {}  
    # Format: {bowler: {'runs_conceded': int, 'balls_bowled': int, 'wickets': int, 'runs_by_over': [], 'wickets_by_over': []}}

    # Initialize current strike and non-strike (from first delivery)
    first_over = innings['overs'][0]
    first_delivery = first_over['deliveries'][0]
    striker = first_delivery.get('batter', 'Unknown')
    non_striker = first_delivery.get('non_striker', 'Unknown')

    for over_data in innings['overs']:
        over_num = over_data.get('over', 0)

        # Track runs and wickets per over for each bowler for plotting
        bowler_runs_this_over = {}
        bowler_wickets_this_over = {}

        # Process deliveries in the over
        for delivery in over_data['deliveries']:
            runs = delivery['runs'].get('total', 0)
            extras = delivery['runs'].get('extras', 0)
            batter_runs = delivery['runs'].get('batter', 0)
            batter = delivery.get('batter', 'Unknown')
            bowler = delivery.get('bowler', 'Unknown')

            total_runs += runs
            balls_bowled += 1

            # Update batter stats
            if batter not in batter_stats:
                batter_stats[batter] = {'runs': 0, 'balls': 0}
            batter_stats[batter]['runs'] += batter_runs
            batter_stats[batter]['balls'] += 1

            # Initialize bowler stats if needed
            if bowler not in bowler_stats:
                bowler_stats[bowler] = {
                    'runs_conceded': 0,
                    'balls_bowled': 0,
                    'wickets': 0,
                    'runs_by_over': [],
                    'wickets_by_over': []
                }
            bowler_stats[bowler]['runs_conceded'] += runs
            bowler_stats[bowler]['balls_bowled'] += 1

            bowler_runs_this_over[bowler] = bowler_runs_this_over.get(bowler, 0) + runs
            bowler_wickets_this_over[bowler] = bowler_wickets_this_over.get(bowler, 0)

            # Wickets update
            if 'wickets' in delivery:
                for wicket in delivery['wickets']:
                    wickets_lost += 1
                    bowler_stats[bowler]['wickets'] += 1
                    bowler_wickets_this_over[bowler] = bowler_wickets_this_over.get(bowler, 0) + 1

            # Strike rotation rules:
            # 1) Runs scored odd → swap strike
            # 2) Extras don’t swap strike unless they include bye/legbye runs (simplify to not swap on wides/no balls here)
            # 3) End of over → swap strike

            # Swap strike on odd runs scored by batter
            if batter_runs % 2 == 1:
                striker, non_striker = non_striker, striker

        # End of over swap strike
        striker, non_striker = non_striker, striker

        wickets_left = 10 - wickets_lost
        overs_left = total_overs - (over_num + 1)

        def strike_rate(stats):
            if stats['balls'] == 0:
                return 0
            return round((stats['runs'] / stats['balls']) * 100, 2)

        print(f"\nOver #{over_num + 1} (Overs left: {overs_left}), Wickets left: {wickets_left}")
        print(f"Team score: {total_runs} / {wickets_lost}")
        print("Batters on strike:")
        print(f" - {striker}, Strike rate: {strike_rate(batter_stats.get(striker, {'runs':0,'balls':0}))}")
        print(f" - {non_striker}, Strike rate: {strike_rate(batter_stats.get(non_striker, {'runs':0,'balls':0}))}")

        # Append over stats for each bowler bowling this over
        for bowler in bowler_runs_this_over.keys():
            bowler_stats[bowler]['runs_by_over'].append((over_num + 1, bowler_runs_this_over[bowler]))
            bowler_stats[bowler]['wickets_by_over'].append((over_num + 1, bowler_wickets_this_over.get(bowler, 0)))

    # --- Plotting section ---
    print("\nPlotting bowlers' economy rate with wickets...")

    plt.figure(figsize=(12, 6))
    for bowler, stats in bowler_stats.items():
        overs = [x[0] for x in stats['runs_by_over']]
        runs_per_over = [x[1] for x in stats['runs_by_over']]

        # Calculate cumulative runs and balls to compute economy rate over overs
        cum_runs = 0
        cum_balls = 0
        economies = []
        for over_idx, runs_this_over in enumerate(runs_per_over):
            cum_runs += runs_this_over
            cum_balls += 6  # 6 balls per over assumed
            economy = cum_runs / (cum_balls / 6)
            economies.append(economy)

        plt.plot(overs, economies, label=bowler)

            # Mark wickets on the graph
        for (over_num, wickets_in_over) in stats['wickets_by_over']:
            idx = over_num - 1
            if wickets_in_over > 0 and 0 <= idx < len(economies):
                plt.scatter(over_num, economies[idx], color='red', s=100, marker='X')  # Red X for wickets


    plt.xlabel('Over Number')
    plt.ylabel('Economy Rate (runs per over)')
    plt.title(f'Bowler Economy Rates with Wickets - Innings: {team}')
    plt.legend()
    plt.grid(True)
    plt.show()
