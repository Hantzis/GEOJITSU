export default function () {
  return {
    //
    GISRibbonIsOpen: true,
    mapaBase: "mapbox-outdoors-v11",
    mapasBase: [
      {value: "mapbox-streets-v11", label: "Mapbox Streets", bgcolor: "#75cff0", url: "https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibml6aGlzYWViYSIsImEiOiJjanZwZXNpeWYwZDcxNDlwOXVhejg1Yno3In0.kqEaQSkVaFMpKKtx0FyNRA"},
      {value: "mapbox-outdoors-v11", label: "Mapbox Outdoors", bgcolor: "#75cff0", url: "https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibml6aGlzYWViYSIsImEiOiJjanZwZXNpeWYwZDcxNDlwOXVhejg1Yno3In0.kqEaQSkVaFMpKKtx0FyNRA"},
      {value: "mapbox-light-v10", label: "Mapbox Light", bgcolor: "#cad2d3", url: "https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibml6aGlzYWViYSIsImEiOiJjanZwZXNpeWYwZDcxNDlwOXVhejg1Yno3In0.kqEaQSkVaFMpKKtx0FyNRA"},
      {value: "mapbox-dark-v10", label: "Mapbox Dark", bgcolor: "#191a1a", url: "https://api.mapbox.com/styles/v1/mapbox/dark-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibml6aGlzYWViYSIsImEiOiJjanZwZXNpeWYwZDcxNDlwOXVhejg1Yno3In0.kqEaQSkVaFMpKKtx0FyNRA"},
      {value: "mapbox-satellite-v9", label: "Mapbox Satellite", bgcolor: "#050c16", url: "https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibml6aGlzYWViYSIsImEiOiJjanZwZXNpeWYwZDcxNDlwOXVhejg1Yno3In0.kqEaQSkVaFMpKKtx0FyNRA"},
      {value: "mapbox-satellite-streets-v11", label: "Mapbox Satellite", bgcolor: "#050c16", url: "https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v11/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibml6aGlzYWViYSIsImEiOiJjanZwZXNpeWYwZDcxNDlwOXVhejg1Yno3In0.kqEaQSkVaFMpKKtx0FyNRA"},
    ],
    capaActiva: "conflictos",
    capasMapa: [
      {value: "estados", label: "Estados", type: "wms", url: "https://gs.maptitude.xyz/geoserver/CONFLICTOS/wms?",
        layers: "CONFLICTOS:estados", visible: true,
        attribution: ", <a href='http://www.inegi.gob.mx' target='_blank'>INEGI</a>",
        opacity: 1,
        server_type: "geoserver",
        format: "image/png8",
        params: {
          crs: "EPSG:4326",
        }
      },
      {value: "municipios", label: "Municipios", type: "wms", url: "https://gs.maptitude.xyz/geoserver/CONFLICTOS/wms?",
        layers: "CONFLICTOS:municipios", visible: false,
        attribution: ", <a href='http://www.inegi.gob.mx' target='_blank'>INEGI</a>",
        opacity: 1,
        server_type: "geoserver",
        format: "image/png8",
        params: {
          crs: "EPSG:4326",
        }
      },
      {value: "anpnov17gw", label: "Áreas naturales protegidas", type: "wms", url: "https://gs.maptitude.xyz/geoserver/CONFLICTOS/wms?",
        layers: "CONFLICTOS:anpnov17gw", visible: false,
        attribution: ", <a href='http://www.inegi.gob.mx' target='_blank'>INEGI</a>",
        opacity: 0.4,
        server_type: "geoserver",
        format: "image/png8",
        params: {
          crs: "EPSG:4326",
        }
      },
      {value: "cue250kgw", label: "Cuencas", type: "wms", url: "https://gs.maptitude.xyz/geoserver/CONFLICTOS/wms?",
        layers: "CONFLICTOS:cue250kgw", visible: false,
        attribution: ", <a href='http://www.inegi.gob.mx' target='_blank'>INEGI</a>",
        opacity: 0.4,
        server_type: "geoserver",
        format: "image/png8",
        params: {
          crs: "EPSG:4326",
        }
      },
      {value: "ecort08gw", label: "Ecorregiones", type: "wms", url: "https://gs.maptitude.xyz/geoserver/CONFLICTOS/wms?",
        layers: "CONFLICTOS:ecort08gw", visible: false,
        attribution: ", <a href='http://www.inegi.gob.mx' target='_blank'>INEGI</a>",
        opacity: 0.4,
        server_type: "geoserver",
        format: "image/png8",
        params: {
          crs: "EPSG:4326",
        }
      },
      {value: "hidro4mgw", label: "Corrientes de agua", type: "wms", url: "https://gs.maptitude.xyz/geoserver/CONFLICTOS/wms?",
        layers: "CONFLICTOS:hidro4mgw", visible: true,
        attribution: ", <a href='http://www.inegi.gob.mx' target='_blank'>INEGI</a>",
        opacity: 1,
        server_type: "geoserver",
        format: "image/png8",
        params: {
          crs: "EPSG:4326",
        }
      },
      {value: "conflictos", label: "Conflictos Socioambientales", type: "vector", opacity: 1,
        url: "https://conflictossocioambientales.iies.unam.mx/conflictos/conflictos.geojson",
        attribution: ", <a href='http://www.iies.unam.mx' target='_blank'>IIES</a> (UNAM)",
        visible: false,
      },
    ]
  }
}
