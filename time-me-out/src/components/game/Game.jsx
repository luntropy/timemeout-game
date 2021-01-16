import React, { useState, useEffect } from "react";
import Board from "../board/Board";
import Over from "./Over";
import {
  Container,
  CssBaseline,
  Grid,
  Button,
  Typography,
  CircularProgress,
} from "@material-ui/core";
import { useHistory } from "react-router-dom";
import initializeDeck from "../../deck";

export default function Game() {
  const [cards, setCards] = useState([]);
  const [flipped, setFlipped] = useState([]);
  const [dimension, setDimension] = useState(600);
  const [solved, setSolved] = useState([]);
  const [disabled, setDisabled] = useState(false);
  const [score, setScore] = useState(0);
  const [combo, setCombo] = useState(1);
  const [loading, setLoading] = useState(true);
  const [counter, setCounter] = useState()
  const history = useHistory();

  const userId = sessionStorage.getItem("userId")
  const guestId = sessionStorage.getItem("guestId");
  const roomId = sessionStorage.getItem("roomId");
  const timeLimit = sessionStorage.getItem("timeLimit")

  const checkForUser = () => {
    if (guestId === '0') {
      fetch("http://127.0.0.1:5000/connect_to_game", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ guest_id: -1, room_id: roomId }),
      })
        .then((res) => res.json())
        .then((res) => {
          if (res.room_data_json.guest_id) {
            setCounter(res.room_data_json.settings.time_limit)
            setLoading(false);
            sessionStorage.setItem("guestId", res.room_data_json.guest_id);
          }
        });
    } else {
      setCounter(timeLimit)
      setLoading(false);
    }
  };

  useEffect(() => {
    resizeBoard();
    setCards(initializeDeck());
  }, []);

  useEffect(() => {
    counter > 0 && setTimeout(() => setCounter(counter - 1), 1000);
    if (counter === 0 || solved.length === 10) {
      const role = sessionStorage.getItem("guestId") ? 'host' : 'guest'

      fetch("http://127.0.0.1:5000/end_game", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          room_id: roomId, 
          player_role: role, 
          player_id: userId, 
          player_game_score: score 
        }),
      })
      history.push({ pathname: '/end', score, userId, role, roomId })
    }

  }, [counter]);

  useEffect(() => {
    if (loading) {
      checkForUser();
      const interval = setInterval(() => {
        checkForUser();
      }, 1000);

      return () => clearInterval(interval);
    }
  });

  useEffect(() => {
    const resizeListener = window.addEventListener("resize", resizeBoard);
    return () => window.removeEventListener("resize", resizeListener);
  });

  const handleOtherRoomsClick = () => {
    sessionStorage.removeItem("roomId");
    history.push("/rooms");
  };

  const handleClick = (id) => {
    setDisabled(true);
    if (flipped.length === 0) {
      setFlipped([id]);
      setDisabled(false);
    } else {
      if (sameCardClicked(id)) return;
      setFlipped([flipped[0], id]);
      if (isMatch(id)) {
        setScore(score + 2 * combo);
        setCombo(combo + 1);
        setSolved([...solved, flipped[0], id]);
        resetCards();
      } else {
        setScore(score - 1);
        setCombo(1);
        noMatch();
      }
    }
  };

  const noMatch = () => {
    setTimeout(resetCards, 1000);
  };

  const resetCards = () => {
    setFlipped([]);
    setDisabled(false);
  };

  const sameCardClicked = (id) => flipped.includes(id);

  const isMatch = (id) => {
    const clickedCard = cards.find((card) => card.id === id);
    const flippedCard = cards.find((card) => flipped[0] === card.id);
    return flippedCard.type === clickedCard.type;
  };

  const resizeBoard = () => {
    setDimension(
      Math.min(
        document.documentElement.clientWidth,
        document.documentElement.clientHeight
      )
    );
  };

  return (
    <Container component="main" maxWidth="sm">
      <CssBaseline />
      <Grid
        container
        direction="row"
        justify="space-evenly"
        alignItems="center"
      >
        <Grid item>
          <Button
            type="button"
            fullWidth
            variant="contained"
            color="primary"
            onClick={handleOtherRoomsClick}
          >
            {"Leave"}
          </Button>
        </Grid>
        <Grid item>
          <Typography component="h2" variant="h5">
            {"Score: " + score}
          </Typography>
        </Grid>
        {counter !== 0 &&<Grid item>
          <Typography component="h2" variant="h5">
            {`${counter >= 60 ? '01' : '00'}:${counter < 10 || (counter > 60 && counter < 70) ? '0' : ''}${counter % 60}`}
          </Typography>
        </Grid>}
      </Grid>
      <Grid>
        {loading ? (
          <>
            <Typography component="h5" variant="h5">
              {"Waiting for another player to join ..."}
            </Typography>
            <CircularProgress />
          </>
        ) : (
          <Board
            dimension={dimension}
            cards={cards}
            flipped={flipped}
            handleClick={handleClick}
            disabled={disabled}
            solved={solved}
          />
        )}
      </Grid>
    </Container>
  );
}
