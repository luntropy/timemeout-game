import React, { useState } from "react";
import { useHistory, Link } from "react-router-dom";

const Create_game = () => {
  const history = useHistory();

  const [visible, setVisible] = useState(false);
  const [value, setValue] = useState();
  const [error, setError] = useState(false);

  const onClick = () =>
    fetch("https://127.0.0.1:5000/create_game", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ host_id: "", field_size: 16, time_limit: value }),
    })
      .then((res) => res.json())
      .then((res) =>
        res.game_creation === 1
          ? history.push(`/game/${res.room_id}`)
          : setError(true)
      );

  return (
    <>
      <button onClick={() => setVisible(true)}>Create Room</button>
      <Link to="/rooms">Enter Room</Link>
      <br />
      {visible && (
        <>
          <div onChange={(e) => setValue(e.target.value)}>
            <input type="radio" value={40} name="length" /> 40 sec
            <input type="radio" value={60} name="length" /> 60 sec
            <input type="radio" value={90} name="length" /> 90 sec
          </div>
          <button onClick={onClick}>Create Game!</button>
        </>
      )}

      {error && <p>Error creating a room!</p>}
    </>
  );
};

export default Create_game;
