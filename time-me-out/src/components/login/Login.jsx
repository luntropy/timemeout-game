import React, { useState } from 'react'
import {
    useHistory,
    Link
} from "react-router-dom";
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
    register: {
        alignItems: 'center',
    }
  }));


const Reg = () => {
    const history = useHistory();
    const classes = useStyles();

    const [userVal, setUserVal] = useState('')
    const [passVal, setPassVal] = useState('')
    //const [error, setError] = useState(false)

    const onClick = () => fetch('http://127.0.0.1:5000/login_user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: userVal, password: passVal }),
      }).then(res=>res.json()).then(res => {
          if ( res.login === 1) {
              sessionStorage.setItem('userId', res.player_id)
              history.push('/create') 
            } 
        //else setError(true) 
    })

    return (
        

        <div>
            <strong>Enter details:</strong>
            <label>Username: </label><br />
            <input type="text" value={userVal} onChange={(e) => setUserVal(e.target.value)} name="username" /><br />
            <label>Password: </label><br />
            <input type="password" value={passVal} onChange={(e) => setPassVal(e.target.value)} name="password" /><br />
            <button onClick={onClick}>Login</button><br />
            
            <Link to="/register">Don't have an accout? Sign up</Link>
        </div>

    //     <Container component="main" maxWidth="xs">
    //     <CssBaseline />
    //     <div className={classes.paper}>
    //       <Typography component="h1" variant="h5">
    //         Sign in
    //       </Typography>
    //       <form className={classes.form} noValidate>
    //         <TextField
    //           variant="outlined"
    //           margin="normal"
    //           required
    //           fullWidth
    //           id="username"
    //           label="Username"
    //           name="username"
    //           autoComplete="username"
    //           value={userVal}
    //           onChange={(e) => setUserVal(e.target.value)}
    //           autoFocus
    //         />
    //         <TextField
    //           variant="outlined"
    //           margin="normal"
    //           required
    //           fullWidth
    //           name="password"
    //           label="Password"
    //           type="password"
    //           id="password"
    //           autoComplete="current-password"
    //           value={passVal}
    //           onChange={(e) => setPassVal(e.target.value)}
    //         />
    //         <Button
    //           type="submit"
    //           fullWidth
    //           variant="contained"
    //           color="primary"
    //           onClick={onClick}
    //           className={classes.submit}
    //         >
    //           Sign In
    //         </Button>
    //         <Grid container>
    //           <Grid item>
    //             <Link to="/register" variant="body2" className={classes.register}>
    //               {"Don't have an accout? Sign up"}
    //             </Link>
    //           </Grid>
    //         </Grid>
    //       </form>
    //     </div>
    //   </Container>
        
    )
}

export default Reg