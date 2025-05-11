/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import { setupLayouts } from 'virtual:generated-layouts'
import { routes } from 'vue-router/auto-routes'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: setupLayouts([
    ...routes,
    {
      path: '/aiph',
      component: () => import('@/pages/aiph.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/team',
      component: () => import('@/pages/team.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/meetings',
      component: () => import('@/pages/meetings.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/objectives',
      component: () => import('@/pages/objectives.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/key-results',
      component: () => import('@/pages/key-results.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/evaluations',
      component: () => import('@/pages/evaluations.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/objective-dashboard/:id',
      component: () => import('@/pages/objective-dashboard.vue'),
      meta: { requiresAuth: true },
    },
  ]),
})

// After router is created, set meta.requiresAuth for /aiph and related pages
router.getRoutes().forEach(route => {
  if ([
    '/aiph',
    '/team',
    '/meetings',
    '/objectives',
    '/key-results',
    '/evaluations',
  ].includes(route.path)) {
    route.meta.requiresAuth = true
  }
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  // Always check for a valid token and user
  // console.log('Checking auth before route change')
  // console.log('Current token:', auth.token)
  // console.log('Current user:', auth.user)
  // console.log('Route meta requiresAuth:', to.meta.requiresAuth)
  if (to.meta.requiresAuth) {
    // If no token, redirect immediately
    // console.log('Route requires auth, checking token and user')
    if (!auth.token) {
      // console.log('No token found, redirecting to login')
      return next({ path: '/' })
    }
    // If token exists but user is not loaded, fetch user and check again
    // console.log('Token found, checking user')
    if (!auth.user) {
      try {
        await auth.fetchUser()
      } catch {
        auth.logout()
        return next({ path: '/' })
      }
      if (!auth.user) {
        auth.logout()
        return next({ path: '/' })
      }
    }
  }
  // console.log('Auth check passed, proceeding to route')
  next()
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
