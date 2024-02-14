
<template>
    <div class="container-fluid full-height-container bg-white">
        <br>
        <div class="card">
        <div class="card-header">
            Registro de Roles <button type="button" class="btn btn-success btn-sm mx-2" @click="agregarRol" data-bs-toggle="modal" data-bs-target="#modalRolForm">Agregar<i class="fas fa-book mx-2 "></i></button>
        </div>
        <div class="card-body">
            <table class="table">
            <thead>
                <tr>
                <th scope="col">Cod Rol</th>
                <th scope="col">Nombre</th>
                <th scope="col">Acciones</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for='data in dataRoles'>
                    <td>{{data.cod_rol}}</td>
                    <td>{{data.nombre}}</td>
                    <td>
                        <button  class="btn btn-success btn-sm" data-bs-toggle="modal" @click="editarRol(data)" data-bs-target="#modalRolForm" >
                            <i class="fas fa-pencil"></i>
                        </button>
                        <button  class="btn btn-danger btn-sm m-1" @click="eliminarRol(data)">
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
    <div class="modal fade" id="modalRolForm" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-scrollable">
        <div class="modal-content">
        <div class="modal-header p-2 bg-dark text-white">
            <i class="fas fa-server" style="font-size: 1rem;"></i>
            <h5 class="modal-title m-1" id="exampleModalLabel">Rol</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
            <form>
                    <div class="row bg-light">
                        <div class="col-12 mb-2">
                            <label class="form-label">Rol :</label>
                            <input type="text" class="form-control form-control-sm"  v-model='nuevoRol.nombre' placeholder="Ingrese nombre del Rol">
                        </div>

                            
                    </div>
                </form>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal" ref="cerrarModal">Cerrar</button>
            <button type="button" class="btn btn-primary btn-sm" v-if="btnGuardar" @click="guardarRol">Guardar</button>
            <button type="button" class="btn btn-success btn-sm" v-if="btnEditar" @click="actualizarRol">Editar</button>
        </div>
        </div>
    </div>
    </div>
    <!-- End Modal Libro-->
    </template>
    <script>
    import axios from "axios";
    export default{
        data() {
            return {
                dataRoles: [],
                btnGuardar:false,
                btnEditar:false,
                nuevoRol: {
                    cod_rol: 0,
                    nombre: ""
                },
                backend_server: 'http://127.0.0.1:5000'
            };
        },
        mounted() {
            //this.obtenerFechaActual();
        },
        methods: {
            guardarRol(){
                
                var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
                axios.post(this.backend_server + '/back/rol', this.nuevoRol, { config_request })
                .then(res => {                                      
                    alert('Registro guardado');
                    this.mostarRoles();
                    this.$refs.cerrarModal.click();
                })
                .catch((error) => {
                    alert('Error al guardar registro');
                    console.log(error)
                }); 
    
                
            },
            limpiarFormulario(){
                this.nuevoRol= {
                    cod_rol: 0,
                    nombre: ""
                }
            },
            actualizarRol(){
                var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
                axios.put(this.backend_server + '/back/rol', this.nuevoRol, { config_request })
                .then(res => {    
                    alert('Registro actualizado');                                  
                    console.log(this.nuevoRol);
                    this.mostarRoles();
                    this.$refs.cerrarModal.click();
                })
                .catch((error) => {
                    alert('Error al actualziar registro');
                    console.log(error)
                });
                
                
            },
            
            eliminarRol(data){
                var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
                axios.delete(this.backend_server + '/back/rol/' + data.cod_rol, {}, { config_request })
                .then(res => {      
                    alert('Registro eliminado');                                   
                    this.mostarRoles();
                })
                .catch((error) => {
                    alert('Error al eliminar registro');   
                    console.log(error)
                }); 
            },
            editarRol(data){
                this.nuevoRol=data;
                this.btnGuardar=false;
                this.btnEditar=true;
                
            },
            agregarRol(){
                this.btnGuardar=true;
                this.btnEditar=false;
                this.limpiarFormulario();
            },
            mostarRoles(){
                axios.get(this.backend_server + "/back/rol")
                    .then(res => {
                    this.dataRoles = res.data;
                });
            }
        },
        created() {
            this.mostarRoles();
        },
        components: {  }
    }
    
    </script>