from enum import Enum
import random


class CardType(Enum):
    Nine = 0,
    Ten = 10,
    Jack = 2,
    Queen = 3,
    King = 4,
    Ace = 11, 


class CardSuit(Enum):
    Club = 0, # ♣
    Diamond = 1, # ♦
    Heart = 2, # ♥
    Spade = 3  # ♠


class Announce(Enum):
    No_one = 0
    Twenty = 20
    Forty = 40


class PlayerPosition(Enum):
    no_one = 0
    first_player = 1
    second_player = 2


class Card:
    def __init__(self, card_type, card_suit):
        self.card_type = card_type
        self.card_suit = card_suit

    def get_value(self):
        for types in CardType:
            if types == self.card_type:
                return CardType.types.value

    
class Deck:
    def __init__(self):
        self.cards = [Card(card_type, card_suit) for card_type in CardType for card_suit in CardSuit]
        random.shuffle(self.cards)
        self.trump_card = self.cards[0]


    def get_next_card(self):
        if len(self.cards) == 0:
            raise ExceptionEmptyDeck()
        return self.cards.pop()

    
    def change_trump(self, new_card):
        self.trump_card = new_card
        self.cards[0] = new_card

    def get_trump(self):
        return self.trump_card

    def get_count_cards(self):
        return len(self.cards)


class PlayerTurnContext:
    pass


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.announce = []        

    def start_round(round_cards, trump_card, my_total_points, opponent_total_points):
        self.cards = list(round_cards)

    def add_card(card):
        self.cards.append(card)

    def get_turn(context):
        pass


class GameHand:
    def __init__(self, who_will_play_first, first_player, second_player, current_state):
        self.first_player = first_player
        self.second_player = second_player
        self.current_state = current_state
        self.first_card  #
        self.second_card  #
        self.winner #=    
        self.first_player_announce 
        self.second_player_announce
        self.closed_by_player
        self.who_will_play_first = who_will_play_first

    def start(self):
        first_to_play = self.first_player
        second_to_play = self.second_player
        if self.who_will_play_first == PlayerPosition.second_player:
            first_to_play = self.second_player
            second_to_play = self.first_player
        #prepare PlayerTurnContext
        firstToPlayTurn = first_to_play.get_turn(PlayerTurnContext())
        #turn == close -> close, ask ,first
        #turn = change_trump -> change, ask, first


class Round:
    def __init__(self, first_player, second_player, who_will_play_first):
        self.deck = Deck()

        self.first_player = first_player
        self.points_player1 = 0
        self.first_player_cards_in_hand = []
        self.first_player_cards_collected = []

        self.second_player = second_player        
        self.points_player2 = 0
        self.second_player_cards_in_hand = []
        self.second_player_cards_collected = []

        self.has_hand_player1 = False
        self.has_hand_player2 = False

        self.last_won_hand = PlayerPosition.no_one

        self.who_will_play_first = who_will_play_first
        self.closed_by_player = PlayerPosition.no_one

        self.current_state = Start(self)

    def start(self):
        self.deal_first_cards()
        while self.is_finished() == False:
            self.play_hand()
    
    def play_hand(self):
        new_hand = GameHand(self.who_will_play_first, self.first_player, self.second_player, self.current_state)
        new_hand.start()

        # update points
        self.update_points(new_hand)

        #winner take both cards
        if new_hand.winner == PlayerPosition.first_player:
            self.first_player_cards_collected.append(new_hand.first_card)
            self.first_player_cards_collected.append(new_hand.second_card)
        else:
            self.second_player_cards_collected.append(new_hand.first_card)
            self.second_player_cards_collected.append(new_hand.second_card)
        
        self.who_will_play_first = new_hand.winner

        self.first_player_cards_in_hand.remove(new_hand.first_card)
        self.second_player_cards_in_hand.remove(new_hand.second_card)

        if self.current_state.should_take_card:
            if self.who_will_play_first == PlayerPosition.first_player:
                self.give_card_first_player()
                self.give_card_second_player()                
            else:
                self.give_card_second_player()
                self.give_card_first_player()

        self.current_state.play_hand(self.deck.get_count_cards())

        if hand.closed_by_player == PlayerPosition.first_player or hand.closed_by_player == PlayerPosition.second_player:
            self.current_state.close()
            self.closed_by_player = hand.closed_by_player
        

    def is_finished(self):
        if self.points_player1 >= 66 or self.points_player2 >= 66:
            return True
        if len(self.first_player_cards_in_hand) == 0 and len(self.second_player_cards_in_hand) == 0:
            return True
        return False

    def set_state(self, new_state):
        self.current_state = new_state


    def deal_first_cards(self):
        for i in range(3):
            self.give_card_first_player()
        for i in range(3):
            self.give_card_second_player()
        for i in range(3):
            self.give_card_first_player()
        for i in range(3):
            self.give_card_second_player()
    
    def give_card_first_player(self):
        card = self.deck.get_next_card()       
        self.first_player.add_card(card)
        self.first_player_cards_in_hand(card)

    def give_card_second_player(self):
        card = self.deck.get_next_card()            
        self.second_player.add_card(card)
        self.second_player_cards_in_hand(card)

    def update_points(self, hand):
        points = hand.first_card.get_value() + hand.second_card.get_value()
        if hand.winner == PlayerPosition.first_player:
            self.points_player1 += points
        else:
            self.points_player2 += points
        self.points_player1 += hand.first_player_announce.value
        self.points_player2 += hand.second_player_announce.value


