interface MapPoint {
  id: number;
  position: [number, number]; // [Latitude, Longitude]
  message: string;
}

// Your mapable list
const locations: MapPoint[] = [
  { id: 1, position: [23.8103, 90.4125], message: "Dhaka Server Hub" },
  { id: 2, position: [23.794, 90.404], message: "Banani Branch" },
  { id: 3, position: [23.746, 90.377], message: "Dhanmondi Node" },
];

export default locations;