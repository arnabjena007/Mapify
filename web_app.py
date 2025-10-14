#!/usr/bin/env python3
"""
Flask web application for Kolkata City Pathfinder
Provides REST API endpoints for the web interface
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
import sys
from kolkata_pathfinder import KolkataPathfinder
import traceback

app = Flask(__name__)
CORS(app)

# Global pathfinder instance
pathfinder = None

def initialize_pathfinder():
    """Initialize the pathfinder with Kolkata data"""
    global pathfinder
    try:
        print("🏙️  Initializing Kolkata pathfinder...")
        pathfinder = KolkataPathfinder()
        pathfinder.load_kolkata_data()
        print("✅ Pathfinder initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Error initializing pathfinder: {e}")
        traceback.print_exc()
        return False

@app.route('/')
def index():
    """Serve the main web application"""
    return render_template('index.html')

@app.route('/api/landmarks')
def get_landmarks():
    """Get all available Kolkata landmarks"""
    try:
        if pathfinder is None:
            return jsonify({'error': 'Pathfinder not initialized'}), 500
        
        landmarks = []
        for name, coords in pathfinder.landmarks.items():
            landmarks.append({
                'name': name,
                'latitude': coords[0],
                'longitude': coords[1]
            })
        
        return jsonify({'landmarks': landmarks})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/geocode', methods=['POST'])
def geocode_address():
    """Geocode an address to coordinates"""
    try:
        if pathfinder is None:
            return jsonify({'error': 'Pathfinder not initialized'}), 500
        
        data = request.get_json()
        address = data.get('address', '').strip()
        
        if not address:
            return jsonify({'error': 'Address is required'}), 400
        
        # Try to geocode the address
        coords = pathfinder.geocode_kolkata_address(address)
        
        return jsonify({
            'latitude': coords[0],
            'longitude': coords[1],
            'address': address
        })
    except Exception as e:
        return jsonify({'error': f'Could not geocode address: {str(e)}'}), 400

@app.route('/api/shortest-path', methods=['POST'])
def compute_shortest_path():
    """Compute shortest path between two points"""
    try:
        if pathfinder is None:
            return jsonify({'error': 'Pathfinder not initialized'}), 500
        
        data = request.get_json()
        
        # Extract coordinates
        start_lat = float(data.get('start_lat'))
        start_lon = float(data.get('start_lon'))
        end_lat = float(data.get('end_lat'))
        end_lon = float(data.get('end_lon'))
        
        start_coords = (start_lat, start_lon)
        end_coords = (end_lat, end_lon)
        
        # Compute shortest path
        path_result = pathfinder.compute_shortest_path(start_coords, end_coords)
        
        # Format response
        response = {
            'path_coordinates': path_result['path_coordinates'],
            'distance_meters': path_result['distance_meters'],
            'distance_km': round(path_result['distance_meters'] / 1000, 2),
            'path_nodes_count': len(path_result['path_nodes']),
            'computation_time': round(path_result['compute_time'], 3),
            'start_coords': start_coords,
            'end_coords': end_coords
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': f'Could not compute path: {str(e)}'}), 400

@app.route('/api/stats')
def get_stats():
    """Get Kolkata network statistics"""
    try:
        if pathfinder is None:
            return jsonify({'error': 'Pathfinder not initialized'}), 500
        
        stats = pathfinder.get_kolkata_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'pathfinder_initialized': pathfinder is not None
    })

if __name__ == '__main__':
    print("🚀 Starting Kolkata Pathfinder Web App...")
    
    # Initialize pathfinder
    if initialize_pathfinder():
        print("🌐 Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=8080)
    else:
        print("❌ Failed to initialize pathfinder. Exiting.")
        sys.exit(1)
