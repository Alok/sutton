# ch 1 exercises

1.  Unless both got stuck in absorbing policies, they'd improve. I think
    they could end up just learning to beat each other but not play
    optimally. Seeding multiple players may help.
2.  Could manually tweak to treat symmetric states the same. But if the
    opponent doesn't use symmetry, then the states are not the same from
    the perspective of maximizing rewards.
3.  It may never learn a new strategy as the opponent improves.
4.  Why are the state values probabilities?

Optimizing return may not always be best because it ignores variance,
which is analogous to *risk*. High risk, high reward may not always be
best.
