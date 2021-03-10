export default function () {
  return {
    //
    GISRibbonIsOpen: true,
    drawerCapas: true,
    mapaBase: "google-maps",
    mapasBase: [
      {value: "google-maps", label: "Google Maps", bgcolor: " #8ab4f8", url: "https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}"},
      {value: "google-satellite", label: "Google Satellite", bgcolor: "#2b3c70", url: "http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}"},
      {value: "google-hybrid", label: "Google Hybrid", bgcolor: "#2b3c70", url: "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"},
      {value: "google-terrain", label: "Google Terrain", bgcolor: "#000000", url: "https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}"},
      {value: "OpenStreetMap-Standard", label: "OpenStreetMap Standard", bgcolor: "#aad3df", url: "http://a.tile.openstreetmap.org/{z}/{x}/{y}.png"},
    ],
    capaSeleccionada: "conflictos",
    capasMapa: [
      {value: "estados", label: "Estados", type: "wms", url: "https://gs.maptitud.xyz/geoserver/CONFLICTOS/wms?",
        layers: "CONFLICTOS:estados", visible: false, children: [{}],
        attribution: ", <a href='http://www.inegi.gob.mx' target='_blank'>INEGI</a>",
        opacity: 1, permanent: true,
        server_type: "geoserver",
        format: "image/png8",
        params: {
          crs: "EPSG:4326",
        }
      },
      {value: "municipios", label: "Municipios", type: "wms", url: "https://gs.maptitud.xyz/geoserver/CONFLICTOS/wms?",
        layers: "CONFLICTOS:municipios", visible: false, children: [{}],
        attribution: ", <a href='http://www.inegi.gob.mx' target='_blank'>INEGI</a>",
        opacity: 0.8, permanent: true,
        server_type: "geoserver",
        format: "image/png8",
        params: {
          crs: "EPSG:4326",
        }
      },
      {value: "anpnov17gw", label: "Áreas naturales protegidas", type: "wms", url: "https://gs.maptitud.xyz/geoserver/CONFLICTOS/wms?",
        layers: "CONFLICTOS:anpnov17gw", visible: false, children: [{}],
        attribution: ", <a href='http://www.inegi.gob.mx' target='_blank'>INEGI</a>",
        opacity: 0.4, permanent: true,
        server_type: "geoserver",
        format: "image/png8",
        params: {
          crs: "EPSG:4326",
        }
      },
      {value: "cue250kgw", label: "Cuencas", type: "wms", url: "https://gs.maptitud.xyz/geoserver/CONFLICTOS/wms?",
        layers: "CONFLICTOS:cue250kgw", visible: false, children: [{}],
        attribution: ", <a href='http://www.inegi.gob.mx' target='_blank'>INEGI</a>",
        opacity: 0.4, permanent: true,
        server_type: "geoserver",
        format: "image/png8",
        params: {
          crs: "EPSG:4326",
        }
      },
      {value: "ecort08gw", label: "Ecorregiones", type: "wms", url: "https://gs.maptitud.xyz/geoserver/CONFLICTOS/wms?",
        layers: "CONFLICTOS:ecort08gw", visible: false, children: [{}],
        attribution: ", <a href='http://www.inegi.gob.mx' target='_blank'>INEGI</a>",
        opacity: 0.4, permanent: true,
        server_type: "geoserver",
        format: "image/png8",
        params: {
          crs: "EPSG:4326",
        }
      },
      {value: "hidro4mgw", label: "Corrientes de agua", type: "wms", url: "https://gs.maptitud.xyz/geoserver/CONFLICTOS/wms?",
        layers: "CONFLICTOS:hidro4mgw", visible: false, children: [{}],
        attribution: ", <a href='http://www.inegi.gob.mx' target='_blank'>INEGI</a>",
        opacity: 0.9, permanent: true,
        server_type: "geoserver",
        format: "image/png8",
        params: {
          crs: "EPSG:4326",
        }
      },
      {value: "conflictos", label: "Conflictos Socioambientales", type: "vector", opacity: 1,
        server_type: "geojson", permanent: true,
        url: "https://conflictossocioambientales.iies.unam.mx/back/api/v1/conflicto-geojson/",
        features: [],
        attribution: ", <a href='http://www.iies.unam.mx' target='_blank'>IIES</a> (UNAM)",
        visible: false, children: [{}],
      },
    ]
  }
}
