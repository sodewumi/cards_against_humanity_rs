function Game() {

    var blackDeck = {};
    var whiteDeck = {};
    var discardedBlack = {};
    var discardedWhite = {};

    var rounds = {};

    var scoresArray = {
        "one": 0,
        "two": 0,
        "three": 0,
        "four": 0
    };


    var playersArray = {
        "one": undefined,
        "two": undefined,
        "three": undefined,
        "four": undefined
    };

    var getAvailablePlayerSlot = function() {
        for (var key in playersArray) {
            if (playersArray[key] == undefined) {
                return key;
            } else {
                return undefined;
            }
        }

    }

    this.players = function() {
        var str = JSON.stringify(playersArray);
        return str;
    }

    this.addPlayer = function addPlayer(playerId) {
        if _.size.playerArray === 4 {
            //notify that game room is full
        } else {
            playersArray[getAvailablePlayerSlot()] = playerId;
            //notify firebase
        }

    };

    this.removePlayer = function removePlayer(playerId) {
        playersArray[playerId] = undefined;
        //notify firebase
    };

}