export default function () {
  return {
    //
    GISRibbonIsOpen: true,
    drawerCapas: true,
    mapaBase: "google-maps",
    mapasBase: [
      {value: "google-maps", label: "Google Maps", bgcolor: "#75cff0", url: "https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}"},
      {value: "google-satellite", label: "Google Satellite", bgcolor: "#75cff0", url: "http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}"},
      {value: "google-hybrid", label: "Google Hybrid", bgcolor: "#cad2d3", url: "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"},
      {value: "google-terrain", label: "Google Terrain", bgcolor: "#191a1a", url: "https://mt1.google.com/vt/lyrs=t&x={x}&y={y}&z={z}"},
      {value: "OpenStreetMap-Standard", label: "OpenStreetMap Standard", bgcolor: "#191a1a", url: "http://a.tile.openstreetmap.org/{z}/{x}/{y}.png"},
    ],
    capaSeleccionada: "zapopan",
    capasMapa: [
      {
        value: "colonias_zapopan", label: "Colonias Zapopan", type: "wms",
        url: "https://catalina.maptitud.xyz/geoserver/wms?",
        layers: "IMMZIS:zen_colonias_zapopan", visible: true, children: [{}],
        attribution: ", <a href='http://www.ine.gob.mx' target='_blank'>INE</a>",
        opacity: 1.0, permanent: true,
        server_type: "geoserver",
        format: "image/png8",
        tiled: false,
        params: {
          crs: "EPSG:4326",
          cql_filter: null,
        }
      },
      {
        value: "reportes", label: "Reportes", type: "wms",
        url: "https://catalina.maptitud.xyz/geoserver/wms?",
        layers: "IMMZIS:zen_reportes", visible: true, children: [{}],
        attribution: ", <a href='http://www.inegi.gob.mx' target='_blank'>IMMZIS</a>",
        opacity: 1.0, permanent: true,
        server_type: "geoserver",
        format: "image/png8",
        tiled: true,
        params: {
          crs: "EPSG:4326",
          cql_filter: null,
        }
      },
    ],
    herramientaActiva: "info",
    userData: undefined,
    userGroups: [],
    mapkey: 0,
    isUserStaff: false,
  }
}
