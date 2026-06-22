# ================================================================
#        SMART TRAFFIC SIGNAL TIMING SYSTEM
#         Using Greedy Algorithm + Tie-Breaker Factors
# ================================================================
# ADA Mini Project
#
# Greedy Algorithm Concept:
#   Primary key  → Vehicle count (highest first)
#   Tie-Breakers → Emergency Vehicle > Cannot Wait >
#                  VIP Route > Accident Report
#
#   When two roads have equal vehicle count, the system scores
#   each road using the tie-breaker factors and picks the one
#   with the highest composite score — still a greedy choice,
#   just with a richer priority function.
# ================================================================

import time

# ── Constants ────────────────────────────────────────────────────
ROADS            = ["A", "B", "C", "D"]
MIN_GREEN_TIME   = 10          # seconds
MAX_GREEN_TIME   = 60          # seconds
ROUND_ROBIN_TIME = 15          # seconds (used when ALL scores are equal)

# Tie-breaker weights (higher = more important)
WEIGHT_EMERGENCY = 100
WEIGHT_WAIT      = 40          # cannot wait → higher urgency
WEIGHT_VIP       = 50
WEIGHT_ACCIDENT  = 30

EMERGENCY_OPTIONS = {"1": "Ambulance", "2": "Fire Truck", "3": "Police", "4": "None"}

# ================================================================
# 1. INPUT
# ================================================================

def ask_int(prompt, min_val=0):
    """Re-prompt until a valid integer >= min_val is entered."""
    while True:
        try:
            val = int(input(prompt).strip())
            if val < min_val:
                print(f"  ⚠  Value must be ≥ {min_val}. Try again.\n")
                continue
            return val
        except ValueError:
            print("  ⚠  Invalid input. Enter a whole number.\n")

def ask_yes_no(prompt):
    """Re-prompt until 'y' or 'n' is entered. Returns bool."""
    while True:
        val = input(prompt).strip().lower()
        if val in ("y", "n"):
            return val == "y"
        print("  ⚠  Enter y or n.\n")

def ask_emergency(prompt):
    """Return the emergency vehicle string for a road."""
    print(prompt)
    for k, v in EMERGENCY_OPTIONS.items():
        print(f"     {k}. {v}")
    while True:
        choice = input("     Choice: ").strip()
        if choice in EMERGENCY_OPTIONS:
            return EMERGENCY_OPTIONS[choice]
        print("  ⚠  Enter 1 / 2 / 3 / 4.\n")

def get_road_data():
    """Collect all factors for each road."""
    print("\n" + "=" * 52)
    print("      SMART TRAFFIC SIGNAL TIMING SYSTEM")
    print("=" * 52)
    print("\n  Enter details for each road:\n")

    roads = []
    for name in ROADS:
        print(f"  ── Road {name} " + "─" * 30)
        vehicles  = ask_int(f"  Vehicles on Road {name}          : ")
        can_wait  = ask_yes_no(f"  Can Road {name} wait?  (y/n)      : ")
        emergency = ask_emergency(f"  Emergency vehicle on Road {name}?")
        vip       = ask_yes_no(f"  VIP / Priority route? (y/n)      : ")
        accident  = ask_yes_no(f"  Accident reported?    (y/n)      : ")
        print()

        roads.append({
            "name"      : f"Road {name}",
            "vehicles"  : vehicles,
            "can_wait"  : can_wait,
            "emergency" : emergency,
            "vip"       : vip,
            "accident"  : accident,
        })
    return roads

# ================================================================
# 2. PRIORITY SCORE (Tie-Breaker)
# ================================================================

def calc_score(road):
    """
    Composite tie-breaker score.
    Used ONLY when two or more roads share the same vehicle count.
      +100  Emergency vehicle present
      +40   Cannot wait (urgent)
      +50   VIP / priority route
      +30   Accident reported
    """
    score = 0
    if road["emergency"] != "None":
        score += WEIGHT_EMERGENCY
    if not road["can_wait"]:
        score += WEIGHT_WAIT
    if road["vip"]:
        score += WEIGHT_VIP
    if road["accident"]:
        score += WEIGHT_ACCIDENT
    return score

# ================================================================
# 3. CASE DETECTION
# ================================================================

def detect_case(roads):
    """
    'all_equal'  – same vehicles AND same score  → pure Round Robin
    'tie'        – same vehicles but diff scores → tie-breaker used
    'normal'     – clear winner by vehicle count
    """
    counts    = [r["vehicles"] for r in roads]
    max_count = max(counts)
    tied      = [r for r in roads if r["vehicles"] == max_count]

    if len(set(counts)) == 1:
        scores = [calc_score(r) for r in roads]
        if len(set(scores)) == 1:
            return "all_equal"
        return "tie"          # equal vehicles but factors differ
    if len(tied) > 1:
        return "tie"
    return "normal"

