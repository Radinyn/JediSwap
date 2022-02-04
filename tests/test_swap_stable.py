import pytest
import asyncio
from utils.events import get_event_data

def uint(a):
    return(a, 0)


async def initialize_stable_pairs(router, stable_token_0, stable_token_1, stable_token_2, user_1, random_acc):
    user_1_signer, user_1_account = user_1
    random_signer, random_account = random_acc
    
    print("\nMint loads of tokens to user_1")
    execution_info = await stable_token_0.decimals().call()
    stable_token_0_decimals = execution_info.result.decimals
    amount_to_mint_stable_token_0 = 100 * (10 ** stable_token_0_decimals)
    ## Mint stable_token_0 to user_1
    await random_signer.send_transaction(random_account, stable_token_0.contract_address, 'mint', [user_1_account.contract_address, *uint(amount_to_mint_stable_token_0)])
    
    execution_info = await stable_token_1.decimals().call()
    stable_token_1_decimals = execution_info.result.decimals
    amount_to_mint_stable_token_1 = 100 * (10 ** stable_token_1_decimals)
    ## Mint stable_token_1 to user_1
    await random_signer.send_transaction(random_account, stable_token_1.contract_address, 'mint', [user_1_account.contract_address, *uint(amount_to_mint_stable_token_1)])

    execution_info = await stable_token_2.decimals().call()
    stable_token_2_decimals = execution_info.result.decimals
    amount_to_mint_stable_token_2 = 100 * (10 ** stable_token_2_decimals)
    ## Mint stable_token_2 to user_1
    await random_signer.send_transaction(random_account, stable_token_2.contract_address, 'mint', [user_1_account.contract_address, *uint(amount_to_mint_stable_token_2)])

    amount_stable_token_0 = 20 * (10 ** stable_token_0_decimals)
    amount_stable_token_1 = 20 * (10 ** stable_token_1_decimals)
    print("Approve required tokens to be spent by router")
    await user_1_signer.send_transaction(user_1_account, stable_token_0.contract_address, 'approve', [router.contract_address, *uint(amount_stable_token_0)])
    await user_1_signer.send_transaction(user_1_account, stable_token_1.contract_address, 'approve', [router.contract_address, *uint(amount_stable_token_1)])
    
    ## New stable_pair with 0 liquidity
    print("Add liquidity to new stable_pair")
    execution_info = await user_1_signer.send_transaction(user_1_account, router.contract_address, 'add_liquidity', [
        stable_token_0.contract_address, 
        stable_token_1.contract_address, 
        *uint(amount_stable_token_0), 
        *uint(amount_stable_token_1), 
        *uint(0), 
        *uint(0), 
        user_1_account.contract_address, 
        0
    ])

    amount_stable_token_1 = 4 * (10 ** stable_token_1_decimals)
    amount_stable_token_2 = 4 * (10 ** stable_token_2_decimals)
    print("Approve required tokens to be spent by router")
    await user_1_signer.send_transaction(user_1_account, stable_token_1.contract_address, 'approve', [router.contract_address, *uint(amount_stable_token_1)])
    await user_1_signer.send_transaction(user_1_account, stable_token_2.contract_address, 'approve', [router.contract_address, *uint(amount_stable_token_2)])
    
    ## New stable_pair with 0 liquidity
    print("Add liquidity to new other stable_pair")
    execution_info = await user_1_signer.send_transaction(user_1_account, router.contract_address, 'add_liquidity', [
        stable_token_1.contract_address, 
        stable_token_2.contract_address, 
        *uint(amount_stable_token_1), 
        *uint(amount_stable_token_2), 
        *uint(0), 
        *uint(0), 
        user_1_account.contract_address, 
        0
    ])

