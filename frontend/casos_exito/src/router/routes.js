
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: '/proyectos', component: () => import('pages/Proyectos.vue') },
      { path: '/evaluaciones', component: () => import('pages/Evaluaciones.vue') },
      { path: '/casos-exito', component: () => import('pages/casosExito.vue') },
      { path: '/acerca-de', component: () => import('pages/acercaDe.vue') },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
