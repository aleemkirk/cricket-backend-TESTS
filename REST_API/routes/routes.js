var faker = require("faker");
var sql = require("mssql");

const config = {
    user: "root",
    password: "",
    server: "localhost",
    database: "cricket_player_profiles"
}

var appRouter = function(app){

    app.get("/", function(req, res){
         
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