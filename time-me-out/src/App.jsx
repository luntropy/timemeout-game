import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Login from "./components/login/Login";
import Create_room from "./components/create-game/Create_game";
import Registration from "./components/registration/Registration";
import Game from "./components/game/Game";
import Rooms from "./components/rooms/Rooms";

export default function App() {
  return (
    <Router>
      <Switch>
        <Route path="/" component={Login} exact />
        <Route path="/register" component={Registration} />
        <Route path="/create" component={Create_room} />
        <Route
          path="/game/:gameId"
          render={(props) => {
            return <Game {...props} />;
          }}
        />
        <Route path="/rooms" component={Rooms} />
      </Switch>
    </Router>
  );
}
