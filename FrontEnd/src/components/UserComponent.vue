
<template>
  <div class="container-fluid full-height-container bg-white">
      <br>
      <div class="card">
      <div class="card-header">
          Registro de Usuarios <button type="button" class="btn btn-success btn-sm mx-2" @click="agregarUsuario" data-bs-toggle="modal" data-bs-target="#modalUsuarioForm">Agregar<i class="fas fa-user mx-2 "></i></button>
      </div>
      <div class="card-body">
          <table class="table">
          <thead>
              <tr>
              <th scope="col">DNI</th>
              <th scope="col">Persona</th>
              <th scope="col">Usuario</th>
              <th scope="col">Acciones</th>
              </tr>
          </thead>
          <tbody>
              <tr v-for='data in dataUsuarios'>
                  <td>{{data.dni}}</td>
                  <td>{{data.persona}}</td>
                  <td>{{ data.usuario }}</td>
                  <td>
                      <button  class="btn btn-success btn-sm" data-bs-toggle="modal" @click="editarUsuario(data)" data-bs-target="#modalUsuarioForm" >
                          <i class="fas fa-pencil"></i>
                      </button>
                      <button  class="btn btn-danger btn-sm m-1" @click="eliminarUsuario(data)">
                          <i class="fas fa-trash"></i>
                      </button>
                  </td> 
              </tr>
          </tbody>
          </table>  
      </div>
  
      </div>
  </div>
  
  <!-- Modal de Agregar Libro-->
  <div class="modal fade" id="modalUsuarioForm" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-md modal-dialog-scrollable">
      <div class="modal-content">
      <div class="modal-header p-2 bg-dark text-white">
          <i class="fas fa-server" style="font-size: 1rem;"></i>
          <h5 class="modal-title m-1" id="exampleModalLabel">Usuario</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
          <form>
                  <div class="row bg-light">
                      <div class="col-6 mb-2">
                          <label class="form-label">DNI :</label>
                          <select class="form-select form-select-sm" v-model='nuevoUsuario.dni'>
                            <option value="0" selected>Seleccione Persona</option>
                            <option v-for="opcion in dataPersona" :key="opcion.dni" :value="opcion.dni">{{ opcion.datos }}</option>
                        </select>
                      </div>
                      <div class="col-6 mb-2">
                          <label class="form-label">Usuario :</label>
                          <input type="text" class="form-control form-control-sm"  v-model='nuevoUsuario.usuario' placeholder="Ingrese Usuario">
                      </div>
                      <div class="col-6 mb-2">
                          <label class="form-label">Clave :</label>
                          <input type="password" class="form-control form-control-sm"  v-model='nuevoUsuario.clave' placeholder="***">
                      </div>
                  </div>
              </form>
      </div>
      <div class="modal-footer">
          <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal" ref="cerrarUsurioModal">Cerrar</button>
          <button type="button" class="btn btn-primary btn-sm" v-if="btnGuardar" @click="guardarUsuario">Guardar</button>
          <button type="button" class="btn btn-success btn-sm" v-if="btnEditar" @click="actualizarUsuario">Editar</button>
      </div>
      </div>
  </div>
  </div>
  <!-- End Modal Libro-->
  </template>
  <script>
  import axios from "axios";
  import CryptoJS from 'crypto-js';
  export default{
      data() {
          return {
              dataUsuarios: [],
              dataPersona: [],
              btnGuardar:false,
              btnEditar:false,
              nuevoUsuario: {
                clave: "",
                dni: 0,
                persona: "",
                usuario: ""
              },
              backend_server: 'http://127.0.0.1:5000'
          };
      },
      mounted() {
          //this.obtenerFechaActual();
      },
      methods: {
          guardarUsuario(){
            this.nuevoUsuario.clave=CryptoJS.SHA256(this.nuevoUsuario.clave).toString();
              var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
              axios.post(this.backend_server + '/back/login', this.nuevoUsuario, { config_request })
              .then(res => {                                      
                  alert('Registro guardado');
                  this.mostarUsuarios();
                  this.$refs.cerrarUsurioModal.click();
              })
              .catch((error) => {
                  alert('Error al guardar registro o el Usuario ya existe');
                  console.log(error)
              }); 
  
              
          },
          limpiarFormulario(){
              this.nuevoUsuario=  {
                clave: "",
                dni: 0,
                persona: "",
                usuario: ""
              }
          },
          actualizarUsuario(){
            this.nuevoUsuario.clave=CryptoJS.SHA256(this.nuevoUsuario.clave).toString();
              var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
              axios.put(this.backend_server + '/back/login', this.nuevoUsuario, { config_request })
              .then(res => {    
                  alert('Registro actualizado');                                  
                  console.log(this.nuevoUsuario);
                  this.mostarUsuarios();
                  this.$refs.cerrarUsurioModal.click();
              })
              .catch((error) => {
                  alert('Error al actualizar registro');
                  console.log(error)
              });
              
              
          },
          
          eliminarUsuario(data){
              var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
              axios.delete(this.backend_server + '/back/login/' + data.dni, {}, { config_request })
              .then(res => {      
                  alert('Registro eliminado');                                   
                  this.mostarUsuarios();
              })
              .catch((error) => {
                  alert('Error al eliminar registro');   
                  console.log(error)
              }); 
          },
          editarUsuario(data){
              this.nuevoUsuario=data;
              this.btnGuardar=false;
              this.btnEditar=true;
              
          },
          agregarUsuario(){
              this.btnGuardar=true;
              this.btnEditar=false;
              this.limpiarFormulario();
          },
          mostarUsuarios(){
              axios.get(this.backend_server + "/back/login")
                  .then(res => {
                   //   console.log(res.data);
                  this.dataUsuarios = res.data;
              });
          },
          mostarPersonas(){
              axios.get(this.backend_server + "/back/persona")
                  .then(res => {
                   //   console.log(res.data);
                  this.dataPersona = res.data;
              });
          }
      },
      created() {
          this.mostarUsuarios();
          this.mostarPersonas();
      },
      components: {  }
  }
  
  </script>