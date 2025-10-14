# Kolkata City Pathfinder - Web Application

A modern, interactive web application for finding shortest paths in Kolkata using Dijkstra's algorithm.

## 🌐 **Web Application Features**

### **Interactive Map Interface**
- **Leaflet-based map** with OpenStreetMap tiles
- **Click-to-select** locations directly on the map
- **Real-time path visualization** with highlighted routes
- **Landmark markers** for famous Kolkata locations
- **Responsive design** that works on desktop and mobile

### **User-Friendly Input Methods**
1. **Text Input**: Enter addresses or location names
2. **Landmark Selection**: Choose from 15 famous Kolkata landmarks
3. **Map Clicking**: Click directly on the map to set locations
4. **Coordinate Input**: Enter precise latitude/longitude coordinates

### **Real-Time Results**
- **Distance calculation** in kilometers
- **Path segments count** showing route complexity
- **Computation time** demonstrating algorithm efficiency
- **Interactive path display** on the map with popups

## 🚀 **Quick Start**

### **Installation**
```bash
# Activate virtual environment
source ~/deeponenv/bin/activate

# Install web dependencies
pip install flask flask-cors

# Or install all dependencies
pip install -r requirements.txt
```

### **Start the Web Application**
```bash
# Method 1: Using startup script (recommended)
python start_webapp.py

# Method 2: Direct Flask app
python web_app.py
```

### **Access the Application**
1. Open your web browser
2. Go to: **http://localhost:8080**
3. Start planning routes in Kolkata!

## 🎮 **How to Use**

### **Step 1: Set Start Location**
- **Type an address** in the "Start Location" field
- **Select a landmark** from the dropdown menu
- **Click on the map** to set coordinates
- **Enter coordinates** directly (format: lat, lon)

### **Step 2: Set End Location**
- Use any of the same methods as Step 1
- The map will show both start (green) and end (red) markers

### **Step 3: Find Shortest Path**
- Click the **"Find Shortest Path"** button
- Watch as Dijkstra's algorithm computes the optimal route
- See the path highlighted in red on the map

### **Step 4: View Results**
- **Distance**: Total route distance in kilometers
- **Path Segments**: Number of road segments in the route
- **Computation Time**: How fast the algorithm worked
- **Interactive Path**: Click on the path for more details

## 🏛️ **Built-in Landmarks**

The web app includes 15 famous Kolkata landmarks:

| Landmark | Type | Area |
|----------|------|------|
| Victoria Memorial | Monument | Central Kolkata |
| Howrah Bridge | Bridge | Howrah |
| Eden Gardens | Stadium | Central Kolkata |
| Dakshineswar Temple | Temple | North Kolkata |
| Kalighat Temple | Temple | South Kolkata |
| Salt Lake Stadium | Stadium | Salt Lake |
| Park Street | Commercial | Central Kolkata |
| New Market | Shopping | Central Kolkata |
| Sealdah Station | Railway | Central Kolkata |
| Howrah Station | Railway | Howrah |
| Esplanade | Business | Central Kolkata |
| Maidan | Park | Central Kolkata |
| Science City | Museum | East Kolkata |
| Birla Planetarium | Planetarium | Central Kolkata |
| Indian Museum | Museum | Central Kolkata |

## 🛠️ **Technical Architecture**

### **Backend (Python/Flask)**
- **Flask REST API** with CORS support
- **KolkataPathfinder class** integration
- **Real-time geocoding** with error handling
- **Dijkstra's algorithm** via NetworkX
- **JSON responses** for all API endpoints

### **Frontend (HTML/CSS/JavaScript)**
- **Responsive design** with CSS Grid and Flexbox
- **Leaflet.js** for interactive mapping
- **Modern JavaScript** with async/await
- **Font Awesome icons** for visual appeal
- **CSS animations** for smooth user experience

### **API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve main web application |
| `/api/landmarks` | GET | Get all Kolkata landmarks |
| `/api/geocode` | POST | Convert address to coordinates |
| `/api/shortest-path` | POST | Compute shortest path |
| `/api/stats` | GET | Get network statistics |
| `/health` | GET | Health check endpoint |

## 📱 **User Interface**

### **Control Panel**
- **Location inputs** with autocomplete suggestions
- **Landmark dropdowns** for easy selection
- **Action buttons** with loading states
- **Results display** with route information
- **Network statistics** showing graph size

### **Interactive Map**
- **Zoom and pan** controls
- **Marker clustering** for landmarks
- **Path highlighting** with custom styling
- **Popup information** for all elements
- **Responsive layout** for mobile devices

## 🎨 **Visual Design**

### **Color Scheme**
- **Primary**: Blue gradient (#3498db to #2980b9)
- **Success**: Green (#27ae60) for start points
- **Danger**: Red (#e74c3c) for end points and paths
- **Info**: Light blue (#3498db) for landmarks
- **Background**: Purple gradient (#667eea to #764ba2)

### **Typography**
- **Font Family**: Segoe UI, system fonts
- **Headers**: Bold, larger sizes with icons
- **Body Text**: Clean, readable font sizes
- **Monospace**: For coordinates display

## 🔧 **Configuration**

### **Map Settings**
```javascript
// Default map center (Kolkata)
center: [22.5726, 88.3639]
zoom: 12
maxZoom: 18
```

### **Server Settings**
```python
# Flask configuration
host: '0.0.0.0'
port: 8080
debug: False  # Set to True for development
```

## 📊 **Performance**

### **Typical Response Times**
- **Landmark loading**: < 100ms
- **Geocoding**: 200-500ms
- **Path computation**: 100-400ms
- **Map rendering**: < 200ms

### **Network Statistics**
- **Nodes**: 35,696 intersections
- **Edges**: 90,936 road segments
- **Coverage**: Full Kolkata metropolitan area
- **Data size**: ~21MB cached OSM data

## 🐛 **Error Handling**

### **User-Friendly Error Messages**
- **Geocoding failures**: "Could not find that address"
- **Path computation errors**: "No route found between points"
- **Network issues**: "Connection error, please try again"
- **Invalid input**: "Please enter valid coordinates"

### **Graceful Degradation**
- **Offline landmarks** if API fails
- **Manual coordinate entry** if geocoding fails
- **Error modals** with clear explanations
- **Retry mechanisms** for network requests

## 🚀 **Deployment Options**

### **Local Development**
```bash
python start_webapp.py
# Access at http://localhost:8080
```

### **Production Deployment**
```bash
# Using Gunicorn (recommended)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app

# Using Docker
docker build -t kolkata-pathfinder .
docker run -p 5000:5000 kolkata-pathfinder
```

## 🎯 **Use Cases**

### **Tourism Planning**
- Plan routes between tourist attractions
- Estimate travel distances and times
- Discover nearby landmarks

### **Navigation Assistance**
- Find optimal routes in Kolkata traffic
- Compare different path options
- Get precise distance measurements

### **Educational Purposes**
- Demonstrate Dijkstra's algorithm visually
- Understand graph theory concepts
- Learn about urban transportation networks

### **Research and Analysis**
- Analyze Kolkata's road network structure
- Study shortest path algorithms
- Export route data for further analysis

## 🎉 **Ready to Navigate Kolkata!**

The web application is now ready to help you find the shortest paths through the City of Joy with an intuitive, modern interface! 🏙️🗺️

**Start the app and begin exploring Kolkata's streets with the power of Dijkstra's algorithm!**
