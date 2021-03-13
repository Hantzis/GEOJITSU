
const routes = [
  { path: '/', component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: 'herramientas', component: () => import('pages/Index.vue') },
      { path: 'tab', component: () => import('pages/V.vue'),
        children: [
          { path: '*', component: () => import('pages/StandardPage.vue') }
        ]
      },
    ]
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes
