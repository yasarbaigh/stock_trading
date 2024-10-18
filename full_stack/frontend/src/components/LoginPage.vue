<template>
    <div class="login-page">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div>
          <label for="username">Username:</label>
          <input type="text" v-model="username" id="username" required />
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" v-model="password" id="password" required />
        </div>
        <button type="submit">Login</button>
        <p v-if="errorMessage">{{ errorMessage }}</p>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoginPage',
    data() {
      return {
        username: '',
        password: '',
        errorMessage: '',
      };
    },
    methods: {
      login() {
        // Static credentials
        // const staticUsername = 'admin';
        // const staticPassword = 'password123';

        const staticUsername = 'a';
        const staticPassword = 'a';
  
        if (this.username === staticUsername && this.password === staticPassword) {
          localStorage.setItem('isLoggedIn', 'true'); // Set login state
        
          this.$router.push({ name: 'Dashboard' });
        } else {
          this.errorMessage = 'Invalid username or password';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .login-page {
    max-width: 400px;
    margin: auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
  }
  
  button {
    padding: 10px;
    background-color: #4CAF50;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  p {
    color: red;
    margin-top: 10px;
  }
  </style>
  