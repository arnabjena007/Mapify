# Kolkata City Pathfinder - Web Application

A modern, interactive web application for finding shortest paths in Kolkata using Dijkstra's algorithm.

##  **Web Application Features**

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

##  **Quick Start**

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

## **How to Use**

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

##  **Built-in Landmarks**

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