async def mint_to_user_2(router, stable_token_0, stable_token_1, stable_token_2, user_2, random_acc):
    user_2_signer, user_2_account = user_2
    random_signer, random_account = random_acc
    
    print("\nMint loads of tokens to user_2")
    execution_info = await stable_token_0.decimals().call()
    stable_token_0_decimals = execution_info.result.decimals
    amount_to_mint_stable_token_0 = 100 * (10 ** stable_token_0_decimals)
    ## Mint stable_token_0 to user_2
    await random_signer.send_transaction(random_account, stable_token_0.contract_address, 'mint', [user_2_account.contract_address, *uint(amount_to_mint_stable_token_0)])
    print("Approve required tokens to be spent by router")
    await user_2_signer.send_transaction(user_2_account, stable_token_0.contract_address, 'approve', [router.contract_address, *uint(amount_to_mint_stable_token_0)])
    
    execution_info = await stable_token_1.decimals().call()
    stable_token_1_decimals = execution_info.result.decimals
    amount_to_mint_stable_token_1 = 100 * (10 ** stable_token_1_decimals)
    ## Mint stable_token_1 to user_2
    await random_signer.send_transaction(random_account, stable_token_1.contract_address, 'mint', [user_2_account.contract_address, *uint(amount_to_mint_stable_token_1)])

    execution_info = await stable_token_2.decimals().call()
    stable_token_2_decimals = execution_info.result.decimals
    amount_to_mint_stable_token_2 = 100 * (10 ** stable_token_2_decimals)
    ## Mint stable_token_2 to user_2
    await random_signer.send_transaction(random_account, stable_token_2.contract_address, 'mint', [user_2_account.contract_address, *uint(amount_to_mint_stable_token_2)])

@pytest.mark.asyncio
async def test_swap_exact_0_to_1(router, stable_token_0, stable_token_1, stable_token_2, stable_pair, other_stable_pair, user_1, user_2, random_acc):
    user_2_signer, user_2_account = user_2

    await initialize_stable_pairs(router, stable_token_0, stable_token_1, stable_token_2, user_1, random_acc)
    await mint_to_user_2(router, stable_token_0, stable_token_1, stable_token_2, user_2, random_acc)

    execution_info = await stable_token_0.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_0_balance_initial = execution_info.result.balance[0]

    execution_info = await stable_token_1.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_1_balance_initial = execution_info.result.balance[0]
    
    sort_info = await router.sort_tokens(stable_token_0.contract_address, stable_token_1.contract_address).call()
    
    execution_info = await stable_pair.get_reserves().call()
    if (sort_info.result.token0 == stable_token_0.contract_address):
        reserve_0_initial = execution_info.result.reserve0[0]
        reserve_1_initial = execution_info.result.reserve1[0]
    else:
        reserve_1_initial = execution_info.result.reserve0[0]
        reserve_0_initial = execution_info.result.reserve1[0]

    print(f"Initial balances: {user_2_stable_token_0_balance_initial}, {user_2_stable_token_1_balance_initial}, {reserve_0_initial}, {reserve_1_initial}")

    execution_info = await stable_token_0.decimals().call()
    stable_token_0_decimals = execution_info.result.decimals
    execution_info = await stable_token_1.decimals().call()
    stable_token_1_decimals = execution_info.result.decimals
    amount_stable_token_0 = 2 * (10 ** stable_token_0_decimals)
    print("Approve required tokens to be spent by router")
    await user_2_signer.send_transaction(user_2_account, stable_token_0.contract_address, 'approve', [router.contract_address, *uint(amount_stable_token_0)])

    ## Swap
    print("Swap")
    execution_info = await user_2_signer.send_transaction(user_2_account, router.contract_address, 'swap_exact_tokens_for_tokens', [
        *uint(amount_stable_token_0), 
        *uint(0), 
        2, 
        stable_token_0.contract_address, 
        stable_token_1.contract_address, 
        user_2_account.contract_address, 
        0
    ])

    amounts_len = execution_info.result.response[0]
    amounts = execution_info.result.response[1:]
    print(f"{amounts_len}, {amounts}")

    event_data = get_event_data(execution_info, "Swap")
    assert event_data

    execution_info = await stable_token_0.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_0_balance_final = execution_info.result.balance[0]

    execution_info = await stable_token_1.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_1_balance_final = execution_info.result.balance[0]

    execution_info = await stable_pair.get_reserves().call()
    reserve_0_final = execution_info.result.reserve0[0]
    reserve_1_final = execution_info.result.reserve1[0]

    print(f"Final balances: {user_2_stable_token_0_balance_final}, {user_2_stable_token_1_balance_final}, {reserve_0_final}, {reserve_1_final}")

    expected_amount_1 = (amount_stable_token_0 * (10 ** stable_token_1_decimals)) /  (10 ** stable_token_0_decimals)
    print(f"Expected amount for stable_token_1: {expected_amount_1}")

    assert user_2_stable_token_0_balance_initial - user_2_stable_token_0_balance_final == amounts[0]
    assert user_2_stable_token_1_balance_final - user_2_stable_token_1_balance_initial == amounts[-2]

    # assert user_2_stable_token_1_balance_final - user_2_stable_token_1_balance_initial == expected_amount_1 * 997.0 / 1000.0

