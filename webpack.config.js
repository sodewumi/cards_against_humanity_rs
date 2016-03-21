var rootAssetPath = './static';
// var webpack = require("webpack");

process.stdout.write(__dirname)
module.exports = {
    context: __dirname,
    entry: "./static/js/example.js",

    output: {
        path: __dirname + "/static/build",
        filename: "bundle.js",
    },
    module: {

    },
};