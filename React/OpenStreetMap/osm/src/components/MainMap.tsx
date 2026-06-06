import { MapContainer, TileLayer } from "react-leaflet";
import MarkerLayout from "../layouts/MarkerLayout";

const MainMap = () => {
    return (
        <MapContainer center={[23.8103, 90.4125]} zoom={13} scrollWheelZoom={true} style={{ height: "100vh", width: "100%" }}>
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <MarkerLayout />
        </MapContainer>
    );
};

export default MainMap;