@pytest.mark.asyncio
async def test_swap_0_to_exact_1(router, stable_token_0, stable_token_1, stable_token_2, stable_pair, other_stable_pair, user_1, user_2, random_acc):
    user_2_signer, user_2_account = user_2

    await initialize_stable_pairs(router, stable_token_0, stable_token_1, stable_token_2, user_1, random_acc)
    await mint_to_user_2(router, stable_token_0, stable_token_1, stable_token_2, user_2, random_acc)

    execution_info = await stable_token_0.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_0_balance_initial = execution_info.result.balance[0]

    execution_info = await stable_token_1.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_1_balance_initial = execution_info.result.balance[0]
    
    sort_info = await router.sort_tokens(stable_token_0.contract_address, stable_token_1.contract_address).call()
    
    execution_info = await stable_pair.get_reserves().call()
    if (sort_info.result.token0 == stable_token_0.contract_address):
        reserve_0_initial = execution_info.result.reserve0[0]
        reserve_1_initial = execution_info.result.reserve1[0]
    else:
        reserve_1_initial = execution_info.result.reserve0[0]
        reserve_0_initial = execution_info.result.reserve1[0]

    print(f"Initial balances: {user_2_stable_token_0_balance_initial}, {user_2_stable_token_1_balance_initial}, {reserve_0_initial}, {reserve_1_initial}")

    execution_info = await stable_token_0.decimals().call()
    stable_token_0_decimals = execution_info.result.decimals
    execution_info = await stable_token_1.decimals().call()
    stable_token_1_decimals = execution_info.result.decimals
    amount_stable_token_1 = 2 * (10 ** stable_token_1_decimals)

    ## Swap
    print("Swap")
    execution_info = await user_2_signer.send_transaction(user_2_account, router.contract_address, 'swap_tokens_for_exact_tokens', [
        *uint(amount_stable_token_1), 
        *uint(10 ** 30),  ## Random large number
        2, 
        stable_token_0.contract_address, 
        stable_token_1.contract_address, 
        user_2_account.contract_address, 
        0
    ])

    amounts_len = execution_info.result.response[0]
    amounts = execution_info.result.response[1:]
    print(f"{amounts_len}, {amounts}")

    event_data = get_event_data(execution_info, "Swap")
    assert event_data

    execution_info = await stable_token_0.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_0_balance_final = execution_info.result.balance[0]

    execution_info = await stable_token_1.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_1_balance_final = execution_info.result.balance[0]

    execution_info = await stable_pair.get_reserves().call()
    if (sort_info.result.token0 == stable_token_0.contract_address):
        reserve_0_final = execution_info.result.reserve0[0]
        reserve_1_final = execution_info.result.reserve1[0]
    else:
        reserve_1_final = execution_info.result.reserve0[0]
        reserve_0_final = execution_info.result.reserve1[0]

    print(f"Final balances: {user_2_stable_token_0_balance_final}, {user_2_stable_token_1_balance_final}, {reserve_0_final}, {reserve_1_final}")

    expected_amount_0 = ((amount_stable_token_1 * (10 ** stable_token_0_decimals)) /  (10 ** stable_token_1_decimals)) + 1
    print(f"Expected input amount for stable_token_0: {expected_amount_0}")

    assert user_2_stable_token_0_balance_initial - user_2_stable_token_0_balance_final == amounts[0]
    assert user_2_stable_token_1_balance_final - user_2_stable_token_1_balance_initial == amounts[-2]

    # assert user_2_stable_token_1_balance_final - user_2_stable_token_1_balance_initial == expected_amount_1 * 997.0 / 1000.0