# ================================================================
# 4. GREEDY SORT — Primary + Tie-Breaker Key
# ================================================================

def greedy_sort(roads):
    """
    Greedy sort with composite key:
      1st  →  vehicle count       (descending)
      2nd  →  tie-breaker score   (descending)
    Time Complexity: O(n log n)
    """
    return sorted(roads,
                  key=lambda r: (r["vehicles"], calc_score(r)),
                  reverse=True)

# ================================================================
# 5. GREEN TIME & WAITING TIME
# ================================================================

def calc_green_time(road):
    """
    Base green time from vehicles.
    Emergency vehicle gets +10s bonus.
    """
    base  = max(MIN_GREEN_TIME, min(int(road["vehicles"] * 0.5), MAX_GREEN_TIME))
    bonus = 10 if road["emergency"] != "None" else 0
    return min(base + bonus, MAX_GREEN_TIME)

def calc_waiting_times(priority_order):
    cumulative = 0
    result = []
    for road in priority_order:
        result.append({"name": road["name"], "wait": cumulative})
        cumulative += calc_green_time(road)
    return result

# ================================================================
# 6. DISPLAY
# ================================================================

def display_traffic_table(roads):
    """Show all input factors in a table."""
    print("\n" + "-" * 52)
    print("  Traffic Data (All Factors):")
    print("-" * 52)
    header = f"  {'Road':<10} {'Veh':>4}  {'CanWait':<9} {'Emergency':<12} {'VIP':<5} {'Acc'}"
    print(header)
    print("  " + "-" * 50)
    for r in roads:
        vip      = "Yes" if r["vip"]      else "No"
        acc      = "Yes" if r["accident"] else "No"
        can_wait = "Yes" if r["can_wait"] else "No"
        bar      = "█" * min(r["vehicles"] // 5, 15)
        print(f"  {r['name']:<10} {r['vehicles']:>4}  {can_wait:<9}"
              f"{r['emergency']:<12} {vip:<5} {acc}   {bar}")

def display_scores(roads, case):
    """Show tie-breaker scores when relevant."""
    if case == "normal":
        return
    print("\n" + "-" * 52)
    print("  Tie-Breaker Score Breakdown:")
    print("-" * 52)
    print(f"  {'Road':<10} {'Vehicles':>8}  {'Score':>6}  Reason")
    print("  " + "-" * 46)
    for r in roads:
        parts  = []
        score  = 0
        if r["emergency"] != "None":
            parts.append(f"+{WEIGHT_EMERGENCY} ({r['emergency']})")
            score += WEIGHT_EMERGENCY
        if not r["can_wait"]:
            parts.append(f"+{WEIGHT_WAIT} (cannot wait)")
            score += WEIGHT_WAIT
        if r["vip"]:
            parts.append(f"+{WEIGHT_VIP} (VIP)")
            score += WEIGHT_VIP
        if r["accident"]:
            parts.append(f"+{WEIGHT_ACCIDENT} (Accident)")
            score += WEIGHT_ACCIDENT
        reason = ", ".join(parts) if parts else "No bonus"
        print(f"  {r['name']:<10} {r['vehicles']:>8}  {score:>6}  {reason}")

def display_priority_order(priority_order, case):
    print("\n" + "-" * 52)
    print("  Applying Greedy Algorithm...\n")

    if case == "all_equal":
        print("  ⚠  All roads have equal vehicles AND equal scores.")
        print("  ➤  No greedy distinction possible.")
        print("  ➤  Switching to Round Robin Scheduling.\n")
        print(f"  Each road gets {ROUND_ROBIN_TIME}s green time equally.")
        print("-" * 52)
        for i, road in enumerate(priority_order, 1):
            print(f"  {i}. {road['name']} → Green Time: {ROUND_ROBIN_TIME}s")

    elif case == "tie":
        max_v = priority_order[0]["vehicles"]
        print("  ⚠  Tie detected on vehicle count!")
        print("  ➤  Applying tie-breaker factors:\n")
        print("     Priority: Emergency > Cannot Wait > VIP > Accident\n")
        print("  Final Priority Order (Greedy + Tie-Breaker):")
        print("-" * 52)
        for i, road in enumerate(priority_order, 1):
            gt    = calc_green_time(road)
            score = calc_score(road)
            tag   = " ← TIE-BROKEN" if road["vehicles"] == max_v else ""
            emg   = f" 🚨{road['emergency']}" if road["emergency"] != "None" else ""
            print(f"  {i}. {road['name']} ({road['vehicles']} veh, score={score})"
                  f" → {gt}s{emg}{tag}")

    else:
        print("  Priority Order (Highest → Lowest Traffic):")
        print("-" * 52)
        for i, road in enumerate(priority_order, 1):
            gt  = calc_green_time(road)
            emg = f" 🚨{road['emergency']}" if road["emergency"] != "None" else ""
            print(f"  {i}. {road['name']} ({road['vehicles']} vehicles) → {gt}s{emg}")

def display_green_signals(priority_order, case):
    print("\n" + "-" * 52)
    print("  Green Signal Allocation:")
    print("-" * 52)
    for road in priority_order:
        emg  = f"  [{road['emergency']}]" if road["emergency"] != "None" else ""
        time_s = ROUND_ROBIN_TIME if case == "all_equal" else calc_green_time(road)
        print(f"  {road['name']:<10} → 🟢 GREEN  ({time_s}s){emg}")
        time.sleep(0.25)

def display_waiting_times(wait_times, case):
    print("\n" + "-" * 52)
    print("  Estimated Waiting Times:")
    print("-" * 52)
    if case == "all_equal":
        for i, entry in enumerate(wait_times):
            wait  = i * ROUND_ROBIN_TIME
            label = "(goes first — no wait)" if wait == 0 else f"~{wait}s"
            print(f"  {entry['name']:<10}: {label}")
    else:
        for entry in wait_times:
            label = "(goes first — no wait)" if entry["wait"] == 0 else f"~{entry['wait']}s"
            print(f"  {entry['name']:<10}: {label}")

def display_statistics(roads, priority_order):
    total   = sum(r["vehicles"] for r in roads)
    average = total / len(roads)
    highest = priority_order[0]
    lowest  = priority_order[-1]
    emg     = [r["name"] for r in roads if r["emergency"] != "None"]
    vips    = [r["name"] for r in roads if r["vip"]]
    accs    = [r["name"] for r in roads if r["accident"]]

    print("\n" + "-" * 52)
    print("  Statistics:")
    print("-" * 52)
    print(f"  Highest Traffic Road  : {highest['name']} ({highest['vehicles']} vehicles)")
    print(f"  Lowest Traffic Road   : {lowest['name']} ({lowest['vehicles']} vehicles)")
    print(f"  Total Vehicles        : {total}")
    print(f"  Average per Road      : {average:.1f} vehicles")
    print(f"  Emergency Roads       : {', '.join(emg) if emg else 'None'}")
    print(f"  VIP Routes            : {', '.join(vips) if vips else 'None'}")
    print(f"  Accident Roads        : {', '.join(accs) if accs else 'None'}")

def display_algorithm_summary(case):
    print("\n" + "-" * 52)
    print("  Greedy Algorithm — Explanation:")
    print("-" * 52)
    print("  Primary Factor  : Vehicle Count (sorted descending)")
    print("  Tie-Breakers    :")
    print(f"    1. Emergency Vehicle  (+{WEIGHT_EMERGENCY} pts)  — highest urgency")
    print(f"    2. Cannot Wait        (+{WEIGHT_WAIT} pts)  — road needs immediate clearance")
    print(f"    3. VIP Route          (+{WEIGHT_VIP} pts)  — designated priority")
    print(f"    4. Accident Report    (+{WEIGHT_ACCIDENT} pts)  — safety clearance")
    print()
    if case == "all_equal":
        print("  Outcome : All values equal → Round Robin used.")
        print("  Complexity : O(n) — no sorting required.")
    elif case == "tie":
        print("  Outcome : Tie broken using composite score.")
        print("  Complexity : O(n log n) — greedy sort with score key.")
    else:
        print("  Outcome : Clear greedy winner by vehicle count.")
        print("  Complexity : O(n log n)  |  Space: O(n)")

# ================================================================
# 7. MAIN
# ================================================================

def main():
    roads          = get_road_data()
    case           = detect_case(roads)
    priority_order = greedy_sort(roads)
    wait_times     = calc_waiting_times(priority_order)

    display_traffic_table(roads)
    display_scores(roads, case)
    display_priority_order(priority_order, case)
    display_green_signals(priority_order, case)
    display_waiting_times(wait_times, case)
    display_statistics(roads, priority_order)
    display_algorithm_summary(case)

    print("\n" + "=" * 52)
    print("        ✅  Simulation Completed Successfully.")
    print("=" * 52 + "\n")

if __name__ == "__main__":
    main()
