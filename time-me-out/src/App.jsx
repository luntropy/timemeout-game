import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Login from "./components/login/Login";
import Registration from "./components/registration/Registration";
import Game from "./components/game/Game";
import Rooms from "./components/rooms/Rooms";
import Over from "./components/game/Over"

export default function App() {
  return (
    <Router>
      <Switch>
        <Route path="/" component={Login} exact />
        <Route path="/register" component={Registration} />
        <Route
          path="/game/:gameId"
          render={(props) => {
            return <Game {...props} />;
          }}
        />
        <Route path="/rooms" component={Rooms} />
        <Route path="/end" component={Over} />
      </Switch>
    </Router>
  );
}
