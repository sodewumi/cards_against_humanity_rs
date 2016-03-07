var _ = require("./underscore-min")

function Round(_gameId, _judge) {

    var gameId = _gameId
    var judge = _judge;
    var winner = undefined;
    var blackCard = undefined;

    var whiteCardsArray = {
        "one": {},
        "two": {},
        "three": {},
        "four": {}
    };

    this.addPick = function addPick(player, pickNo, cardId) {
        if whiteCardsArray[player][pickNo] != undefined {
            temp = whiteCardsArray[player][pickNo];
            //return card to player's hand
            //notify firebase
        }
        whiteCardsArray[player][pickNo] = cardId;
        //notify firebase
    };

    this.makeJudgement = function makeJudgement(judge, winner) {
        //check that judge is correct for this round
        //declare winner
        //notify firebase
    };

}