class Game:
    def __init__(self, first_player, second_player, who_will_play_first):
        self.first_player = first_player
        self.first_player = second_player
        self.total_point1 = 0
        self.total_point2 = 0
        self.finished = False
        self.current_player = first_player
        self.who_will_play_first = who_will_play_first
    
    def start(self):
        while self.is_finished() == False:
            self.play_round()
    
    def play_round(self):
        new_round = Round(self.first_player, self.second_player, self.who_will_play_first)
        new_round.start()
        if new_round.closed_by_player == PlayerPosition.first_player:
            if new_round.total_point1 < 66:
                self.total_point2 += 3
                self.who_will_play_first = PlayerPosition.first_player
                return
        if new_round.closed_by_player == PlayerPosition.second_player:
            if new_round.total_point2 < 66:
                self.total_point1 += 3
                self.who_will_play_first = PlayerPosition.second_player
                return

        if new_round.points_player1 < 66 and new_round.points_player2 < 66:
            if new_round.last_won_hand == PlayerPosition.first_player:
                self.total_point1 += 1
                self.who_will_play_first = PlayerPosition.second_player
                return
            else:
                self.total_point2 += 1
                self.who_will_play_first = PlayerPosition.first_player
                return

        if new_round.points_player1 > new_round.points_player2:
            if new_round.points_player2 >= 33:
                self.total_point1 += 1
                self.who_will_play_first = PlayerPosition.second_player
            elif new_round.has_hand_player2:
                self.total_point1 += 2
                self.who_will_play_first = PlayerPosition.second_player
            else:
                self.total_point1 += 3
                self.who_will_play_first = PlayerPosition.second_player
        elif new_round.points_player1 < new_round.points_player2:
            if new_round.points_player1 >= 33:
                self.total_point2 += 1
                self.who_will_play_first = PlayerPosition.first_player
            elif new_round.has_hand_player1:
                self.total_point2 += 2
                self.who_will_play_first = PlayerPosition.first_player
            else:
                self.total_point2 += 3
                self.who_will_play_first = PlayerPosition.first_player
        else:
            if new_round.last_won_hand:
                self.total_point1 += 1
                self.who_will_play_first = PlayerPosition.second_player
            else:
                self.total_point2 += 1
                self.who_will_play_first = PlayerPosition.first_player

    def is_finished(self):
        return self.total_point1 >= 11 or self.total_point2 >= 11


#game_states
class Start:
    def __init__(self, round):
        self.round = round

    def can_announce_20_40(self):
        return False

    def can_close(self):
        return False

    def can_change_trump(self):
        return False

    def should_observe_rules(self):
        return False

    def should_take_card(self):
        return True

    def play_hand(self, cards_left_deck):
        self.round.set_state(MoreThanTwoCardsLeftState(self.round))

    def close(self):
        if self.can_close():
            self.round.set_state(FinalState(self.round))


class MoreThanTwoCardsLeftState:
    def __init__(self, round):
        self.round = round

    def can_announce_20_40(self):
        return True

    def can_close(self):
        return True

    def can_change_trump(self):
        return True

    def should_observe_rules(self):
        return False

    def should_take_card(self):
        return True

    def play_hand(self, cards_left_deck):
        if cards_left_deck == 2:
            self.round.set_state(TwoCardsLeftState(self.round))

    def close(self):
        if self.can_close():
            self.round.set_state(FinalState(self.round))

  
class TwoCardsLeftState:
    def __init__(self, round):
        self.round = round

    def can_announce_20_40(self):
        return True

    def can_close(self):
        return False

    def can_change_trump(self):
        return False

    def should_observe_rules(self):
        return False

    def should_take_card(self):
        return True

    def play_hand(self, cards_left_deck):
        self.round.set_state(FinalState(self.round))

    def close(self):
        if self.can_close():
            self.round.set_state(FinalState(self.round))


class FinalState:
    def __init__(self, round):
        self.round = round

    def can_announce_20_40(self):
        return True

    def can_close(self):
        return False

    def can_change_trump(self):
        return False

    def should_observe_rules(self):
        return True

    def should_take_card(self):
        return False

    def play_hand(self, cards_left_deck):
        pass

    def close(self):
        if self.can_close():
            self.round.set_state(FinalState(self.round))


class PlayerTurnContext:
    pass
    

class ExceptionEmptyDeck(Exception):
    pass    
