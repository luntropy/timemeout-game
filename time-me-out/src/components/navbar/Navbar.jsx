import React from "react";
import {
  Link
} from "react-router-dom";

const Navbar = (props) => (
  <nav className="navbar navbar-expand-lg navbar-light bg-light">
    <div>
      <ul className="navbar-nav">
        <li className="nav-item">
          <div className="restart" onClick={() => props.newGame()}>
            Restart Game
          </div>
        </li>
        <li className="nav-item">
        <Link to="/">Back To Home</Link>
        </li>
      </ul>
    </div>
  </nav>
);

export default Navbar;
