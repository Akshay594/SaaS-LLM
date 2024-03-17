import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Typography, TextField, Button, Box, Paper, CircularProgress } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  container: {
    marginTop: theme.spacing(4),
  },
  paper: {
    padding: theme.spacing(3),
    marginTop: theme.spacing(3),
  },
  form: {
    display: 'flex',
    alignItems: 'center',
  },
  textField: {
    marginRight: theme.spacing(2),
    flexGrow: 1,
  },
  fileInput: {
    marginBottom: theme.spacing(2),
  },
  button: {
    marginLeft: theme.spacing(2),
  },
  loadingOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    zIndex: 1,
  },
}));

function App() {
  const classes = useStyles();
  const [query, setQuery] = useState('');
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [dataIngested, setDataIngested] = useState(false);

  useEffect(() => {
    const handleFileUpload = async () => {
      const formData = new FormData();
      formData.append('file', file);

      setLoading(true);
      try {
        const res = await axios.post('http://localhost:8000/upload_file/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        if (res.status === 200) {
          setDataIngested(true);
        }
      } catch (error) {
        console.error('Error:', error);
      }
      setLoading(false);
    };

    if (file) {
      handleFileUpload();
    }
  }, [file]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query) return;

    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/make_query/', { query });
      setResponse(res.data.response);
      setQuery('');
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="sm" className={classes.container}>
      <Typography variant="h4" align="center" gutterBottom>
        RAG Model Query
      </Typography>
      <Paper className={classes.paper}>
        {!dataIngested && (
          <Box mb={3}>
            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={handleFileChange}
              className={classes.fileInput}
            />
          </Box>
        )}
        <form onSubmit={handleSubmit} className={classes.form}>
          <TextField
            label="Enter your query"
            variant="outlined"
            fullWidth
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className={classes.textField}
            disabled={!dataIngested || loading}
          />
          <Button type="submit" variant="contained" color="primary" className={classes.button} disabled={!dataIngested || loading}>
            Submit
          </Button>
        </form>
      </Paper>
      {loading && (
        <div className={classes.loadingOverlay}>
          <CircularProgress />
        </div>
      )}
      {response && (
        <Box mt={3}>
          <Typography variant="h6">Response:</Typography>
          <Typography>{response}</Typography>
        </Box>
      )}
    </Container>
  );
}

export default App;