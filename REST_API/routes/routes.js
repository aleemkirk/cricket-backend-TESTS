var faker = require("faker");
var mysql = require("mysql");
var host_name = 'localhost'

var connection = mysql.createConnection({
    host: host_name,
    user: 'root',
    password: '',
    database: 'cricket_player_profiles'
});

var appRouter = function(app){

    //-->Get full list of player names from 'players' table
    app.get("/players", function(req, res){
        connection.query('SELECT `name` from `players`', function(err, rows, fields){
            if(err) throw err;
            res.status(200).send(JSON.stringify(rows));
        });
    });


    //-->Get player general information from 'players' table by using 'id' 
    app.get("/player/:info", function(req, res){
        var re = /^[A-Za-z_A-Za-z]+$/;
        var info = req.params.info;
        if(isFinite(info) && info >=0){ 
            connection.query('SELECT * FROM `players` ORDER BY `id` LIMIT 1 OFFSET '+ info +';', function(err, row, fields){
                if(err) {res.status(500).send({error: err});}
                else{res.status(200).send(JSON.stringify(row));}

            });
        }else if(re.test(info)){
            connection.query("SELECT * FROM `players` WHERE (`Name` = '" + info.replace('_', ' ') + "');", function(err, row, fields){
                if(err) {res.status(500).send({error: err});}
                else{res.status(200).send(JSON.stringify(row));}
            });
        }else{res.status(404).send({'error message': "enter valid player info"});}

    });

    //-->Get player match stats using player name
    app.get("/match_stats/:player_name", function(req, res){
        var re = /^[A-Za-z_A-Za-z]+$/;
        var name = req.params.player_name;
        if(re.test(name)){
            connection.query('SELECT * FROM '+name+';', function(err, table, fields){
                if(err){res.status(500).send({error: err});}
                else{res.status(200).send(JSON.stringify(table));}
            });
        }else{
            res.status(400).send({error:'invalid name'})
        }
    });

    //-->API for search functionality
    app.get("/player_search/:player_name", function(req, res){
        var re = /^[A-Za-z_A-Za-z]+$/;
        var name = req.params.player_name;
        const limit = 10; //how much result are returned
        if(re.test(name)){
            connection.query('SELECT * FROM `players` WHERE `Name` LIKE \'%'+name.replace('_', ' ')+'%\' LIMIT ' + limit +';', function(err, rows, fields){
                if(err){res.status(500).send({error:err})}
                else{
                    res.status(200).send(JSON.stringify(rows));
                }
            });
        }else{
            res.status(400).send({error:"invalid player name"})
        }
    });


}

module.exports = appRouter;