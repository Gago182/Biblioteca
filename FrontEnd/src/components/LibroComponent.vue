
<template>
<div class="container-fluid full-height-container bg-white">
    <br>
    <div class="card">
    <div class="card-header">
        Registro de Libros <button type="button" class="btn btn-success btn-sm mx-2" @click="agregarLibro" data-bs-toggle="modal" data-bs-target="#modalLibro">Agregar<i class="fas fa-book mx-2 "></i></button>
    </div>
    <div class="card-body">
        <table class="table">
        <thead>
            <tr>
            <th scope="col">Cod Libro</th>
            <th scope="col">Titulo</th>
            <th scope="col">Materia</th>
            <th scope="col">Autor</th>
            <th scope="col">Descripcion</th>
            <th scope="col">Stock</th>
            <th scope="col">Acciones</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for='data in dataLibros'>
                <td>{{data.cod_libro}}</td>
                <td>{{data.titulo}}</td>
                <td>{{ data.materia }}</td>
                <td>{{ data.autor }}</td>
                <td>{{ data.descripcion }}</td>
                <td>{{ data.stock }}</td>
                <td>
                    <button  class="btn btn-success btn-sm" data-bs-toggle="modal" @click="editarLibro(data)" data-bs-target="#modalLibro" >
                        <i class="fas fa-pencil"></i>
                    </button>
                    <button  class="btn btn-danger btn-sm m-1" @click="eliminarLibro(data)">
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
<div class="modal fade" id="modalLibro" tabindex="-1" aria-hidden="true">
<div class="modal-dialog modal-lg modal-dialog-scrollable">
    <div class="modal-content">
    <div class="modal-header p-2 bg-dark text-white">
        <i class="bi bi-file-earmark-text" style="font-size: 1rem;"></i>
        <h5 class="modal-title m-1" id="exampleModalLabel">Libro</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
    </div>
    <div class="modal-body">
        <form>
                <div class="row bg-light">
                    <div class="col-12 mb-2">
                        <label class="form-label">Título :</label>
                        <input type="text" class="form-control form-control-sm"  v-model='nuevoLibro.titulo' placeholder="Ingrese título">
                    </div>
                    <div class="col-12 mb-2">
                        <label class="form-label">Autor :</label>
                        <input type="text" class="form-control form-control-sm"  v-model='nuevoLibro.autor' placeholder="Ingrese autor">
                    </div>
                    <div class="col-12 mb-2">
                        <label class="form-label">Descripción :</label>
                        <input type="text" class="form-control form-control-sm"  v-model='nuevoLibro.descripcion' placeholder="Ingrese descripción">
                    </div>
                    <div class="col-6 mb-2">
                        <label class="form-label">Materia :</label>
                        <input type="text" class="form-control form-control-sm"  v-model='nuevoLibro.materia' placeholder="Ingrese materia">
                    </div>
                    <div class="col-6 mb-2">
                        <label class="form-label">Stock :</label>
                        <input type="text" class="form-control form-control-sm"  v-model='nuevoLibro.stock' placeholder="">
                    </div>
                        
                </div>
            </form>
    </div>
    <div class="modal-footer">
        <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal" ref="cerrarModal">Cerrar</button>
        <button type="button" class="btn btn-primary btn-sm" v-if="btnGuardar" @click="guardarLibro">Guardar</button>
        <button type="button" class="btn btn-success btn-sm" v-if="btnEditar" @click="actualizarLibro">Editar</button>
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
            dataLibros: [],
            btnGuardar:false,
            btnEditar:false,
            nuevoLibro: {
                autor: "",
                cod_libro: 0,
                descripcion: "",
                materia: "",
                stock: 0,
                titulo: ""
            },
            backend_server: 'http://127.0.0.1:5000'
        };
    },
    mounted() {
        //this.obtenerFechaActual();
    },
    methods: {
        guardarLibro(){
            
            var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
            axios.post(this.backend_server + '/back/libro', this.nuevoLibro, { config_request })
            .then(res => {                                      
                alert('Registro guardado');
                this.mostarLibros();
                this.$refs.cerrarModal.click();
            })
            .catch((error) => {
                alert('Error al guardar registro');
                console.log(error)
            }); 

            
        },
        limpiarFormulario(){
            this.nuevoLibro= {
                autor: "",
                cod_libro: 0,
                descripcion: "",
                materia: "",
                stock: 0,
                titulo: ""
            }
        },
        actualizarLibro(){
            var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
            axios.put(this.backend_server + '/back/libro', this.nuevoLibro, { config_request })
            .then(res => {    
                alert('Registro actualizado');                                  
                console.log(this.nuevoLibro);
                this.mostarLibros();
                this.$refs.cerrarModal.click();
            })
            .catch((error) => {
                alert('Error al actualziar registro');
                console.log(error)
            });
            
            
        },
        
        eliminarLibro(data){
            var config_request={'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}
            axios.delete(this.backend_server + '/back/libro/' + data.cod_libro, {}, { config_request })
            .then(res => {      
                alert('Registro eliminado');                                   
                this.mostarLibros();
            })
            .catch((error) => {
                alert('Error al eliminar registro');   
                console.log(error)
            }); 
        },
        editarLibro(data){
            this.nuevoLibro=data;
            this.btnGuardar=false;
            this.btnEditar=true;
            
        },
        agregarLibro(){
            this.btnGuardar=true;
            this.btnEditar=false;
            this.limpiarFormulario();
        },
        mostarLibros(){
            axios.get(this.backend_server + "/back/libro")
                .then(res => {
                 //   console.log(res.data);
                this.dataLibros = res.data;
            });
        }
    },
    created() {
        this.mostarLibros();
    },
    components: {  }
}

</script>