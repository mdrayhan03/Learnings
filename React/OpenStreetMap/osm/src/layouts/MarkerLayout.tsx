import MarkerComponent from "../components/Marker";
import locations from "../services/MarkersInfo";

const MarkerLayout = () => {
    return (
        <>
            {locations.map((location) => (
                <MarkerComponent key={location.id} position={location.position} message={location.message} />
            ))}
        </>
    );
};

export default MarkerLayout;