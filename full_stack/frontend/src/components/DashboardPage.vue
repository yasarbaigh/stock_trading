<template>
  <div class="dashboard-page">
    <!-- Header with logout button -->
    <header class="dashboard-header">
      <h2>Dashboard</h2>
      <button class="logout-button" @click="logout">Logout</button>
    </header>

    <!-- Main layout with sidebar and content area -->
    <div class="dashboard-content">
      <nav class="sidebar">
        <ul>
          <!-- <li>
            <router-link to="/dashboard">Dashboard Home</router-link>
          </li> -->

          <li>
            <router-link to="/dashboard/running">Running</router-link>
          </li>
          <li>
            <router-link to="/dashboard/indices">Indices</router-link>
          </li>
          <li>
            <router-link to="/dashboard/nifty_50">Nifty 50</router-link>
          </li>

          <li>
            <router-link to="/dashboard/fno">FnO</router-link>
          </li>        
          
        </ul>
      </nav>

      <!-- Content area where child routes will be displayed -->
      <main class="content">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardPage',
  methods: {
    logout() {
      localStorage.removeItem('isLoggedIn');
      this.$router.push({ name: 'Login' });
    },
  },
};
</script>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
}

.logout-button {
  background-color: #f44336;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.logout-button:hover {
  background-color: #d32f2f;
}

.dashboard-content {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 200px;
  background-color: #f4f4f4;
  padding: 10px;
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 10px;
}

.sidebar a {
  text-decoration: none;
  color: #333;
  padding: 8px;
  display: block;
  border-radius: 4px;
}

.sidebar a:hover {
  background-color: #ddd;
}

.content {
  flex: 1;
  padding: 20px;
  background: #fff;
  overflow-y: auto;
}
</style>
