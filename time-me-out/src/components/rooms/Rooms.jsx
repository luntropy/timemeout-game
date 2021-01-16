import React, { useState, useEffect } from 'react'
import {
    useHistory,
    Link
} from "react-router-dom";

const Rooms = () => {
    const history = useHistory()

    const [rooms, setRooms] = useState([])
    const [error, setError] = useState(false)

    const fetchData = () => fetch('https://127.0.0.1:5000/list_games')
          .then(res=>res.json()).then(res => setRooms(res.rooms_list)); 

    useEffect(() => {
        fetchData();
      }, []);

    const onClick = (id) => {
        const userId = sessionStorage.getItem('userId')
        fetch('https://127.0.0.1:5000/connect_to_game', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({ guest_id: userId, room_id: id }),
      }).then(res=>res.json()).then(res =>
        res.room_data_json ? history.push(`/game/${id}`) : setError(true)
      )
    }

    return (
        <>
        <Link to='/create'>Create room</Link><br />
        <button onClick={fetchData}>Refresh</button>
        <ul>
        {rooms.map(r => <li>{<button onClick={() => onClick(r)}>Join Room: {r}</button>}</li>)}
        </ul>
        {error && <p>Error joining!</p>}
        </>
    )
}

export default Rooms