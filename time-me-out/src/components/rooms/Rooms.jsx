import React, { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";
import {
  Button,
  CssBaseline,
  Grid,
  Typography,
  Container,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  FormLabel,
  List,
  ListItem,
  ListItemText,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  form: {
    width: "100%",
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  join: {
    textDecoration: "none",
  },
}));

const Rooms = () => {
  const history = useHistory();
  const classes = useStyles();

  const [showRooms, setShowRooms] = useState(true);
  const [value, setValue] = useState();
  const [error, setError] = useState("");
  const [rooms, setRooms] = useState([]);

  const fetchData = () =>
    fetch("http://127.0.0.1:5000/list_games")
      .then((res) => res.json())
      .then((res) => setRooms(res.rooms_list || []));

  useEffect(() => {
    fetchData();
  }, []);

  const onJoinClick = (id) => {
    const userId = sessionStorage.getItem("userId");
    fetch("http://127.0.0.1:5000/connect_to_game", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ guest_id: userId, room_id: id }),
    })
      .then((res) => res.json())
      .then((res) => {
        sessionStorage.setItem("roomId", res.room_data_json.room_id);
        sessionStorage.setItem("timeLimit", res.room_data_json.settings.time_limit)
        res.room_data_json
          ? history.push(`/game/${id}`)
          : setError("Error joining game!");
      });
  };

  const onCreateClick = () =>
    fetch("http://127.0.0.1:5000/create_game", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        host_id: 3,
        field_size: 16,
        time_limit: parseInt(value),
      }),
    })
      .then((res) => res.json())
      .then((res) => {
        sessionStorage.setItem("roomId", res.room_id);
        sessionStorage.setItem("guestId", 0);
        res.game_creation === 1
          ? history.push(`/game/${res.room_id}`)
          : setError("Error creating game!");
      });

  return (
    <Container component="main" maxWidth="xs">
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
            onClick={() => setShowRooms(true)}
            className={classes.submit}
          >
            {"Rooms"}
          </Button>
        </Grid>
        <Grid item>
          <Button
            type="button"
            fullWidth
            variant="contained"
            color="primary"
            onClick={() => setShowRooms(false)}
            className={classes.submit}
          >
            {"Create"}
          </Button>
        </Grid>
        <Grid item>
          <Button
            type="button"
            fullWidth
            variant="contained"
            color="primary"
            onClick={() => {
              sessionStorage.removeItem("userId")
              history.push('/')              
            }}
            className={classes.submit}
          >
            {"Logout"}
          </Button>
        </Grid>
      </Grid>
      {!showRooms && (
        <div className={classes.paper}>
          <Typography component="h1" variant="h5">
            {"New Room"}
          </Typography>
          <form className={classes.form} noValidate>
            <FormControl component="fieldset">
              <FormLabel component="legend">{"Game Duration:"}</FormLabel>
              <RadioGroup
                aria-label="time"
                name="time"
                value={value}
                onChange={(e) => setValue(e.target.value)}
              >
                <FormControlLabel
                  value="40"
                  control={<Radio />}
                  label="40 sec"
                />
                <FormControlLabel
                  value="60"
                  control={<Radio />}
                  label="60 sec"
                />
                <FormControlLabel
                  value="90"
                  control={<Radio />}
                  label="90 sec"
                />
              </RadioGroup>
            </FormControl>
            {error && (
              <Typography component="h2" variant="h6">
                {error}
              </Typography>
            )}
            <Button
              type="button"
              fullWidth
              variant="contained"
              color="primary"
              onClick={onCreateClick}
              className={classes.submit}
            >
              {"Create Game"}
            </Button>
          </form>
        </div>
      )}
      {showRooms && (
        <div className={classes.paper}>
          <Typography component="h1" variant="h5">
            {"Available Rooms"}
          </Typography>
          <List component="nav" aria-label="secondary mailbox folders">
            {rooms.map((r) => {
              return (
                <ListItem>
                  <ListItemText primary={r} />
                  <Button
                    type="button"
                    variant="contained"
                    color="primary"
                    onClick={() => onJoinClick(r)}
                    className={classes.submit}
                  >
                    {"Join Game"}
                  </Button>
                </ListItem>
              );
            })}
          </List>
          <Button
            type="button"
            variant="contained"
            color="primary"
            onClick={() => fetchData()}
            className={classes.submit}
          >
            {"Refresh"}
          </Button>
        </div>
      )}
    </Container>
  );
};

export default Rooms;
