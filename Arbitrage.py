import itertools

# Given liquidity pools
liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

# Function to calculate the output amount using the Uniswap constant product formula
def get_output_amount(input_amount, input_liquidity, output_liquidity):
    input_amount_with_fee = input_amount * 0.997  # 0.3% trading fee
    numerator = input_amount_with_fee * output_liquidity
    denominator = input_liquidity + input_amount_with_fee
    return numerator / denominator

# Function to calculate profit for a given path
def calculate_profit(path, start_amount):
    amount = start_amount
    for i in range(len(path) - 1):
        token_in, token_out = path[i], path[i + 1]
        if (token_in, token_out) in liquidity:
            input_liquidity, output_liquidity = liquidity[(token_in, token_out)]
        else:
            output_liquidity, input_liquidity = liquidity[(token_out, token_in)]
        amount = get_output_amount(amount, input_liquidity, output_liquidity)
    return amount - start_amount

# Function to find the best arbitrage path
def find_best_arbitrage(liquidity, start_token, start_amount ):
    tokens = set(itertools.chain(*liquidity.keys()))
    max_profit = 0
    best_path = None
    for length in range(2, len(tokens)):  # Minimum cycle length is 3
        for path in itertools.permutations(tokens, length):
            if path[-1] == start_token:
                path = list(path)
                path.insert(0, start_token)
                profit = calculate_profit(path, start_amount)
                if profit > max_profit:
                    max_profit = profit
                    best_path = path
    return max_profit, best_path

# Starting with 5 units of tokenB
start_token = 'tokenB'
start_amount = 5
max_profit, best_path = find_best_arbitrage(liquidity, start_token, start_amount)

print("path: " + "->".join(best_path))
print(f"tokenB balance: {start_amount + max_profit}")