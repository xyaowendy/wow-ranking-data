const path = require('path');
const express = require("express");
const mongoose = require('mongoose');
const {Schema} = require("mongoose");

const PORT = process.env.PORT || 3001;

const app = express();

// connect to mongo db
main().catch(err => console.log(err));

async function main() {
    await mongoose.connect('mongodb+srv://admin:oo4KBdt7tSjF2ADr@mycluster.mbzbjc0.mongodb.net/wowdb?retryWrites=true&w=majority');
}


const connection = mongoose.connection;

let players = []

connection.on('error', console.error.bind(console, 'connection error:'));
connection.once('open', async function () {

    const collection  = connection.db.collection("user");
    collection.find({}).toArray(function(err, data){
        if(err) {
            console.log(err);
        } else {
            players = data;
        }
    });
});


// Have Node serve the files for our built React app
app.use(express.static(path.resolve(__dirname, '../client/build')));

// Handle GET requests to /api route
app.get("/api", (req, res) => {
    res.json(players);
});

// All other GET requests not handled before will return our React app
// app.get('*', (req, res) => {
//     res.sendFile(path.resolve(__dirname, '../client/build', 'index.html'));
// });

app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
});