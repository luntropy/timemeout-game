import React from "react";
import "./navbar.css";

const Navbar = (props) => (
  <nav className="navbar navbar-expand-lg navbar-light bg-light">
    <div>
      <ul className="navbar-nav">
        <li className="nav-item">
          <div className="restart" onClick={() => props.newGame()}>
            Restart Game
          </div>
        </li>
      </ul>
    </div>
  </nav>
);

export default Navbar;
