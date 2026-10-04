# blackjack-cli

terminal blackjack. the game logic is separate from the input and output, so it's reusable.

```
python blackjack.py
python test_blackjack.py
```

- start with 500 chips
- blackjack pays 3:2
- dealer stands on 17
- the deck reshuffles when it runs out

## reusing the engine

`hand_value`, `is_blackjack`, `dealer_play` and `settle` have no printing or input in them, so a discord bot can import them and handle the buttons itself.
