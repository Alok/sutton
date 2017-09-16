#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

ITERS = int(1e5)
TOTALS = range(1, 22)
CARDS = range(1, 11)

S = {player_total for player_total in TOTALS}

STICK = 0
HIT = 1
A = {STICK, HIT}


def choice(x):
    return random.sample(x, 1)[0]


class Table(dict):
    def __init__(self, *x):
        super().__init__(*x)

    def __call__(self, *x):
        if len(x) == 1:
            return self[x[0]]
        if len(x) == 2:
            return self[(x[0][0], x[0][1]), x[1]]
        elif len(x) == 3:
            return self[(x[0], x[1]), x[2]]
        else:
            raise ValueError('value not found')


class Policy(Table):
    def __init__(self, *x):
        super().__init__(*x)

    def __call__(self, *x):
        if len(x) == 1:
            if isinstance(x[0], int):
                return self[x[0]]
            else:
                return self[x[0][0]]
        elif len(x) == 2:
            return self[(x[0], x[1])]


# init Q with 0 starting
Q = Table({(s, a): 0 for s in S for a in A})
pi = Policy({s: HIT for s in S})


def argmax(q, s):
    return max((a for a in A), key=lambda a: q(s, a))


def eps_greedy(q, s, eps=.05):
    return choice(A) if random.random() < eps else argmax(q, s)


# stick on 20 or 21
player = Policy({total: HIT if total < 20 else STICK for total in TOTALS})
dealer = Policy({total: HIT if total < 17 else STICK for total in TOTALS})

PLAYER_TURN = 'player turn'
DEALER_TURN = 'dealer turn'


def update(q, states, actions):
    pairs = list(zip(states, actions))

    def update_entry(q, s, a):
        try:
            i = pairs.index((s, a))
            rets = sum(rewards[i:])
            n = len(pairs[i:])
            if n == 0 or n == 1:
                pass

            q[s, a] = (1 / n) * q[s, a] + (1 - 1 / n) * rets
            return q
        except ValueError:
            # if not found just leave it at 0
            pass

    for s in S:
        for a in A:
            update_entry(q, s, a)
    return q


if __name__ == '__main__':

    from env import Env
    for iter in range(ITERS):

        states = []
        actions = []
        rewards = []

        env = Env()

        s = choice(S)
        # Ignore first state since it messes with the length of the lists and isn't in our control.
        # states.append(s)

        # a = eps_greedy(Q, s)
        a = player(s)
        actions.append(a)

        s, r, done = env(a)
        ((player_total, dealer_total), turn) = s

        states.append(player_total)
        rewards.append(r)

        while not done:

            if turn == PLAYER_TURN:
                s = player_total
                a = player(s)
            elif turn == DEALER_TURN:
                s = dealer_total
                a = dealer(s)
            actions.append(a)

            s, r, done = env(a)

            ((player_total, dealer_total), turn) = s

            states.append(player_total)
            rewards.append(r)
            update(Q, states, actions)
