import React, { useState } from "react";
import { useHistory, Link } from "react-router-dom";
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  form: {
    width: '100%',
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  login: {
      textDecoration: 'none',
  }
}));

const Registration = () => {
  const history = useHistory();
  const classes = useStyles()

  const [userVal, setUserVal] = useState("");
  const [passVal, setPassVal] = useState("");
  const [confPassVal, setConfPassVal] = useState("");
  const [error, setError] = useState('');

  const onClick = () => {
    if (confPassVal !== passVal) {
      setError('Passwords do not match!')
      return
    }

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
          history.push("/rooms");
        } else setError('Invalid data!');
      });
    }

  return (
    <Container component="main" maxWidth="xs">
        <CssBaseline />
        <div className={classes.paper}>
          <Typography component="h1" variant="h5">
            {"Sign up"}
          </Typography>
          <form className={classes.form} noValidate>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              value={userVal}
              onChange={(e) => setUserVal(e.target.value)}
              autoFocus
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              value={passVal}
              onChange={(e) => setPassVal(e.target.value)}
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="confirm-password"
              label="Confirm Password"
              type="password"
              id="confirm-password"
              autoComplete="confirm-password"
              value={confPassVal}
              onChange={(e) => setConfPassVal(e.target.value)}
            />
            {error && 
                <Typography component="h2" variant="h6">
                    {error} {"Please try again!"}
                </Typography>
            }
            <Button
              type="button"
              fullWidth
              variant="contained"
              color="primary"
              onClick={onClick}
              className={classes.submit}
            >
              {"Sign Up"}
            </Button>
            <Grid container>
              <Grid item>
                <Link to="/" variant="body2" className={classes.login}>
                  {"Already have an account? Sign in!"}
                </Link>
              </Grid>
            </Grid>
          </form>
        </div>
      </Container>
  );
};

export default Registration;
