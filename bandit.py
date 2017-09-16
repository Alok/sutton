#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

import numpy as np

k = 10
ITERS = int(1e5)
Q = {a: 0 for a in range(k)}
seen = {a: 0 for a in range(k)}


def pure_greedy():
    return max(Q, key=Q.get)


def rand():
    return random.choice(list(Q.keys()))


def epsilon_greedy(epsilon=.1):
    return rand() if random.random() < epsilon else pure_greedy()


class Bandit():
    def _rewards(self, f=None):
        return {a: np.random.normal(loc=a)
                for a in range(k)} if f is None else {a: f(a)
                                                      for a in range(k)}

    def step(self, a):
        ''' return reward since state is constant'''
        seen[a] += 1
        return self._rewards()[a]


def update(a, r) -> None:
    n = seen[a]
    assert n > 0
    Q[a] = (1 - 1 / n) * Q[a] + (1 / n) * r


def main(policy=epsilon_greedy) -> None:
    env = Bandit()

    for i in range(ITERS):
        a = policy()
        r = env.step(a)
        update(a, r)
        if i % int(1e4) == 0:
            print(Q)


if __name__ == '__main__':
    main()
