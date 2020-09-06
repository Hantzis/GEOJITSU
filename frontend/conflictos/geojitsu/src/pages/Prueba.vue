<template>
  <q-page class="q-pa-sm">
    <h1>Titulo</h1>
    <p>esto es una prueba</p>
    <div class="row " style="height: 100px; background-color: red;">
      <div class="col-auto">
        <div class="row">a</div>
        <div class="row">
          b
        </div>
        <div class="row" style="flex-grow: 1">c</div>
      </div>


      <div class="col-auto" style="min-height:300px; display:flex; flex:1; flex-direction:column;">
        <div class=" panel">
          <div class=" panel-header">
            I'm a header
          </div>
          <div class="panel-main">
            Main content
          </div>
          <div class=" panel-footer">
            I'm a footer
          </div>
        </div>
      </div>
    </div>

  </q-page>
</template>

<script>
export default {
  name: "Prueba"
}
</script>

<style>
.panel {
  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: column;
  flex-grow: 1;

  justify-content: flex-start; /* align items in Main Axis */
  align-items: stretch; /* align items in Cross Axis */
  align-content: stretch; /* Extra space in Cross Axis */

  background-color: #00acc1;
}

.panel-header {
  flex: 0 1 auto;
  /*max-height: fit-content;*/
}

.panel-main {
  /*margin-bottom: auto;*/
  display: flex;
  flex-direction: column;
  flex: 1; /* same as flex: 1 1 auto; */
  justify-content: flex-start; /* align items in Main Axis */
  align-items: stretch; /* align items in Cross Axis */
  align-content: stretch; /* Extra space in Cross Axis */
  background-color: #0d47a1;
}

.panel-footer {
  margin-top: auto;
  max-height: fit-content;
}

.q-pa-md {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
