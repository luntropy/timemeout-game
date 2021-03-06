import React, { useState, useEffect } from "react";
import { useHistory, useLocation } from "react-router-dom";
import {
  Button,
  CssBaseline,
  Typography,
  Container,
  CircularProgress,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

const Over = () => {
  const history = useHistory();
  const classes = useStyles();
  const location = useLocation();

  const [hasWon, setHasWon] = useState('');
  const [waiting, setWaiting] = useState(true);
  const [otherScore, setOtherScore] = useState(0);

  const { roomId, userId, score, role } = location;

  const checkForUser = () => {
    fetch("http://127.0.0.1:5000/game_over", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        room_id: roomId,
        player_id: userId,
        player_role: role,
      }),
    })
      .then((res) => res.json())
      .then((res) => {
        if (res.finished) {
          score === Number(res.host_score)
            ? setOtherScore(Number(res.guest_score))
            : setOtherScore(Number(res.host_score));
          setHasWon(res.winner_id === userId ? 'won' : 'lost');
          setWaiting(false);
        }
      });
  };

  useEffect(() => {
    if (waiting) {
      checkForUser();
      const interval = setInterval(() => {
        checkForUser();
      }, 2000);

      return () => clearInterval(interval);
    }
  });

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Typography component="h1" variant="h2">
          {"Game Over"}
        </Typography>
        <Typography component="h1" variant="h5">
          {`You have achieved ${score} points!`}
        </Typography>
        {waiting ? (
          <>
            <Typography component="h1" variant="h5">
              {`Waiting for other player to finish...`}
            </Typography>
            <CircularProgress />
          </>
        ) : (
          <>
            {" "}
            {otherScore !== -100 ? (
              <Typography component="h5" variant="h5">
                {`Your opponent has ${otherScore} points!`}
              </Typography>
            ) : (
              <Typography component="h1" variant="h5">
                {`Your opponent has left the game!`}
              </Typography>
            )}
            {score === otherScore ? (
              <Typography component="h1" variant="h5">
                {`It's a draw!`}
              </Typography>
            ) : (
              <>
              {hasWon &&
              <Typography component="h1" variant="h5">
                {`You have ${hasWon} the game!`}
              </Typography>
              }</>
            )}
            <Button
              type="button"
              fullWidth
              variant="contained"
              color="primary"
              onClick={() => {
                sessionStorage.removeItem("guestId");
                sessionStorage.removeItem("roomId");
                sessionStorage.removeItem("timeLimit");
                history.push("/rooms");
              }}
              className={classes.submit}
            >
              {"Back To Rooms"}
            </Button>
          </>
        )}
      </div>
    </Container>
  );
};

export default Over;
