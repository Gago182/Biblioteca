
<template>
    <div class="container-fluid full-height-container bg-white">
        <br>
        <div class="card">
        <div class="card-header">
            <div class="row justify-content-between">
                    <div class="col-5">
                        <h5 class="card-title">Reporte de Prestamos</h5>
                    </div>
                    <div class="col-7">
                        <div class="input-group mb-3">
                            <select class="form-select form-select-sm" v-model="selectedOption" id="cboTipoTesis" @change="seleccionarReporte">
                                <option selected value="0">Seleccione su Reporte</option>
                                <option value="1">Ranking de libros mas solicitados</option>
                                <option value="2">Libros pendientes de devolución</option>
                            </select>
                            <button class="btn btn-outline-secondary" type="button" id="btnFiltrarReporte" @click="buscarReporte">Filtrar</button>
                        </div>
                        
                    </div>
                </div>
        </div>
        <div class="card-body">
            <table class="table">
            <thead>
                <tr>
                <th scope="col">Usuario</th>
                <th scope="col">Libro</th>
                <th scope="col">Cantidad</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for='data in dataLibros'>
                    <td>{{data.usuario}}</td>
                    <td>{{data.libro}}</td>
                    <td>{{ data.cantidad }}</td>
                </tr>
            </tbody>
            </table>  
        </div>
    
        </div>
    </div>
    
    
    </template>
    <script>
    import axios from "axios";
    export default{
        data() {
            return {
                selectedOption:"0",
                dataLibros: [],
                btnGuardar:false,
                backend_server: 'http://127.0.0.1:5000'
            };
        },
        mounted() {
            //this.obtenerFechaActual();
        },
        methods: {

            misLibros(selecOption){
                let urlReporte='';
                switch(selecOption){
                    case 1: urlReporte='/back/ranking-prestado';break;
                    case 2: urlReporte='/back/ranking-devuelto';break;
                    default: urlReporte='';break;
                }
                console.log(this.backend_server + urlReporte);
                axios.get(this.backend_server + urlReporte)
                    .then(res => {
                    this.dataLibros = res.data;
                    console.log(this.dataLibros);
                });
            },
            seleccionarReporte(event) {
                this.misLibros(parseInt(event.target.value));
                
            }
        },
        created() {
           
        },
        components: {  }
    }
    
    </script>