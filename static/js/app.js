// Kolkata City Pathfinder - JavaScript Application

class KolkataPathfinder {
    constructor() {
        this.map = null;
        this.startMarker = null;
        this.endMarker = null;
        this.pathLayer = null;
        this.landmarkMarkers = [];
        this.landmarks = [];
        this.startCoords = null;
        this.endCoords = null;
        
        this.init();
    }

    async init() {
        this.initializeMap();
        this.setupEventListeners();
        await this.loadLandmarks();
        await this.loadNetworkStats();
        this.hideMapLoading();
    }

    initializeMap() {
        // Initialize Leaflet map centered on Kolkata
        this.map = L.map('map').setView([22.5726, 88.3639], 12);

        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18
        }).addTo(this.map);

        // Add map click handler
        this.map.on('click', (e) => this.onMapClick(e));
    }

    setupEventListeners() {
        // Location input handlers
        document.getElementById('start-location').addEventListener('blur', () => {
            this.geocodeLocation('start');
        });

        document.getElementById('end-location').addEventListener('blur', () => {
            this.geocodeLocation('end');
        });

        // Landmark selection handlers
        document.getElementById('start-landmark').addEventListener('change', (e) => {
            this.selectLandmark('start', e.target.value);
        });

        document.getElementById('end-landmark').addEventListener('change', (e) => {
            this.selectLandmark('end', e.target.value);
        });

        // Button handlers
        document.getElementById('find-path-btn').addEventListener('click', () => {
            this.findShortestPath();
        });

        document.getElementById('clear-btn').addEventListener('click', () => {
            this.clearAll();
        });

        // Modal handlers
        document.getElementById('modal-close').addEventListener('click', () => {
            this.hideModal();
        });

        document.getElementById('modal-ok').addEventListener('click', () => {
            this.hideModal();
        });

        // Enter key handlers
        document.getElementById('start-location').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.geocodeLocation('start');
        });

        document.getElementById('end-location').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.geocodeLocation('end');
        });
    }

    async loadLandmarks() {
        try {
            const response = await fetch('/api/landmarks');
            const data = await response.json();
            
            if (data.landmarks) {
                this.landmarks = data.landmarks;
                this.populateLandmarkSelects();
                this.addLandmarkMarkers();
            }
        } catch (error) {
            console.error('Error loading landmarks:', error);
        }
    }

    async loadNetworkStats() {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();
            
            if (data.nodes) {
                document.getElementById('nodes-stat').textContent = data.nodes.toLocaleString();
                document.getElementById('edges-stat').textContent = data.edges.toLocaleString();
                document.getElementById('length-stat').textContent = `${Math.round(data.total_length_km)} km`;
            }
        } catch (error) {
            console.error('Error loading stats:', error);
            document.getElementById('nodes-stat').textContent = 'Error';
            document.getElementById('edges-stat').textContent = 'Error';
            document.getElementById('length-stat').textContent = 'Error';
        }
    }

    populateLandmarkSelects() {
        const startSelect = document.getElementById('start-landmark');
        const endSelect = document.getElementById('end-landmark');

        this.landmarks.forEach(landmark => {
            const option1 = new Option(landmark.name, landmark.name);
            const option2 = new Option(landmark.name, landmark.name);
            startSelect.add(option1);
            endSelect.add(option2);
        });
    }

    addLandmarkMarkers() {
        this.landmarks.forEach(landmark => {
            const marker = L.circleMarker([landmark.latitude, landmark.longitude], {
                radius: 6,
                fillColor: '#3498db',
                color: '#2980b9',
                weight: 2,
                opacity: 1,
                fillOpacity: 0.7
            }).addTo(this.map);

            marker.bindPopup(`<strong>🏛️ ${landmark.name}</strong><br>
                             Lat: ${landmark.latitude.toFixed(4)}<br>
                             Lon: ${landmark.longitude.toFixed(4)}`);

            this.landmarkMarkers.push(marker);
        });
    }

    selectLandmark(type, landmarkName) {
        if (!landmarkName) return;

        const landmark = this.landmarks.find(l => l.name === landmarkName);
        if (!landmark) return;

        const coords = [landmark.latitude, landmark.longitude];
        
        if (type === 'start') {
            this.startCoords = coords;
            document.getElementById('start-location').value = landmarkName;
            document.getElementById('start-coords').textContent = 
                `Coordinates: ${coords[0].toFixed(4)}, ${coords[1].toFixed(4)}`;
            this.updateStartMarker(coords);
        } else {
            this.endCoords = coords;
            document.getElementById('end-location').value = landmarkName;
            document.getElementById('end-coords').textContent = 
                `Coordinates: ${coords[0].toFixed(4)}, ${coords[1].toFixed(4)}`;
            this.updateEndMarker(coords);
        }

        // Clear the other landmark selection
        const otherSelect = type === 'start' ? 'end-landmark' : 'start-landmark';
        document.getElementById(otherSelect).value = '';
    }

    async geocodeLocation(type) {
        const input = document.getElementById(`${type}-location`);
        const address = input.value.trim();
        
        if (!address) return;

        try {
            const response = await fetch('/api/geocode', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ address: address })
            });

            const data = await response.json();

            if (response.ok) {
                const coords = [data.latitude, data.longitude];
                
                if (type === 'start') {
                    this.startCoords = coords;
                    this.updateStartMarker(coords);
                } else {
                    this.endCoords = coords;
                    this.updateEndMarker(coords);
                }

                document.getElementById(`${type}-coords`).textContent = 
                    `Coordinates: ${coords[0].toFixed(4)}, ${coords[1].toFixed(4)}`;

                // Clear landmark selection
                document.getElementById(`${type}-landmark`).value = '';

            } else {
                this.showError(`Geocoding failed: ${data.error}`);
            }
        } catch (error) {
            this.showError(`Error geocoding address: ${error.message}`);
        }
    }

    updateStartMarker(coords) {
        if (this.startMarker) {
            this.map.removeLayer(this.startMarker);
        }

        this.startMarker = L.marker(coords, {
            icon: L.divIcon({
                className: 'start-marker',
                html: '<i class="fas fa-play-circle" style="color: #27ae60; font-size: 24px;"></i>',
                iconSize: [30, 30],
                iconAnchor: [15, 15]
            })
        }).addTo(this.map);

        this.startMarker.bindPopup('<strong>🚩 Start Location</strong>');
        this.map.setView(coords, Math.max(this.map.getZoom(), 14));
    }

    updateEndMarker(coords) {
        if (this.endMarker) {
            this.map.removeLayer(this.endMarker);
        }

        this.endMarker = L.marker(coords, {
            icon: L.divIcon({
                className: 'end-marker',
                html: '<i class="fas fa-stop-circle" style="color: #e74c3c; font-size: 24px;"></i>',
                iconSize: [30, 30],
                iconAnchor: [15, 15]
            })
        }).addTo(this.map);

        this.endMarker.bindPopup('<strong>🏁 End Location</strong>');
        this.map.setView(coords, Math.max(this.map.getZoom(), 14));
    }

    onMapClick(e) {
        const coords = [e.latlng.lat, e.latlng.lng];
        
        // Determine which location to set based on what's missing
        if (!this.startCoords) {
            this.startCoords = coords;
            this.updateStartMarker(coords);
            document.getElementById('start-location').value = `${coords[0].toFixed(4)}, ${coords[1].toFixed(4)}`;
            document.getElementById('start-coords').textContent = 
                `Coordinates: ${coords[0].toFixed(4)}, ${coords[1].toFixed(4)}`;
            document.getElementById('start-landmark').value = '';
        } else if (!this.endCoords) {
            this.endCoords = coords;
            this.updateEndMarker(coords);
            document.getElementById('end-location').value = `${coords[0].toFixed(4)}, ${coords[1].toFixed(4)}`;
            document.getElementById('end-coords').textContent = 
                `Coordinates: ${coords[0].toFixed(4)}, ${coords[1].toFixed(4)}`;
            document.getElementById('end-landmark').value = '';
        } else {
            // Both are set, replace the end location
            this.endCoords = coords;
            this.updateEndMarker(coords);
            document.getElementById('end-location').value = `${coords[0].toFixed(4)}, ${coords[1].toFixed(4)}`;
            document.getElementById('end-coords').textContent = 
                `Coordinates: ${coords[0].toFixed(4)}, ${coords[1].toFixed(4)}`;
            document.getElementById('end-landmark').value = '';
        }
    }

    async findShortestPath() {
        if (!this.startCoords || !this.endCoords) {
            this.showError('Please set both start and end locations.');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch('/api/shortest-path', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    start_lat: this.startCoords[0],
                    start_lon: this.startCoords[1],
                    end_lat: this.endCoords[0],
                    end_lon: this.endCoords[1]
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.displayPath(data);
                this.showResults(data);
            } else {
                this.showError(`Path computation failed: ${data.error}`);
            }
        } catch (error) {
            this.showError(`Error computing path: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }

    displayPath(pathData) {
        // Remove existing path
        if (this.pathLayer) {
            this.map.removeLayer(this.pathLayer);
        }

        // Create path polyline
        const pathCoords = pathData.path_coordinates;
        this.pathLayer = L.polyline(pathCoords, {
            color: '#e74c3c',
            weight: 6,
            opacity: 0.8
        }).addTo(this.map);

        // Fit map to show entire path
        const group = new L.featureGroup([this.pathLayer, this.startMarker, this.endMarker]);
        this.map.fitBounds(group.getBounds().pad(0.1));

        // Add path popup
        const midpoint = Math.floor(pathCoords.length / 2);
        this.pathLayer.bindPopup(`
            <strong>🛣️ Shortest Path</strong><br>
            Distance: ${pathData.distance_km} km<br>
            Segments: ${pathData.path_nodes_count}<br>
            Algorithm: Dijkstra's
        `);
    }

    showResults(data) {
        document.getElementById('distance-result').textContent = `${data.distance_km} km`;
        document.getElementById('segments-result').textContent = data.path_nodes_count;
        document.getElementById('time-result').textContent = `${data.computation_time}s`;
        
        const resultsSection = document.getElementById('results-section');
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    clearAll() {
        // Clear coordinates
        this.startCoords = null;
        this.endCoords = null;

        // Clear inputs
        document.getElementById('start-location').value = '';
        document.getElementById('end-location').value = '';
        document.getElementById('start-landmark').value = '';
        document.getElementById('end-landmark').value = '';

        // Clear coordinate displays
        document.getElementById('start-coords').textContent = 'Coordinates: Not set';
        document.getElementById('end-coords').textContent = 'Coordinates: Not set';

        // Remove markers
        if (this.startMarker) {
            this.map.removeLayer(this.startMarker);
            this.startMarker = null;
        }
        if (this.endMarker) {
            this.map.removeLayer(this.endMarker);
            this.endMarker = null;
        }

        // Remove path
        if (this.pathLayer) {
            this.map.removeLayer(this.pathLayer);
            this.pathLayer = null;
        }

        // Hide results
        document.getElementById('results-section').style.display = 'none';

        // Reset map view
        this.map.setView([22.5726, 88.3639], 12);
    }

    showLoading() {
        document.getElementById('loading-overlay').style.display = 'flex';
        document.getElementById('find-path-btn').disabled = true;
    }

    hideLoading() {
        document.getElementById('loading-overlay').style.display = 'none';
        document.getElementById('find-path-btn').disabled = false;
    }

    hideMapLoading() {
        document.getElementById('map-loading').style.display = 'none';
    }

    showError(message) {
        document.getElementById('error-message').textContent = message;
        document.getElementById('error-modal').style.display = 'flex';
    }

    hideModal() {
        document.getElementById('error-modal').style.display = 'none';
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new KolkataPathfinder();
});
