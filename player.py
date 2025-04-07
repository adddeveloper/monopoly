import gameboard
import gamesquare
import observer


class Player:
    """Player class to represent a player in the game"""
    def __init__(self, name, money, token):
        # ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 3 | Token
        self.__token = token
        # ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 3 | Token
        # ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 1 | Jail
        self.__in_jail = False
        self.__turns_in_jail = 0
        self.__get_out_of_jail_free_cards = 0
        # ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 1 | Jail
        """Constructor for the Player class"""
        self.__name = name
        self.__money = money
        self.__properties = []
        self.__board_position = 0
        self.__doubles_count = 0
        self.__bankrupt_declared = False
        self.__utility_count = 0
        self.__railroad_count = 0
        self.__luck = 0

        self.__mortgaging_order = []
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 3 | Token
    @property
    def token(self):
        return self.__token
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 3 | Token
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 1 | Jail 
    def send_to_jail(self):
        self.__in_jail = True
        self.__turns_in_jail = 0
        self.__board_position = 10

    def attempt_jail_escape(self, dice1, dice2):
        if dice1 == dice2:
            self.__in_jail = False
            self.__turns_in_jail = 0
            return True
        self.__turns_in_jail += 1
        return False

    def pay_to_get_out_of_jail(self):
        if self.__money >= 50:
            self.__money -= 50
            self.__in_jail = False
            self.__turns_in_jail = 0
            return True
        return False

    def use_get_out_of_jail_card(self):
        if self.__get_out_of_jail_free_cards > 0:
            self.__get_out_of_jail_free_cards -= 1
            self.__in_jail = False
            self.__turns_in_jail = 0
            return True
        return False
    
    @property
    def in_jail(self):
        return self.__in_jail

    @property
    def turns_in_jail(self):
        return self.__turns_in_jail

    @property
    def get_out_of_jail_free_cards(self):
        return self.__get_out_of_jail_free_cards

    @get_out_of_jail_free_cards.setter
    def get_out_of_jail_free_cards(self, count):
        self.__get_out_of_jail_free_cards = count
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 1 | Jail

    def __str__(self):
        """String representation of the player"""
        # ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 3 | Token
        return f"{self.__token} {self.__name} - {self.money} - {self.net_worth()} luck:{self.__luck:.1f}"
        # ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 3 | Token
    def buy_property(self, board_property):
        """Function to attempt to buy a property"""
        if not board_property.can_be_purchased():
            return False

        self.__properties.append(board_property)
        self.__money -= board_property.price
        board_property.owner = self
        if board_property.is_utility:
            self.__utility_count += 1
        if board_property.is_railroad:
            self.__railroad_count += 1

        return True

    def pay_rent(self, square, dice_sum):
        """Function to attempt to pay rent or tax on a square"""
        if square.owner is self:
            return 0
        rent = square.calculate_rent_or_tax(dice_sum)
        self.__money -= rent

        if square.owner is not None:
            square.owner.money += rent
        return rent

    def mortgage_property(self, deed_name):
        """Function to mortgage a property"""
        for p in self.__properties:
            if p.name == deed_name:
                res = p.mortgage()
                if res:
                    self.__mortgaging_order.append(p)
                return True
        return False

    def unmortgage_property(self):
        """Function to unmortgage a property
        return the name of the property that was unmortgaged
        or the empty string if no such property exists"""
        if len(self.__mortgaging_order) == 0:
            return ""
        p = self.__mortgaging_order.pop(0)
        res = p.unmortgage()
        if not res:
            return ""
        return p.name


    def net_worth(self):
        """Function to calculate the net worth of the player"""
        return self.money + sum(p.price for p in self.__properties)

    def collect(self, amount):
        """Function to collect money"""
        self.__money += amount

    def move(self, spaces):
        """Function to move the player on the board"""
        prior_position = self.__board_position
        self.__board_position += spaces
        if self.__board_position >= 40:
            self.__board_position -= 40
        # careful about passing go
        if self.__board_position < prior_position:
            observer.Event("update_state", "pass_go +200")
            self.collect(200)

    @property
    def doubles_count(self):
        return self.__doubles_count

    @doubles_count.setter
    def doubles_count(self, doubles_count):
        self.__doubles_count = doubles_count

    @property
    def luck(self):
        return self.__luck

    @luck.setter
    def luck(self, luck):
        self.__luck = luck

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, money):
        self.__money = money

    @property
    def name(self):
        return self.__name

    @property
    def position(self):
        return self.__board_position

    @property
    def bankrupt_declared(self):
        return self.__bankrupt_declared

    def declare_bankrupt(self):
        self.__bankrupt_declared = True

    @property
    def railroad_count(self):
        return self.__railroad_count

    @property
    def properties(self):
        return self.__properties

    @property
    def deed_names(self):
        return [p.name for p in self.__properties]