export default function () {
  return {
    //
    GISRibbonIsOpen: true,
    drawerCapas: true,
    mapaBase: "google-maps",
    mapasBase: [
      {
        value: "google-maps",
        label: "Google Maps",
        bgcolor: "#75cff0",
        url: "https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}"
      },
      {
        value: "google-satellite",
        label: "Google Satellite",
        bgcolor: "#75cff0",
        url: "http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}"
      },
      {
        value: "google-hybrid",
        label: "Google Hybrid",
        bgcolor: "#cad2d3",
        url: "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"
      },
      {
        value: "google-terrain",
        label: "Google Terrain",
        bgcolor: "#191a1a",
        url: "https://mt1.google.com/vt/lyrs=t&x={x}&y={y}&z={z}"
      },
      {
        value: "OpenStreetMap-Standard",
        label: "OpenStreetMap Standard",
        bgcolor: "#191a1a",
        url: "http://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
      },
    ],
    capaSeleccionada: "zapopan",
    capasMapa: [
      {
        value: "reportes", label: "Reportes", type: "mvt",
        url: "https://api.zapopanentrenosotras.com/rest/v1/tiles/reportes/{z}/{x}/{y}.pbf",
        visible: true, children: [{}],
        attribution: ", <a href='http://www.zapopan.gob.mx' target='_blank'>IMMZIS</a>",
        opacity: 1.0,
        permanent: true,
        server_type: "mvt",
        params: {
          tipo: null,
          servicio: null,
          situacion: null
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
