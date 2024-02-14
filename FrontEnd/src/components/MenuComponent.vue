<template>
    <nav class="navbar navbar-expand-lg navbar-dark" style="background-color: #373536;">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">
        <img src="https://i.pinimg.com/736x/c4/23/d7/c423d7f929650892d3345964a5230989.jpg" width="50" alt="">
        Biblio Virtual</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Personas
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><router-link to="/persona" class="dropdown-item">Ver Personas</router-link></li>
              <li><router-link to="/usuario" class="dropdown-item">Usuarios</router-link></li>
              <li><hr class="dropdown-divider"></li>
              <li><router-link to="/rol" class="dropdown-item">Roles</router-link></li>
            </ul>
          </li>
          <li class="nav-item">
            <router-link to="/libro" class="nav-link">Libros</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/prestamo" class="nav-link">Prestamos</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/reporte" class="nav-link">Reportes</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Ayuda</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  </template>