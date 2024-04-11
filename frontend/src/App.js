import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Typography, TextField, Button, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
});

const App = () => {
  const [items, setItems] = useState([]);
  const [name, setName] = useState('');
  const [quantity, setQuantity] = useState('');

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = () => {
    api.get('/items')
      .then(response => {
        // Map response data to format expected by the component
        const formattedItems = response.data.map(item => ({
          id: item[0], // Assuming item[0] is the id
          name: item[1], // Assuming item[1] is the name
          quantity: item[2], // Assuming item[2] is the quantity
        }));
        setItems(formattedItems);
      })
      .catch(error => {
        console.error('Error fetching items:', error);
      });
  };

  const handleAddItem = () => {
    api.post('/items', { name, quantity })
      .then(response => {
        console.log(response.data.message);
        fetchItems();
        setName('');
        setQuantity('');
      })
      .catch(error => {
        console.error('Error adding item:', error);
      });
  };

  const handleDeleteItem = (itemId) => {
    api.delete(`/items/${itemId}`)
      .then(response => {
        console.log(response.data.message);
        fetchItems();
      })
      .catch(error => {
        console.error('Error deleting item:', error);
      });
  };

  return (
    <Container maxWidth="sm" style={{ marginTop: '40px' }}>
      <Typography variant="h4" gutterBottom>
        Items List
      </Typography>
      <TextField
        label="Name"
        variant="outlined"
        value={name}
        onChange={(e) => setName(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Quantity"
        variant="outlined"
        type="number"
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
        fullWidth
        margin="normal"
      />
      <Button variant="contained" color="primary" onClick={handleAddItem}>
        Add Item
      </Button>
      <List style={{ marginTop: '20px' }}>
        {items.map(item => (
          <ListItem key={item.id}>
            <ListItemText primary={item.name} secondary={`Quantity: ${item.quantity}`} />
            <ListItemSecondaryAction>
              <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteItem(item.id)}>
                <DeleteIcon />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>
    </Container>
  );
};

export default App;
