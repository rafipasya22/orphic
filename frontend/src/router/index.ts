import App from '@/App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Dash from '@/views/dash.vue'
import History from '@/views/history.vue'
import Help from '@/views/help.vue'
import Pred_result from '@/views/pred_results.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/dash',
      name: 'dash',
      component: Dash
    },
    {
      path: '/dash/manage-history',
      name: 'history',
      component: History
    },
    {
      path: '/dash/help',
      name: 'help',
      component: Help
    },
    {
      path: '/dash/predictions/:historyId',
      name: 'pred_result',
      component: Pred_result
    }
  ],
})

export default router
