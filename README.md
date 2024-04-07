# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1

Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> - path: tokenB->tokenA->tokenD->tokenC->tokenB
> - tokenB amountIn: 5, tokenA amountOut: 5.655321988655323
> - tokenA amountIn: 5.655321988655323, tokenD amountOut: 2.458781317097934
> - tokenD amountIn: 2.458781317097934, tokenC amountOut: 5.0889272933015155
> - tokenC amountIn: 5.0889272933015155, tokenB amountOut: 20.129888944077447
> - final tokenB balance: 20.129888944077447

## Problem 2

What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> 1. 執行 swap 時，由於過程中可能有其他筆 swap 發生，造成 token 價格出現波動，導致最終實際得到的 token 數與你預期拿到的數量不一樣，兩者的差距就稱作滑價 (slippage)
> 2. 因為滑價無法避免，所以在 Uniswap 中可以設定你可以接受的滑價範圍，若交易的成交價格低於容忍範圍，那麼當筆交易就不會成交，以此來避免 Uniswap 價格上下浮動太大帶來的損失。以 `UniswapV2Router` 的 `swapExactTokensForTokens` 這個函式為例:

```solidity
function swapExactTokensForTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
) external override ensure(deadline) returns (uint[] memory amounts) {
    amounts = UniswapV2Library.getAmountsOut(factory, amountIn, path);
    require(amounts[amounts.length - 1] >= amountOutMin, 'UniswapV2Router: INSUFFICIENT_OUTPUT_AMOUNT');
    TransferHelper.safeTransferFrom(path[0], msg.sender, UniswapV2Library.pairFor(factory, path[0], path[1]), amounts[0]);
    _swap(amounts, path, to);
}
```

> > 在一系列的 swap 之前，會先去檢查現在情況下最後拿到的 token 數量 (`amounts[-1]`) 有沒有少於最低預期可以獲得的數量 (`amountOutMin`)，如果不如預期就把交易 revert 掉，如果符合預期就真正開始做交易。

## Problem 3

Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> 為了防止初期的流動性參與者 (attacker) 為壟斷交易對而刻意抬高流動性單價，使得散戶無力參與，沒辦法提供流動性，所以透過 burn MINIMUM_LIQUIDITY (=1000)，來保證首次 mint 時總流動性大於 1000。

## Problem 4

Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> 希望讓兩種 token 在 pool 裡的比例可以維持一個恆定值

## Problem 5

What is a sandwich attack, and how might it impact you when initiating a swap?

> 1. 用戶提交一筆 swap 交易，並處於等待確認的狀態。
> 2. 攻擊者注意到這筆待確認的交易，並知道該 token 的價格將上升。
> 3. 攻擊者利用這段時間搶先提交一筆 swap 交易並以較低的價格完成，token 價格上升。
> 4. 用戶的交易以較高的價格完成，這意味著用戶收到的 token 少於預期。
> 5. 攻擊者再次以較高的價格 swap token。
> 6. 攻擊者從前面兩筆交易的價格差異中獲利。
