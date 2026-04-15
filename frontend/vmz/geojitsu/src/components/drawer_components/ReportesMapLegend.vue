<template>
  <div class="legend">

    <q-list bordered dense>

      <q-expansion-item
        v-for="group in groupedItems"
        :key="group.key"
        dense
        expand-separator
        default-opened
        :label="group.label"
        header-class="text-weight-bold"
      >

        <q-item
          v-for="item in group.items"
          :key="item.key"
          dense
        >
          <q-item-section avatar>
            <div
              class="legend-symbol"
              :class="item.tipo === 'Situaciones' ? 'square' : 'circle'"
              :style="{
                backgroundColor: item.fill,
                borderColor: item.stroke
              }"
            ></div>
          </q-item-section>

          <q-item-section>
            {{ item.nombre }}
          </q-item-section>

        </q-item>

      </q-expansion-item>

    </q-list>

  </div>
</template>

<script>
export default {
  name: 'ReportesMapLegend',

  props: {
    servicios: {type: Array, required: true},
    situaciones: {type: Array, required: true},

    strokeServicios: {type: Object, required: true},
    strokeSituaciones: {type: Object, required: true},
    filtro: Object
  },

  computed: {

    groupedItems() {
      const estatusList = ['Abierto', 'Atendiendo', 'Resuelto']
      const groups = []

      // 🔎 aplicar filtro (CORRECTO)
      let serviciosFiltrados = []
      let situacionesFiltradas = []

      if (this.filtro && this.filtro.tipo === 'Servicios') {
        if (this.filtro.servicio) {
          serviciosFiltrados = this.servicios.filter(s => s.id === this.filtro.servicio)
        } else {
          serviciosFiltrados = this.servicios
        }
      } else if (this.filtro && this.filtro.tipo === 'Situaciones') {
        if (this.filtro.situacion) {
          situacionesFiltradas = this.situaciones.filter(s => s.id === this.filtro.situacion)
        } else {
          situacionesFiltradas = this.situaciones
        }
      }

      // 👉 sin filtro → todo
      else {
        serviciosFiltrados = this.servicios
        situacionesFiltradas = this.situaciones
      }

      // 🔴 SERVICIOS
      for (const estatus of estatusList) {
        if (serviciosFiltrados.length === 0) continue

        const items = serviciosFiltrados.map(s => ({
          key: `serv-${s.id}-${estatus}`,
          tipo: 'Servicios',
          id: s.id,
          nombre: s.nombre,
          estatus,
          stroke: this.strokeServicios[s.id] || '#000',
          fill: this.getFill(estatus)
        }))

        groups.push({
          key: `servicios-${estatus}`,
          label: `Servicios (${estatus})`,
          items
        })
      }

      // 🔲 SITUACIONES
      for (const estatus of estatusList) {
        if (situacionesFiltradas.length === 0) continue

        const items = situacionesFiltradas.map(s => ({
          key: `sit-${s.id}-${estatus}`,
          tipo: 'Situaciones',
          id: s.id,
          nombre: s.nombre,
          estatus,
          stroke: this.strokeSituaciones[s.id] || '#000',
          fill: this.getFill(estatus)
        }))

        groups.push({
          key: `situaciones-${estatus}`,
          label: `Situaciones (${estatus})`,
          items
        })
      }

      return groups
    }
  },

  methods: {

    // 🎨 EXACTAMENTE alineado con tu mapa (sin semáforo explícito)
    getFill(estatus) {
      if (estatus === 'Atendiendo') return '#ffffff'  // blanco
      if (estatus === 'Resuelto') return '#00ff00'    // verde

      return '#f0ff00' // 👈 amarillo para Abierto (coincide mejor con mapa)
    }

  }
}
</script>

<style scoped lang="css">
.legend {
  font-size: 12px;
}

.legend-group {
  margin-bottom: 10px;
}

.legend-title {
  font-weight: bold;
  margin-bottom: 4px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 3px;
}

/* 🔴 ESTE ES EL IMPORTANTE */
.legend-symbol {
  display: inline-block;
  width: 14px;
  height: 14px;
  min-width: 14px;
  border: 2px solid;
  margin-right: 6px;
  box-sizing: border-box;
}

/* círculo */
.legend-symbol.circle {
  border-radius: 50%;
}

/* cuadrado (rotado como en SLD) */
.legend-symbol.square {
  transform: rotate(0deg);
}
</style>