@pytest.mark.asyncio
async def test_swap_exact_0_to_2(router, stable_token_0, stable_token_1, stable_token_2, stable_pair, other_stable_pair, user_1, user_2, random_acc):
    user_2_signer, user_2_account = user_2

    await initialize_stable_pairs(router, stable_token_0, stable_token_1, stable_token_2, user_1, random_acc)
    await mint_to_user_2(router, stable_token_0, stable_token_1, stable_token_2, user_2, random_acc)

    execution_info = await stable_token_0.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_0_balance_initial = execution_info.result.balance[0]

    execution_info = await stable_token_2.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_2_balance_initial = execution_info.result.balance[0]
    
    sort_info = await router.sort_tokens(stable_token_0.contract_address, stable_token_1.contract_address).call()
    
    execution_info = await stable_pair.get_reserves().call()
    if (sort_info.result.token0 == stable_token_0.contract_address):
        reserve_0_0_initial = execution_info.result.reserve0[0]
        reserve_1_0_initial = execution_info.result.reserve1[0]
    else:
        reserve_1_0_initial = execution_info.result.reserve0[0]
        reserve_0_0_initial = execution_info.result.reserve1[0]

    other_sort_info = await router.sort_tokens(stable_token_1.contract_address, stable_token_2.contract_address).call()
    
    execution_info = await other_stable_pair.get_reserves().call()
    if (other_sort_info.result.token0 == stable_token_1.contract_address):
        reserve_0_1_initial = execution_info.result.reserve0[0]
        reserve_1_1_initial = execution_info.result.reserve1[0]
    else:
        reserve_1_1_initial = execution_info.result.reserve0[0]
        reserve_0_1_initial = execution_info.result.reserve1[0]

    print(f"Initial balances: {user_2_stable_token_0_balance_initial}, {user_2_stable_token_2_balance_initial}, {reserve_0_0_initial}, {reserve_1_0_initial}, {reserve_0_1_initial}, {reserve_1_1_initial}")

    execution_info = await stable_token_0.decimals().call()
    stable_token_0_decimals = execution_info.result.decimals
    execution_info = await stable_token_1.decimals().call()
    stable_token_1_decimals = execution_info.result.decimals
    execution_info = await stable_token_2.decimals().call()
    stable_token_2_decimals = execution_info.result.decimals
    amount_stable_token_0 = 2 * (10 ** stable_token_0_decimals)
    print("Approve required tokens to be spent by router")
    await user_2_signer.send_transaction(user_2_account, stable_token_0.contract_address, 'approve', [router.contract_address, *uint(amount_stable_token_0)])

    ## Swap
    print("Swap")
    execution_info = await user_2_signer.send_transaction(user_2_account, router.contract_address, 'swap_exact_tokens_for_tokens', [
        *uint(amount_stable_token_0), 
        *uint(0), 
        3, 
        stable_token_0.contract_address, 
        stable_token_1.contract_address, 
        stable_token_2.contract_address, 
        user_2_account.contract_address, 
        0
    ])

    amounts_len = execution_info.result.response[0]
    amounts = execution_info.result.response[1:]
    print(f"{amounts_len}, {amounts}")

    event_data = get_event_data(execution_info, "Swap")
    assert event_data

    execution_info = await stable_token_0.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_0_balance_final = execution_info.result.balance[0]

    execution_info = await stable_token_2.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_2_balance_final = execution_info.result.balance[0]

    execution_info = await stable_pair.get_reserves().call()
    if (sort_info.result.token0 == stable_token_0.contract_address):
        reserve_0_0_final = execution_info.result.reserve0[0]
        reserve_1_0_final = execution_info.result.reserve1[0]
    else:
        reserve_1_0_final = execution_info.result.reserve0[0]
        reserve_0_0_final = execution_info.result.reserve1[0]

    execution_info = await other_stable_pair.get_reserves().call()
    if (other_sort_info.result.token0 == stable_token_1.contract_address):
        reserve_0_1_final = execution_info.result.reserve0[0]
        reserve_1_1_final = execution_info.result.reserve1[0]
    else:
        reserve_1_1_final = execution_info.result.reserve0[0]
        reserve_0_1_final = execution_info.result.reserve1[0]

    print(f"Final balances: {user_2_stable_token_0_balance_final}, {user_2_stable_token_2_balance_final}, {reserve_0_0_final}, {reserve_1_0_final}, {reserve_0_1_final}, {reserve_1_1_final}")

    expected_amount_1 = (amount_stable_token_0 * (10 ** stable_token_1_decimals)) /  (10 ** stable_token_0_decimals)
    print(f"Expected amount for stable_token_1: {expected_amount_1}")
    expected_amount_2 = (expected_amount_1 * (10 ** stable_token_2_decimals)) /  (10 ** stable_token_1_decimals)
    print(f"Expected amount for stable_token_2: {expected_amount_2}")

    assert user_2_stable_token_0_balance_initial - user_2_stable_token_0_balance_final == amounts[0]
    assert user_2_stable_token_2_balance_final - user_2_stable_token_2_balance_initial == amounts[-2]


