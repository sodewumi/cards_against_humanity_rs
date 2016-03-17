# Created by randall and stella at 3/9/16

Feature: Sign Up
  As a user
  I want to create a new room
  So I can create a new game


  Feature: Login In
  As a user
  I want to create a new room
  So I can create a new game

  Scenario: Login as unregistered user
    Given I am an unregistered user
    When I enter my credentials
    Then I should be redirected to the login page

  Scenario: Successful Login as registered user
    Given I am a registered user
    When I enter my credentials correctly
    Then I should be logged in successfully

  Scenario: Unsuccesful Login as registered user
    Given I am a registered user
    When I enter my credentials incorrectly
    Then I should be redirected to the login page


Feature: Create Room
  As a user
  I want to create a new room
  So I can create a new game

  Scenario: Create new room as unregistered user
    Given I am an unregistered user
    When I try to create a new room
    Then I should be redirected to sign up page

  Scenario: Create new room a registered user
    Given I am a registered user
    When I try to create a new room
    Then There should be a new room
    And I should be a room member


Feature: Send game invite
  As a user
  I want to send an invite to another user
  So they can join my room

  Scenario: Invitee is currently in room
    Given I am a logged in user
    And I have created a room
    And I am the room master
    And invitee is already in room
    When I try to send invitee a game invite
    Then I should see that user is already in room

  Scenario: Invitee is not currently in room
    Given I am a logged in user
    And I have created a room
    And I am the room master
    And invitee is not already in room
    When I try to send invitee a game invite
    Then I invitee should receive invite

  Scenario: Room is full
    Given I am a logged in user
    And I have created a room
    And I am the room master
    And Room is already full
    When I try to send invitee a game invite
    Then I should be notified that room is already full

  Scenario: Room is not full
    Given I am a logged in user
    And I have created a room
    And I am the room master
    And Room is not already full
    And invitee is not already in room
    When I try to send invitee a game invite
    Then I invitee should receive invite


Feature: Respond to game invite
  As a user
  I want to send an invite to another user
  So they can join my room

  Scenario: User accepts invite and room is full
    Given I am a registered User
    And I have been sent an invite
    And The Room is already full
    When I acept the invite
    Then I will recieve a rejection

  Scenario: User accepts invite and room has open slot
    Given I am a registered User
    And I have been sent an invite
    And The Room has an open slot
    When I acept the invite
    Then I will join the room

  Scenario: User accepts invite and is already in room
    Given I am a registered User
    And I have been sent an invite
    And I am already in the room
    When I acept the invite
    Then nothing will happen


Feature: Create Game
  As a room master
  I want to create a new room
  So That I can create a new game

  Scenario: Room Master not currently in game
    Given I am the room master
    And there is currently not a game
    When I create a new game
    Then a new game is created

  Scenario: Room Master currently in finished game
    Given I am the room master
    And a game has finished
    When I create a new game
    Then a new game is created


Feature: Deal Initial Game Hands
  As a player
  I want to initialize player's hands
  So That we can play a game

  Scenario: Player has no cards in hand
    Given I am the player
    And I currently have 0 cards in Hand
    When the game starts
    Then I should be given 10 cards


Feature: Replenish Game Deck
  As the player
  I want to replenish the deck
  So that game play can continue

  Scenario: Game deck is full
    Given I am the deck is full
    When a check occurs to replenish deck
    Then deck is not replenished

  Scenario: Game deck is less than full
    Given I am the deck is less than full
    When a check occurs to replenish deck
    Then deck is replenished


Feature: Shuffle Game Deck
  As the player
  I want to shuffle the game deck
  So that card order is random

  Scenario: Shuffle game deck
    Given I have an ordered deck
    When I shuffle the deck
    Then the deck's order should be different


Feature: Create new Game Round
  As the player
  I want to create a new game round
  So that players can keep playing

  Scenario: Previous round has ended
    Given the previous round has ended
    And more than three users are in the game
    When I create a new game round
    Then a new round is created


Feature: Play Round Hand
  As the player
  I want to play my hand
  So that the judge can choose a winner

  Scenario: All players have already played their cards for the round
    Given I am the last player who hasn't played this round's hand
    When I play my hand this round
    Then The judge is prompted to choose a winner

  Scenario: All players have not already played their cards for the round
    Given one or more other players have not played this round's hand
    When I play my hand
    Then the round will wait for all the other players to play their hands
    And judge cannot select winner


Feature: Update Player Score
  As the player
  I want to keep track of each players score
  So that I know who is currently winning

  Scenario: Player wins round
    Given that a player plays the winning hand
    When the judge chooses them
    Then all players should see their updated score

  Scenario: Player looses round
    Given that a player plays the losing hand
    When the judge does not choose them
    Then all players should see their updated score


Feature: Declare Round Winner
  As a judge
  I want to declare a round winner
  So that we can move to the next round

  Scenario: Judge chooses winner
    Given all players have played hand for round
    When the judge chooses a winner
    Then the winnner should know they are the winner
    And all the other players should know who the winner is
    And a new round should be created
    And the new round should have a judge
    And I should not be the judge of the new round


Feature: Replenish Player Hand
  As a player
  I want to get new card(s)
  So that I always have 10 cards

  Scenario: Player has less than ten cards in hand
    Given I am a player
    And I have less than ten cards in hand
    When hands are replenished
    Then I should have ten cards in hand

  Scenario: Player has ten or more cards in hand
    Given I am a player
    And I have ten or more cards in hand
    When hands are replenished
    Then I should have the same ten cards in hand


Feature: Declare Game Winner

  Scenario: Player has won required number of rounds
    Given All players have played this round's hand
    And I am one more point away from winning the game
    When The judge declares me as the round winner
    Then I am the winner of the game
    And all players should be notified that I am the winner
    And the game should be ended.


Feature: Prompt Game Restart

  Scenario: Master User chooses to restart game
    Given there are more than three players in the game
    And the master user chooses to play again
    When the game has ended
    Then Another Game is created

  Scenario: Master User does not choose to restart game
    Given the master user chooses not to play again
    When the game has ended
    Then the game is deleted
    And the room is deleted
    And the players can never come back to that room
    And the users can never be those players
