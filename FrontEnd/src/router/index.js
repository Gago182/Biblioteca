import { createRouter, createWebHistory } from 'vue-router';
import UserComponent from '../components/UserComponent.vue';
import HomeComponent from '../components/HomeComponent.vue';
import PrestamoComponent from '../components/PrestamoComponent.vue';
import LibroComponent from '../components/LibroComponent.vue';
import RolComponent from '../components/RolComponent.vue';
import PersonaComponent from '../components/PersonaComponent.vue';
import ReporteComponent from '../components/ReporteComponent.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeComponent,
  },
  {
    path: '/home',
    name: 'home',
    component: HomeComponent,
  },
  {
    path: '/usuario',
    name: 'Usuarios',
    component: UserComponent,
  },
  {
    path: '/prestamo',
    name: 'Prestamos',
    component: PrestamoComponent,
  },
  {
    path: '/libro',
    name: 'Libros',
    component: LibroComponent,
  },
  {
    path: '/rol',
    name: 'Roles',
    component: RolComponent,
  },{
    path: '/persona',
    name: 'Personas',
    component: PersonaComponent,
  }
  ,{
    path: '/reporte',
    name: 'Reportes',
    component: ReporteComponent,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