@pytest.mark.asyncio
async def test_swap_exact_1_to_0(router, stable_token_0, stable_token_1, stable_token_2, stable_pair, other_stable_pair, user_1, user_2, random_acc):
    user_2_signer, user_2_account = user_2

    await initialize_stable_pairs(router, stable_token_0, stable_token_1, stable_token_2, user_1, random_acc)
    await mint_to_user_2(router, stable_token_0, stable_token_1, stable_token_2, user_2, random_acc)

    execution_info = await stable_token_0.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_0_balance_initial = execution_info.result.balance[0]

    execution_info = await stable_token_1.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_1_balance_initial = execution_info.result.balance[0]

    sort_info = await router.sort_tokens(stable_token_0.contract_address, stable_token_1.contract_address).call()
    
    execution_info = await stable_pair.get_reserves().call()
    if (sort_info.result.token0 == stable_token_0.contract_address):
        reserve_0_initial = execution_info.result.reserve0[0]
        reserve_1_initial = execution_info.result.reserve1[0]
    else:
        reserve_1_initial = execution_info.result.reserve0[0]
        reserve_0_initial = execution_info.result.reserve1[0]

    print(f"Initial balances: {user_2_stable_token_0_balance_initial}, {user_2_stable_token_1_balance_initial}, {reserve_0_initial}, {reserve_1_initial}")

    execution_info = await stable_token_0.decimals().call()
    stable_token_0_decimals = execution_info.result.decimals
    execution_info = await stable_token_1.decimals().call()
    stable_token_1_decimals = execution_info.result.decimals
    amount_stable_token_1 = 2 * (10 ** stable_token_1_decimals)
    print("Approve required tokens to be spent by router")
    await user_2_signer.send_transaction(user_2_account, stable_token_1.contract_address, 'approve', [router.contract_address, *uint(amount_stable_token_1)])

    ## Swap
    print("Swap")
    execution_info = await user_2_signer.send_transaction(user_2_account, router.contract_address, 'swap_exact_tokens_for_tokens', [
        *uint(amount_stable_token_1), 
        *uint(0), 
        2, 
        stable_token_1.contract_address, 
        stable_token_0.contract_address, 
        user_2_account.contract_address, 
        0
    ])

    amounts_len = execution_info.result.response[0]
    amounts = execution_info.result.response[1:]
    print(f"{amounts_len}, {amounts}")

    event_data = get_event_data(execution_info, "Swap")
    assert event_data

    execution_info = await stable_token_0.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_0_balance_final = execution_info.result.balance[0]

    execution_info = await stable_token_1.balanceOf(user_2_account.contract_address).call()
    user_2_stable_token_1_balance_final = execution_info.result.balance[0]

    execution_info = await stable_pair.get_reserves().call()
    if (sort_info.result.token0 == stable_token_0.contract_address):
        reserve_0_final = execution_info.result.reserve0[0]
        reserve_1_final = execution_info.result.reserve1[0]
    else:
        reserve_1_final = execution_info.result.reserve0[0]
        reserve_0_final = execution_info.result.reserve1[0]

    print(f"Final balances: {user_2_stable_token_0_balance_final}, {user_2_stable_token_1_balance_final}, {reserve_0_final}, {reserve_1_final}")

    expected_amount_0 = (amount_stable_token_1 * (10 ** stable_token_0_decimals)) /  (10 ** stable_token_1_decimals)
    print(f"Expected amount for stable_token_0: {expected_amount_0}")

    assert user_2_stable_token_1_balance_initial - user_2_stable_token_1_balance_final == amounts[0]
    assert user_2_stable_token_0_balance_final - user_2_stable_token_0_balance_initial == amounts[-2]

    # assert user_2_stable_token_1_balance_final - user_2_stable_token_1_balance_initial == expected_amount_1 * 997.0 / 1000.0
