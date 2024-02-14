<template>
  <div id="app">
    <div v-if="estadoLogin">
        <LoginComponent @actualizaLogin="actualizaLogin"></LoginComponent>
    </div>
    <div v-if="estadoPanel">
        <MenuComponent></MenuComponent>
        <router-view></router-view>
    </div>
  </div>
</template>

<script>
import MenuComponent from "./components/MenuComponent.vue";
import LoginComponent from "./components/LoginComponent.vue";
export default {
  data() {
        return {
          estadoLogin:true,
          messageError:false,
          login:true,
          estadoPanel:false,
        }
      },
      methods: {
        actualizaLogin(dato) {
          this.estadoLogin = dato;
          if(this.estadoLogin){
            this.estadoPanel=false;
          }else{
            this.estadoPanel=true;
            this.$router.push('/home');
          }
            
            
        },
  },   
  name: 'App',
  components: { MenuComponent,LoginComponent}
};
</script>