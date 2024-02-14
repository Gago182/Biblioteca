
<template>
    <div class="container-fluid full-height-container bg-white">
        <br>
        <div class="card">
        <div class="card-header">
            Registro de Personas <button type="button" class="btn btn-success btn-sm mx-2" @click="agregarPersona" data-bs-toggle="modal" data-bs-target="#modalPersonaForm">Agregar<i class="fas fa-book mx-2 "></i></button>
        </div>
        <div class="card-body">
            <table class="table">
            <thead>
                <tr>
                <th scope="col">DNI</th>
                <th scope="col">Nombre</th>
                <th scope="col">Apellido P.</th>
                <th scope="col">Apellido M.</th>
                <th scope="col">Acciones</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for='data in dataPersonas'>
                    <td>{{data.dni}}</td>
                    <td>{{data.nombre}}</td>
                    <td>{{ data.apellido_p }}</td>
                    <td>{{ data.apellido_m }}</td>
                    <td>
                        <button  class="btn btn-success btn-sm" data-bs-toggle="modal" @click="editarPersona(data)" data-bs-target="#modalPersonaForm" >
                            <i class="fas fa-pencil"></i>
                        </button>
                        <button  class="btn btn-danger btn-sm m-1" @click="eliminarPersona(data)">
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
    <div class="modal fade" id="modalPersonaForm" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-scrollable">
        <div class="modal-content">
        <div class="modal-header p-2 bg-dark text-white">
            <i class="fas fa-server" style="font-size: 1rem;"></i>
            <h5 class="modal-title m-1" id="exampleModalLabel">Persona</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
            <form>
                    <div class="row bg-light">
                        <div class="col-12 mb-2">
                            <label class="form-label">DNI :</label>
                            <input type="text" class="form-control form-control-sm"  v-model='nuevaPersona.dni' placeholder="">
                        </div>
                        <div class="col-12 mb-2">
                            <label class="form-label">Nombres :</label>
                            <input type="text" class="form-control form-control-sm"  v-model='nuevaPersona.nombre' placeholder="Ingrese Nombres">
                        </div>
                        <div class="col-12 mb-2">
                            <label class="form-label">Apellido Paterno :</label>
                            <input type="text" class="form-control form-control-sm"  v-model='nuevaPersona.apellido_p' placeholder="Ingrese Apellido Paterno">
                        </div>
                        <div class="col-6 mb-2">
                            <label class="form-label">Apellido Materno :</label>
                            <input type="text" class="form-control form-control-sm"  v-model='nuevaPersona.apellido_m' placeholder="Ingrese Appelido Materno">
                        </div>
                    </div>
                </form>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal" ref="cerrarModal">Cerrar</button>
            <button type="button" class="btn btn-primary btn-sm" v-if="btnGuardar" @click="guardarPersona">Guardar</button>
            <button type="button" class="btn btn-success btn-sm" v-if="btnEditar" @click="actualizarPersona">Editar</button>
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
                dataPersonas: [],
                btnGuardar:false,
                btnEditar:false,
                nuevaPersona: {
                    dni: 0,
                    nombre: "",
                    apellido_p: "",
                    apellido_m: "",
                },
                backend_server: 'http://127.0.0.1:5000'
            };
        },
        mounted() {
            //this.obtenerFechaActual();
        },
        methods: {
            guardarPersona(){
                
                var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
                axios.post(this.backend_server + '/back/persona', this.nuevaPersona, { config_request })
                .then(res => {                                      
                    alert('Registro guardado');
                    this.mostarPersonas();
                    this.$refs.cerrarModal.click();
                })
                .catch((error) => {
                    alert('Error al guardar registro');
                    console.log(error)
                }); 
    
                
            },
            limpiarFormulario(){
                this.nuevaPersona= {
                    dni: 0,
                    nombre: "",
                    apellido_p: "",
                    apellido_m: "",
                }
            },
            actualizarPersona(){
                var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
                axios.put(this.backend_server + '/back/persona', this.nuevaPersona, { config_request })
                .then(res => {    
                    alert('Registro actualizado');                                  
                    this.mostarPersonas();
                    this.$refs.cerrarModal.click();
                })
                .catch((error) => {
                    alert('Error al actualziar registro');
                    console.log(error)
                });
                
                
            },
            
            eliminarPersona(data){
                var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
                axios.delete(this.backend_server + '/back/persona/' + data.dni, {}, { config_request })
                .then(res => {      
                    alert('Registro eliminado');                                   
                    this.mostarPersonas();
                })
                .catch((error) => {
                    alert('Error al eliminar registro');   
                    console.log(error)
                }); 
            },
            editarPersona(data){
                this.nuevaPersona=data;
                this.btnGuardar=false;
                this.btnEditar=true;
                
            },
            agregarPersona(){
                this.btnGuardar=true;
                this.btnEditar=false;
                this.limpiarFormulario();
            },
            mostarPersonas(){
                axios.get(this.backend_server + "/back/persona")
                    .then(res => {
                     //   console.log(res.data);
                    this.dataPersonas = res.data;
                });
            }
        },
        created() {
            this.mostarPersonas();
        },
        components: {  }
    }
    
    </script>