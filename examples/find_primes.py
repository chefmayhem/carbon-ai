import sys
sys.path.append('../carbon_ai')
from carbon_ai import CarbonAI
import logging

cai_instance = CarbonAI()
@cai_instance.evaluate_impact
def find_primes_eval(n1, n2):
    primes = []
    for num in range(n1, n2 + 1):
        if num > 1:
            for i in range(2, int(pow(num, 0.5)) + 1):
                if (num % i) == 0:
                    break
            else:
                primes.append(num)
    return primes

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(find_primes_eval(400, 500))
