<template>
    <div class="col-auto">
      <div class="row">
        <div class="col">
          <barra-herramientas-principal />
        </div>
      </div>
      <!-- <div class="row" style="padding: 20px;"></div> -->
      <div class="row justify-between">
        <div class="col-auto">
          <div class="row q-px-sm" />
        </div>
        <div class="col-auto">
          Principal
        </div>
        <div class="col-auto">
          <q-btn dense size="xs" flat icon="mdi-arrow-bottom-right" />
        </div>
      </div>
    </div>
</template>

<script>
  import BarraHerramientasPrincipal from "./BarraHerramientasPrincipal";
  export default {
    name: "MapaBloquePrincipal",
    components: {BarraHerramientasPrincipal}
  }
</script>
