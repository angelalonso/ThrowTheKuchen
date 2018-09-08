from flask import Flask
from flask_restful import Api, Resource, reqparse

statuses = [
        {
"gameStatus": "JustStarted"
}
        ]


class Status(Resource):

    def get(self, gameStatus):
        try:
            return statuses[0], 200
        except IndexError:
            return "No entries available at the moment", 500

    def post(self, gameStatus):
        # no post here, we update the one record we have instead
        #status = {
        #        "gameStatus": gameStatus
        #        }
        #statuses.append(status)
        #return status, 201
        returnstatus, returncode = self.put(gameStatus)
        return returnstatus, returncode


    def put(self, gameStatus):
        if gameStatus == "P1_Hit" or gameStatus == "P1_Missed":
            newGameStatus = "P2_Ready"
        elif gameStatus == "P2_Hit" or gameStatus == "P2_Missed":
            newGameStatus = "P1_Ready"

        statuses[0]["gameStatus"] = newGameStatus
        
        return statuses[0], 200

    def delete(self, gameStatus):
        global statuses
        statuses = []
        return "Game Status Entry deleted", 200


        

app = Flask(__name__)
api = Api(app)


api.add_resource(Status, "/<string:gameStatus>")
app.run(debug=True)
