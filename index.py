import numpy as np
import sys

def min_production_time(processing_times, switch_costs):
    """
    Calculates the minimum total production time
    
    Args:
        processing_times: n x m matrix, processing_times[i][j] = processing time of job i on machine j
        switch_costs: m x m matrix, switch_costs[i][j] = time cost to switch from machine i to machine j
    
    Returns:
        min_time: Minimum total time
        best_machines: List of machines to use for each job
    """
    n = len(processing_times)  # Number of jobs
    m = len(processing_times[0])  # Number of machines
    
    # dp[i][j] = best solution for jobs up to i, ending with machine j
    dp = np.full((n, m), np.inf)
    #dp[i][j]

    # Path matrix to track which machine was used before
    path = np.zeros((n, m), dtype=int)
    
    # Initial state: time for the first job on each machine
    for j in range(m):
        dp[0][j] = processing_times[0][j]
    
    # For each job
    for i in range(1, n):
        # For each machine choice
        for j in range(m):
            # Previous job's machine
            for k in range(m):
                # Previous best solution + machine switch cost + job processing time
                cost = dp[i-1][k] + switch_costs[k][j] + processing_times[i][j]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    path[i][j] = k
    
    # Find best final machine choice
    min_time = float('inf')
    last_machine = 0
    for j in range(m):
        if dp[n-1][j] < min_time:
            min_time = dp[n-1][j]
            last_machine = j
    
    # Extract the optimal solution path
    best_machines = [0] * n
    best_machines[n-1] = last_machine
    
    for i in range(n-1, 0, -1):
        best_machines[i-1] = path[i][best_machines[i]]
    
    return min_time, best_machines

# Test cases

def test_random():
    """Random test case"""
    np.random.seed(42)
    n = 10  # Number of jobs
    m = 5   # Number of machines
    
    processing_times = np.random.randint(1, 10, size=(n, m))
    switch_costs = np.random.randint(1, 5, size=(m, m))
    
    # Zero cost for staying on the same machine
    for i in range(m):
        switch_costs[i][i] = 0
    
    min_time, best_machines = min_production_time(processing_times, switch_costs)
    print(f"Random Test Case (n={n}, m={m}):")
    print(f"Minimum Total Time: {min_time}")
    print(f"Best Machine Selection: {best_machines}")
    
    # Solution validation
    total = processing_times[0][best_machines[0]]
    for i in range(1, n):
        prev_machine = best_machines[i-1]
        curr_machine = best_machines[i]
        total += switch_costs[prev_machine][curr_machine] + processing_times[i][curr_machine]
    
    print(f"Validation: {'Success' if abs(min_time - total) < 1e-6 else 'Failed'}")
    print()

if __name__ == "__main__":
    test_random()