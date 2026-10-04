#!/usr/bin/env python3
"""blackjack: terminal game. the engine has no I/O, so it can be reused elsewhere."""
import random

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["S", "H", "D", "C"]


def card_value(rank: str) -> int:
    if rank == "A":
        return 11
    if rank in ("J", "Q", "K"):
        return 10
    return int(rank)


def hand_value(cards: list) -> int:
    """best total for a hand. aces drop from 11 to 1 as needed."""
    total = sum(card_value(r) for r, _ in cards)
    aces = sum(1 for r, _ in cards if r == "A")
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def is_blackjack(cards: list) -> bool:
    return len(cards) == 2 and hand_value(cards) == 21


class Deck:
    def __init__(self, rng: random.Random = None):
        self.rng = rng or random.Random()
        self.cards = []
        self._rebuild()

    def _rebuild(self) -> None:
        self.cards = [(r, s) for r in RANKS for s in SUITS]
        self.rng.shuffle(self.cards)

    def draw(self) -> tuple:
        if not self.cards:
            self._rebuild()
        return self.cards.pop()


def dealer_play(deck: Deck, hand: list) -> list:
    """dealer draws until 17 or more, and stands on soft 17."""
    while hand_value(hand) < 17:
        hand.append(deck.draw())
    return hand


def settle(player: list, dealer: list, bet: int) -> int:
    """net coin change for the player. blackjack pays 3:2."""
    p, d = hand_value(player), hand_value(dealer)
    if p > 21:
        return -bet
    if is_blackjack(player) and not is_blackjack(dealer):
        return int(bet * 1.5)
    if is_blackjack(dealer) and not is_blackjack(player):
        return -bet
    if d > 21 or p > d:
        return bet
    if p < d:
        return -bet
    return 0


def show(cards: list) -> str:
    return " ".join(f"{r}{s}" for r, s in cards)


def ask_bet(chips: int) -> int:
    while True:
        raw = input(f"chips: {chips}. bet (or q to leave): ").strip().lower()
        if raw in ("q", "quit"):
            return 0
        if raw.isdigit() and 1 <= int(raw) <= chips:
            return int(raw)
        print("invalid bet.")


def play_round(deck: Deck, chips: int) -> int:
    """plays one round. returns the new chip total, or -1 if the player leaves."""
    bet = ask_bet(chips)
    if bet == 0:
        return -1
    player = [deck.draw(), deck.draw()]
    dealer = [deck.draw(), deck.draw()]

    print(f"\nyou:    {show(player)} ({hand_value(player)})")
    print(f"dealer: {show(dealer[:1])} ??")

    while not is_blackjack(player) and hand_value(player) < 21:
        move = input("[h]it or [s]tand? ").strip().lower()
        if move.startswith("h"):
            player.append(deck.draw())
            print(f"you:    {show(player)} ({hand_value(player)})")
        elif move.startswith("s"):
            break

    if hand_value(player) <= 21:
        dealer_play(deck, dealer)
    print(f"dealer: {show(dealer)} ({hand_value(dealer)})")

    change = settle(player, dealer, bet)
    verdict = "you win." if change > 0 else "you lose." if change < 0 else "push."
    print(f"{verdict} ({change:+d})\n")
    return chips + change


def main() -> None:
    deck = Deck()
    chips = 500
    print("blackjack. blackjack pays 3:2, dealer stands on 17.\n")
    while chips > 0:
        result = play_round(deck, chips)
        if result == -1:
            break
        chips = result
    print(f"you leave with {chips} chips." if chips > 0 else "you're out of chips.")


if __name__ == "__main__":
    main()
