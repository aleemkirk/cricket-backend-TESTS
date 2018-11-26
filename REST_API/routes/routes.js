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

    app.get("/players", function(req, res){
        connection.query('SELECT `name` from `players`', function(err, rows, fields){
            if(err) throw err;
            res.status(200).send(JSON.stringify({player_names: rows}));
        });
    });

    app.get("/player/:num", function(req, res){
        var index = req.params.num;
        if(isFinite(index) && index >=0){
            connection.query('SELECT * FROM `players` ORDER BY `id` LIMIT 1 OFFSET '+ index +';', function(err, row, fields){
                if(err) throw err;
                res.status(200).send(JSON.stringify({player: row}))

            });
        }else{res.status(404).send({'error message': "enter valid number"});}

    });

    

    // app.get("/user", function(req, res){
    //     var data = ({
    //         firstName: faker.name.firstName(),
    //         lastName: faker.name.lastName(),
    //         userName: faker.internet.userName(),
    //         email: faker.internet.email()
    //     });
    //     res.status(200).send(data);
    // });

    // app.get("/user/:num", function(req, res){
    //     var users = [];
    //     var num = req.params.num;

    //     if(isFinite(num) && num > 0){
    //         for(i =0; i <= num-1; i++){
    //             users.push({
    //                 firstName: faker.name.firstName(),
    //                 lastName: faker.name.lastName(),
    //                 userName: faker.internet.userName(),
    //                 email: faker.internet.email()
    //             });
    //         }
            
    //         res.status(200).send({info: users});

    //     } else{
    //         res.status(400).send({message: 'invalid number supplied'});
    //     }
    // });

}

module.exports = appRouter;