
import { createRouter, createWebHistory } from 'vue-router'

import LoginPage from '@/components/LoginPage.vue';
import DashboardPage from '@/components/DashboardPage.vue';
import Indices_Page from '@/components/stocks/Indices.vue';
import Nifty_50_Page from '@/components/stocks/Nifty_50.vue';
import FnO_Page from '@/components/stocks/FnO.vue';
import Running_Page from '@/components/stocks/Running_Pattern_Page.vue';



const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginPage,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardPage,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'DashboardHome',
        component: {
          template: '<div>Welcome to the Dashboard! Select an option from the sidebar.</div>',
        },
      },
      {
        path: 'running',
        name: 'Running',
        component: Running_Page,
      },
      {
        path: 'indices',
        name: 'Indices',
        component: Indices_Page,
      },
      {
        path: 'nifty_50',
        name: 'Nifty 50',
        component: Nifty_50_Page,
      },
      {
        path: 'fno',
        name: 'FnO List',
        component: FnO_Page,
      },      
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation guard to check if the route requires authentication
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn');

  if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn) {
    next({ name: 'Login' }); // Redirect to login page if not authenticated
  } else {
    next(); // Proceed to the route
  }
});

export default router;
