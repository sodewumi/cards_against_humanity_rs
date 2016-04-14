var _ = require("./underscore-min")

function GameRoom() {

    var usersArray = {
        "one": undefined,
        "two": undefined,
        "three": undefined,
        "four": undefined
    };

    var getAvailableUserSlot = function() {
        for (var key in usersArray) {
            if (usersArray[key] == undefined) {
                return key;
            } else {
                return undefined;
            }
        }

    }

    this.users = function() {
        var str = JSON.stringify(usersArray);
        return str;
    }

    this.addUser = function addUser(userId) {
        if _.size.userArray === 4 {
            //notify that game room is full
        } else {
            usersArray[getAvailableUserSlot()] = userId;
            //notify firebase
        }

    };

    this.removeUser = function removeUser(userId) {
        usersArray[userId] = undefined;
        //notify firebase
    };

}

// example usage
var newGameRoom = new GameRoom();
newGameRoom.addUser(1); // alerts "my method"
console.log(newGameRoom.users())
newGameRoom.removeUser(1); // alerts "my other method"
console.log(newGameRoom.users())