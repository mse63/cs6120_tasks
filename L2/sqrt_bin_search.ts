var x: bigint = 64n;

//min_guess is leq, max_guess is gt
function sqrt_bin_search(x: bigint, min_guess: bigint, max_guess: bigint) {
    let min_plus_1: bigint = min_guess + 1n;
    if(min_plus_1 == max_guess){
        console.log(min_guess);
        return;
    }
    let sum_bounds: bigint = min_guess + max_guess;
    let mid: bigint = sum_bounds / 2n;
    let mid_squared: bigint = mid * mid;
    if(mid_squared <= x){
        sqrt_bin_search(x, mid, max_guess)
    }
    else{
        sqrt_bin_search(x, min_guess, mid)
    }
}

sqrt_bin_search(x, 0n, x);
