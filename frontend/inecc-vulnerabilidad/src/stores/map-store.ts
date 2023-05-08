import { defineStore } from 'pinia';

export const useMapStore = defineStore('map-store', {
  state: () => ({
    counter: 0,
    mapasBase: [
      {value: 'mapbox-streets-v11', label: 'Mapbox Streets', bgcolor: '#75cff0', url: 'https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibml6aGlzYWViYSIsImEiOiJjanZwZXNpeWYwZDcxNDlwOXVhejg1Yno3In0.kqEaQSkVaFMpKKtx0FyNRA'},
      {value: 'mapbox-outdoors-v11', label: 'Mapbox Outdoors', bgcolor: '#75cff0', url: 'https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibml6aGlzYWViYSIsImEiOiJjanZwZXNpeWYwZDcxNDlwOXVhejg1Yno3In0.kqEaQSkVaFMpKKtx0FyNRA'},
      {value: 'mapbox-light-v10', label: 'Mapbox Light', bgcolor: '#cad2d3', url: 'https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibml6aGlzYWViYSIsImEiOiJjanZwZXNpeWYwZDcxNDlwOXVhejg1Yno3In0.kqEaQSkVaFMpKKtx0FyNRA'},
      {value: 'mapbox-dark-v10', label: 'Mapbox Dark', bgcolor: '#191a1a', url: 'https://api.mapbox.com/styles/v1/mapbox/dark-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibml6aGlzYWViYSIsImEiOiJjanZwZXNpeWYwZDcxNDlwOXVhejg1Yno3In0.kqEaQSkVaFMpKKtx0FyNRA'},
      {value: 'mapbox-satellite-v9', label: 'Mapbox Satellite', bgcolor: '#050c16', url: 'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibml6aGlzYWViYSIsImEiOiJjanZwZXNpeWYwZDcxNDlwOXVhejg1Yno3In0.kqEaQSkVaFMpKKtx0FyNRA'},
      {value: 'mapbox-satellite-streets-v11', label: 'Mapbox Satellite Streets', bgcolor: '#050c16', url: 'https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v11/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibml6aGlzYWViYSIsImEiOiJjanZwZXNpeWYwZDcxNDlwOXVhejg1Yno3In0.kqEaQSkVaFMpKKtx0FyNRA'},
    ],
    mapaBase: 'mapbox-streets-v11',
    capasMapa: [
      {value: 'estados', label: 'Estados', type: 'wms', url: 'https://gs.maptitud.xyz/geoserver/CONFLICTOS/wms?',
        layers: 'CONFLICTOS:estados', visible: true, children: [{}],
        attribution: ', <a href="https://www.inegi.gob.mx" target="_blank">INEGI</a>',
        opacity: 1, permanent: true,
        server_type: 'geoserver',
        format: 'image/png8',
        params: {
          crs: 'EPSG:4326',
        }
      },
      {value: 'municipios', label: 'Municipios', type: 'wms', url: 'https://gs.maptitud.xyz/geoserver/CONFLICTOS/wms?',
        layers: 'CONFLICTOS:municipios', visible: false, children: [{}],
        attribution: ', <a href="https://www.inegi.gob.mx" target="_blank">INEGI</a>',
        opacity: 0.8, permanent: true,
        server_type: 'geoserver',
        format: 'image/png8',
        params: {
          crs: 'EPSG:4326',
        }
      }
      ],
    capaSeleccionada: 'estados',
    showDrawerCapas: false,
  }),
  getters: {
    doubleCount: (state) => state ? 1 : 0,
  },
  actions: {
    increment() {
      this.counter++;
    },
  },
});
