
<template>
    <div class="container-fluid full-height-container bg-white">
        <br>
        <div class="card">
        <div class="card-header">
            Registro de Préstamo de Libros <button type="button" class="btn btn-success btn-sm mx-2" @click="agregarPrestamo" data-bs-toggle="modal" data-bs-target="#modalPrestamoForm">Agregar<i class="fas fa-file-text mx-2 "></i></button>
        </div>
        <div class="card-body">
            <table class="table">
            <thead>
                <tr>
                <th scope="col">DNI</th>
                <th scope="col">Cliente</th>
                <th scope="col">Bibliotecario</th>
                <th scope="col">Fecha</th>
                <th scope="col">Devolución</th>
                <th scope="col">Acciones</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for='data in dataPrestamos'>
                    <td>{{data.dni}}</td>
                    <td>{{data.cliente}}</td>
                    <td>{{ data.bibliotecario }}</td>
                    <td>{{ data.fecha_entrega }}</td>
                    <td>{{ data.fecha_devolucion }}</td>
                    <td>
                        <button  class="btn btn-success btn-sm" data-bs-toggle="modal" @click="editarPrestamo(data)" data-bs-target="#modalPrestamoForm" >
                            <i class="fas fa-pencil"></i>
                        </button>
                        <button  class="btn btn-danger btn-sm m-1" @click="eliminarPrestamo(data)">
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
    <div class="modal fade" id="modalPrestamoForm" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-scrollable">
        <div class="modal-content">
        <div class="modal-header p-2 bg-dark text-white">
            <i class="fas fa-server" style="font-size: 1rem;"></i>
            <h5 class="modal-title m-1" id="exampleModalLabel">Préstamo de Libros</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
            <form>
                <div class="row bg-light">
                    <div class="col-12 mb-2">
                        <label class="form-label">Usuarios :</label>
                        <select class="form-select form-select-sm" v-model='nuevoPrestamo.dni'>
                            <option value="0" selected>Seleccione un Usuario</option>
                            <option v-for="opcion in dataPersonas" :key="opcion.dni" :value="opcion.dni">{{ opcion.datos }}</option>
                        </select>
                    </div>
                    <div class="col-12 mb-2">
                        <label class="form-label">Bibliotecario :</label>
                        <select class="form-select form-select-sm" v-model='nuevoPrestamo.cod_bibliotecario'>
                            <option value="0" selected>Seleccione Biliotecario</option>
                            <option v-for="opcion in dataBibliotecarios" :key="opcion.dni" :value="opcion.dni">{{ opcion.datos }}</option>
                        </select>
                    </div>
                    <div class="col-6 mb-2">
                        <label class="form-label">Fecha Entrega :</label>
                        <input type="date" class="form-control form-control-sm"  v-model='nuevoPrestamo.fecha_entrega'>
                    </div>
                    <div class="col-6 mb-2">
                        <label class="form-label">Fecha Devolución :</label>
                        <input type="date" class="form-control form-control-sm"  v-model='nuevoPrestamo.fecha_devolucion'>
                    </div>
                </div>
            </form>
            <!-- Inicio de detalle -->
            <hr>
            <span class="fw-bold">Préstamo de libros</span>
            <div v-show="mostrarDiv">
            <div class="row">
                <div class="col-10 mb-2">
                    <select id="cboEstudiante" class="form-select form-select-sm" v-model='nuevoDetalle.cod_libro'>
                        <option selected value="0">Seleccione un Libro</option>
                        <option v-for="opcion in dataLibros" :key="opcion.titulo" :value="opcion.cod_libro">{{ opcion.titulo }}</option>
                    </select>
                </div>
                <div class="col-2">
                    <button type="button" class="btn btn-sm btn-warning" @click="agregarDetalleLibro()">
                        <i class="fas fa-add"></i>
                        Agregar
                    </button>
                </div>
            </div>
            <div  class="row bg-light">
                <div class="col-12">
                    <table class="table table-sm display">
                        <thead class="bg-table-head">
                            <tr>
                                <th>Libros</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for='data in dataDetalles'>
                                <td>{{data.libro}}</td>
                                <td>
                                    <button  class="btn btn-info btn-sm py-0" @click="eliminarPrestamoDet(data)">
                                        <i class="fa-solid fa-book fa-xs"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            </div>
            <!-- Fin de detalle -->
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal" ref="cerrarPrestamoModal">Cerrar</button>
            <button type="button" class="btn btn-primary btn-sm" v-if="btnGuardar" @click="guardarPrestamo">Guardar</button>
            <button type="button" class="btn btn-success btn-sm" v-if="btnEditar" @click="actualizarPrestamo">Editar</button>
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
                mostrarDiv:false,
                dataPrestamos: [],
                dataDetalles: [],
                dataPersonas: [],
                dataLibros: [],
                dataBibliotecarios: [],
                btnGuardar:false,
                btnEditar:false,
                nuevoPrestamo: {
                  cod_prestamo: 0,
                  dni: 0,
                  cliente:"",
                  cod_bibliotecario: 0,
                  bibliotecario:"",
                  fecha_entrega: "",
                  fecha_devolucion: "",
                },
                nuevoDetalle: {
                  cod_prestamo_det: 0,
                  cod_prestamo: 0,
                  cod_libro:0,
                  prestado: true
                },
                backend_server: 'http://127.0.0.1:5000'
            };
        },
        mounted() {
            //this.obtenerFechaActual();
        },
        methods: {
            agregarDetalleLibro(){
                //console.log(this.nuevoDetalle);
                this.nuevoDetalle.cod_prestamo=this.nuevoPrestamo.cod_prestamo;
                var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
                axios.post(this.backend_server + '/back/prestamo_det', this.nuevoDetalle, { config_request })
                .then(res => {    
                    this.mostrarPrestamosDet();
                    //this.$refs.cerrarPrestamoModal.click();
                })
                .catch((error) => {
                    alert('Error al guardar registro !!');
                    //console.log(error)
                }); 
            },
            guardarPrestamo(){
                //console.log(this.nuevoPrestamo);
                var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
                axios.post(this.backend_server + '/back/prestamo_cab', this.nuevoPrestamo, { config_request })
                .then(res => {    
                    this.nuevoPrestamo=res.data['prestamo_cabecera']; 
                    this.btnEditar=true;
                    this.btnGuardar=false;                             
                    this.mostrarPrestamos();
                    this.mostrarDiv=true;
                    //this.$refs.cerrarPrestamoModal.click();
                })
                .catch((error) => {
                    alert('Error al guardar registro !!');
                    console.log(error)
                }); 
    
                
            },
            limpiarFormulario(){
                this.nuevoPrestamo=  {
                  cod_prestamo: 0,
                  dni: 0,
                  cliente:"",
                  cod_bibliotecario: 0,
                  bibliotecario:"",
                  fecha_entrega: "",
                  fecha_devolucion: ""
                }
            },
            actualizarPrestamo(){
                var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
                axios.put(this.backend_server + '/back/prestamo_cab', this.nuevoPrestamo, { config_request })
                .then(res => {    
                    alert('Registro actualizado');                                  
                    this.mostrarPrestamos();
                    this.$refs.cerrarPrestamoModal.click();
                })
                .catch((error) => {
                    alert('Error al actualizar registro');
                    console.log(error)
                });
                
                
            },
            
            eliminarPrestamo(data){
                var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
                axios.delete(this.backend_server + '/back/prestamo_cab/' + data.cod_prestamo, {}, { config_request })
                .then(res => {      
                    alert('Registro eliminado');                                   
                    this.mostrarPrestamos();
                })
                .catch((error) => {
                    alert('Error al eliminar registro o tiene libros prestados');   
                    console.log(error)
                }); 
            },
            eliminarPrestamoDet(data){
                var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
                axios.delete(this.backend_server + '/back/prestamo_det/' + data.cod_prestamo_det, {}, { config_request })
                .then(res => {                                       
                    this.mostrarPrestamosDet();
                })
                .catch((error) => {
                    alert('Error al eliminar registro o tiene libros prestados');   
                    console.log(error)
                }); 
            },
            editarPrestamo(data){
                this.nuevoPrestamo=data;
                this.btnGuardar=false;
                this.btnEditar=true;
                this.mostrarDiv=true;
                this.mostrarPrestamosDet();
                
            },
            agregarPrestamo(){
                this.btnGuardar=true;
                this.btnEditar=false;
                this.limpiarFormulario();
                this.mostrarDiv=false;
            },
            mostrarLibros(){
                axios.get(this.backend_server + "/back/libro")
                    .then(res => {
                     //   console.log(res.data);
                    this.dataLibros = res.data;
                });
            },
            mostrarPrestamos(){
                axios.get(this.backend_server + "/back/prestamo_cab")
                    .then(res => {
                     //console.log(res.data);
                    this.dataPrestamos = res.data;
                });
            },
            mostrarPrestamosDet(){
                axios.get(this.backend_server + "/back/prestamo_det/"+this.nuevoPrestamo.cod_prestamo)
                    .then(res => {
                    console.log(res.data);
                    this.dataDetalles = res.data;
                });
            },
            mostrarPersonas(){
                axios.get(this.backend_server + "/back/persona")
                    .then(res => {
                     //   console.log(res.data);
                    this.dataPersonas = res.data;
                });
            },
            mostrarBibliotecarios(){
                axios.get(this.backend_server + "/back/persona")
                    .then(res => {
                     //   console.log(res.data);
                    this.dataBibliotecarios = res.data;
                });
            }
        },
        created() {
            this.mostrarPersonas();
            this.mostrarBibliotecarios();
            this.mostrarLibros();
            this.mostrarPrestamos();
        },
        components: {  }
    }
    
    </script>