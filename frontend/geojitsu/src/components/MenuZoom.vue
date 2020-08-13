<template>
  <div class="menu-zoom">
    <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle" self="bottom middle">
      Zoom general
    </q-tooltip>
    <q-btn-dropdown
      split
      flat
      glossy
      dense
      color="primary"
      text-color="white"
      backgound-color="white"
      icon="mdi-arrow-expand-all"
      @click="onMainClick"
      class="no-border-radius"
    >
      <q-list dense bordered>
        <q-item dense clickable v-close-popup @click="onItemClick">
          <q-item-section side style="padding-right: 6px;">
            <q-icon name="mdi-arrow-expand-all" color="primary"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Zoom general</q-item-label>
          </q-item-section>
        </q-item>
        <q-item dense clickable v-close-popup @click="onItemClick">
          <q-item-section side style="padding-right: 6px;">
            <q-icon name="mdi-layers-search" color="primary"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Zoom a la capa activa</q-item-label>
          </q-item-section>
        </q-item>
        <q-item dense clickable v-close-popup @click="onItemClick">
          <q-item-section side style="padding-right: 6px;">
            <q-icon name="mdi-select-search" color="primary"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Zoom a la selección</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-btn-dropdown>
  </div>
</template>

<script>
  export default {
    name: "MenuZoom",
    data() {
      return {}
    },
    methods: {
      onMainClick() {
        console.log("hola")
        return
      }
    }
  }
</script>


<style lang="css" scoped>
  .menu-zoom {
    margin-top: 4px;
  }
  .q-item.q-item-type.row.no-wrap.q-item--clickable.q-link.cursor-pointer.q-focusable.q-hoverable.q-item--dense {
    padding: 4px 12px 4px 4px;
  }

  .dropdown-sinpadding {
    margin: -10px -4px;
  }

  .dropdown-sinpadding >>> .material-icons.q-icon.notranslate.q-btn-dropdown__arrow {
    width: 6px;
    font-size: 1.5em;
    margin-right: 1px;
  }
</style>

