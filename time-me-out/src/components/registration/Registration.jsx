import React, { useState } from "react";
import { useHistory, Link } from "react-router-dom";

const Registration = () => {
  const history = useHistory();

  const [userVal, setUserVal] = useState("");
  const [passVal, setPassVal] = useState("");
  const [error, setError] = useState(false);

  const onClick = () =>
    fetch("http://127.0.0.1:5000/register_user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: userVal, password: passVal }),
    })
      .then((res) => res.json())
      .then((res) => {
        if (res.registration === 1) {
          sessionStorage.setItem("userId", res.player_id);
          history.push("/create");
        } else setError(true);
      });

  return (
    <div>
      <strong>Enter details:</strong>
      <br />
      <label>Username: </label>
      <br />
      <input
        type="text"
        value={userVal}
        onChange={(e) => setUserVal(e.target.value)}
        name="username"
      />
      <br />
      <label>Password: </label>
      <br />
      <input
        type="password"
        value={passVal}
        onChange={(e) => setPassVal(e.target.value)}
        name="password"
      />
      <br />
      <button onClick={onClick}>Register</button>
      <br />
      {error && <p>Error!</p>}
      <Link to="/">Already have an accout? Login</Link>
    </div>
  );
};

export default Registration;
