#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from blackjack import CARDS, DEALER_TURN, HIT, PLAYER_TURN, STICK, A, choice


class Env:
    def __init__(self):
        self.dealer_showing = choice(CARDS)
        self.dealer_cards = [self.dealer_showing, choice(CARDS)]
        self.player_cards = random.sample(CARDS, k=2)
        self.turn = PLAYER_TURN  # player starts, dealer ends
        self.done = False

    def _bust(self):
        return sum(self.player_cards
                   ) > 21 if self.turn == PLAYER_TURN else sum(self.dealer_cards) > 21

    def __call__(self, a):

        player_total = sum(self.player_cards)
        dealer_total = sum(self.dealer_cards)

        if a == STICK:
            if self.turn == PLAYER_TURN:
                self.turn = DEALER_TURN
                reward = 0
            elif self.turn == DEALER_TURN:
                # check for bust on hits
                assert player_total <= 21 and dealer_total <= 21

                if player_total == dealer_total:
                    reward = 0
                else:
                    reward = 1 if player_total > dealer_total else -1
                self.done = True
            else:
                raise ValueError

        elif a == HIT:
            if self.turn == PLAYER_TURN:
                self.player_cards.append(choice(CARDS))
                reward = -1 if self._bust() else 0
                self.done = self._bust()

            elif self.turn == DEALER_TURN:
                self.dealer_cards.append(choice(CARDS))
                reward = 1 if self._bust() else 0
                self.done = self._bust()
        else:
            raise ValueError('expected HIT or STICK')

        state = ((player_total, self.dealer_showing, dealer_total), self.turn)

        return state, reward, self.done
