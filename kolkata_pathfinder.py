#!/usr/bin/env python3
"""
Kolkata City Pathfinder using Dijkstra's Algorithm with OpenStreetMap data
Specialized demo for Kolkata, West Bengal, India
"""

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import folium
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import numpy as np
from typing import Tuple, List, Optional, Dict, Any
import time


class KolkataPathfinder:
    """
    A specialized pathfinder for Kolkata city street networks using OSM data
    """
    
    def __init__(self):
        """
        Initialize the Kolkata pathfinder
        """
        self.city_name = "Kolkata, West Bengal, India"
        self.graph = None
        self.gdf_nodes = None
        self.gdf_edges = None
        self.geocoder = Nominatim(user_agent="kolkata_pathfinder")
        
        # Configure OSMnx
        ox.settings.use_cache = True
        ox.settings.log_console = True
        
        # Famous Kolkata landmarks for easy reference
        self.landmarks = {
            "Victoria Memorial": (22.5448, 88.3426),
            "Howrah Bridge": (22.5851, 88.3468),
            "Eden Gardens": (22.5645, 88.3433),
            "Dakshineswar Temple": (22.6553, 88.3578),
            "Kalighat Temple": (22.5186, 88.3411),
            "Salt Lake Stadium": (22.5645, 88.4134),
            "Park Street": (22.5549, 88.3516),
            "New Market": (22.5569, 88.3511),
            "Sealdah Station": (22.5697, 88.3697),
            "Howrah Station": (22.5804, 88.3465),
            "Esplanade": (22.5697, 88.3501),
            "Maidan": (22.5526, 88.3496),
            "Science City": (22.5423, 88.3956),
            "Birla Planetarium": (22.5447, 88.3497),
            "Indian Museum": (22.5579, 88.3533)
        }
        
    def load_kolkata_data(self, network_type: str = "drive") -> None:
        """
        Download and process Kolkata street data from OpenStreetMap
        
        Args:
            network_type: Type of street network ('drive', 'walk', 'bike', 'all')
        """
        print(f"🏙️  Downloading street network for {self.city_name}...")
        start_time = time.time()
        
        try:
            # Download the street network for Kolkata
            self.graph = ox.graph_from_place(
                self.city_name, 
                network_type=network_type,
                simplify=True
            )
            
            # Convert to GeoDataFrames for easier manipulation
            self.gdf_nodes, self.gdf_edges = ox.graph_to_gdfs(self.graph)
            
            # Add edge lengths and travel times
            self.graph = ox.add_edge_speeds(self.graph)
            self.graph = ox.add_edge_travel_times(self.graph)
            
            load_time = time.time() - start_time
            print(f"✅ Loaded Kolkata street network:")
            print(f"   📍 {len(self.graph.nodes):,} intersections (nodes)")
            print(f"   🛣️  {len(self.graph.edges):,} road segments (edges)")
            print(f"   ⏱️  Load time: {load_time:.1f} seconds")
            
        except Exception as e:
            print(f"❌ Error loading Kolkata data: {e}")
            raise
    
    def show_landmarks(self) -> None:
        """Display available Kolkata landmarks"""
        print("\n🏛️  Famous Kolkata Landmarks:")
        print("=" * 50)
        for i, (name, coords) in enumerate(self.landmarks.items(), 1):
            print(f"{i:2d}. {name:<20} ({coords[0]:.4f}, {coords[1]:.4f})")
        print()
    
    def get_landmark_coords(self, landmark_name: str) -> Optional[Tuple[float, float]]:
        """Get coordinates for a landmark by name (case-insensitive)"""
        for name, coords in self.landmarks.items():
            if landmark_name.lower() in name.lower():
                return coords
        return None
    
    def geocode_kolkata_address(self, address: str) -> Tuple[float, float]:
        """
        Convert Kolkata address to latitude, longitude coordinates
        
        Args:
            address: Street address or location name in Kolkata
            
        Returns:
            Tuple of (latitude, longitude)
        """
        try:
            # First check if it's a landmark
            landmark_coords = self.get_landmark_coords(address)
            if landmark_coords:
                print(f"📍 Found landmark: {address} -> {landmark_coords}")
                return landmark_coords
            
            # Try geocoding with Kolkata context
            full_address = f"{address}, Kolkata, West Bengal, India"
            location = self.geocoder.geocode(full_address)
            
            if location:
                coords = (location.latitude, location.longitude)
                print(f"📍 Geocoded: {address} -> {coords}")
                return coords
            else:
                raise ValueError(f"Could not geocode address: {address}")
                
        except Exception as e:
            print(f"❌ Geocoding error: {e}")
            raise
    
    def find_nearest_node(self, lat: float, lon: float) -> int:
        """
        Find the nearest graph node to given coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Node ID of nearest node
        """
        return ox.nearest_nodes(self.graph, lon, lat)
    
    def compute_shortest_path(self, start_coords: Tuple[float, float], 
                            end_coords: Tuple[float, float],
                            weight: str = "length") -> Dict[str, Any]:
        """
        Compute shortest path between two points in Kolkata
        
        Args:
            start_coords: (latitude, longitude) of start point
            end_coords: (latitude, longitude) of end point
            weight: Edge attribute to use as weight ('length', 'travel_time')
            
        Returns:
            Dictionary containing path info, nodes, coordinates, and distance
        """
        if self.graph is None:
            raise ValueError("Kolkata data not loaded. Call load_kolkata_data() first.")
        
        print("\n🔍 Computing shortest path in Kolkata...")
        start_time = time.time()
        
        # Find nearest nodes
        start_node = self.find_nearest_node(start_coords[0], start_coords[1])
        end_node = self.find_nearest_node(end_coords[0], end_coords[1])
        
        print(f"   Start node: {start_node}")
        print(f"   End node: {end_node}")
        
        try:
            # Compute shortest path using Dijkstra's algorithm
            path_nodes = nx.shortest_path(
                self.graph, 
                start_node, 
                end_node, 
                weight=weight,
                method='dijkstra'
            )
            
            # Get path length
            path_length = nx.shortest_path_length(
                self.graph, 
                start_node, 
                end_node, 
                weight=weight,
                method='dijkstra'
            )
            
            # Convert path nodes to coordinates
            path_coords = []
            for node in path_nodes:
                node_data = self.graph.nodes[node]
                path_coords.append((node_data['y'], node_data['x']))  # (lat, lon)
            
            compute_time = time.time() - start_time
            
            result = {
                'path_nodes': path_nodes,
                'path_coordinates': path_coords,
                'distance_meters': path_length if weight == 'length' else None,
                'travel_time_seconds': path_length if weight == 'travel_time' else None,
                'start_coords': start_coords,
                'end_coords': end_coords,
                'start_node': start_node,
                'end_node': end_node,
                'compute_time': compute_time
            }
            
            # Calculate actual distance if using travel_time
            if weight == 'travel_time':
                distance = sum(
                    self.graph[path_nodes[i]][path_nodes[i+1]][0].get('length', 0)
                    for i in range(len(path_nodes)-1)
                )
                result['distance_meters'] = distance
            
            print(f"✅ Shortest path computed successfully!")
            print(f"   📏 Distance: {result['distance_meters']/1000:.2f} km")
            print(f"   🚗 Path segments: {len(path_nodes)} nodes")
            print(f"   ⚡ Computation time: {compute_time:.3f} seconds")
            
            if result['travel_time_seconds']:
                print(f"   🕐 Estimated travel time: {result['travel_time_seconds']/60:.1f} minutes")
            
            return result
            
        except nx.NetworkXNoPath:
            raise ValueError("No path found between the specified points in Kolkata")
        except Exception as e:
            print(f"❌ Error computing path: {e}")
            raise
    
    def visualize_kolkata_path(self, path_result: Dict[str, Any], 
                              save_html: str = "kolkata_path.html", 
                              show_plot: bool = True) -> None:
        """
        Visualize the Kolkata street network and shortest path
        
        Args:
            path_result: Result from compute_shortest_path()
            save_html: Filename to save interactive map
            show_plot: Whether to show matplotlib plot
        """
        print(f"\n🗺️  Creating visualizations...")
        
        if show_plot:
            self._plot_matplotlib_kolkata(path_result)
        
        if save_html:
            self._create_interactive_kolkata_map(path_result, save_html)
    
    def _plot_matplotlib_kolkata(self, path_result: Dict[str, Any]) -> None:
        """Create matplotlib visualization for Kolkata"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        
        # Plot the entire Kolkata street network
        ox.plot_graph(
            self.graph, 
            ax=ax, 
            node_size=0, 
            edge_color='lightgray', 
            edge_linewidth=0.5,
            show=False, 
            close=False
        )
        
        # Highlight the shortest path
        ox.plot_graph_route(
            self.graph, 
            path_result['path_nodes'],
            ax=ax,
            route_color='red',
            route_linewidth=4,
            node_size=0,
            show=False,
            close=False
        )
        
        # Add start and end markers
        start_coords = path_result['start_coords']
        end_coords = path_result['end_coords']
        
        ax.scatter(start_coords[1], start_coords[0], c='green', s=150, marker='o', 
                  zorder=5, label='Start', edgecolors='black', linewidth=2)
        ax.scatter(end_coords[1], end_coords[0], c='red', s=150, marker='s', 
                  zorder=5, label='End', edgecolors='black', linewidth=2)
        
        # Add some landmark points for reference
        for name, coords in list(self.landmarks.items())[:5]:  # Show first 5 landmarks
            ax.scatter(coords[1], coords[0], c='blue', s=50, marker='^', 
                      alpha=0.7, zorder=4)
            ax.annotate(name, (coords[1], coords[0]), xytext=(5, 5), 
                       textcoords='offset points', fontsize=8, alpha=0.8)
        
        ax.legend(fontsize=12)
        ax.set_title(f"Shortest Path in Kolkata\n"
                    f"Distance: {path_result['distance_meters']/1000:.2f} km | "
                    f"Computation Time: {path_result['compute_time']:.3f}s", 
                    fontsize=16, pad=20)
        
        plt.tight_layout()
        plt.show()
    
    def _create_interactive_kolkata_map(self, path_result: Dict[str, Any], filename: str) -> None:
        """Create interactive Folium map for Kolkata"""
        # Calculate map center
        path_coords = path_result['path_coordinates']
        center_lat = np.mean([coord[0] for coord in path_coords])
        center_lon = np.mean([coord[1] for coord in path_coords])
        
        # Create map centered on Kolkata
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=12,
            tiles='OpenStreetMap'
        )
        
        # Add path as polyline
        folium.PolyLine(
            path_coords,
            color='red',
            weight=6,
            opacity=0.8,
            popup=f"Shortest Path: {path_result['distance_meters']/1000:.2f} km"
        ).add_to(m)
        
        # Add start marker
        folium.Marker(
            path_result['start_coords'],
            popup='🚩 Start Point',
            icon=folium.Icon(color='green', icon='play', prefix='fa')
        ).add_to(m)
        
        # Add end marker
        folium.Marker(
            path_result['end_coords'],
            popup='🏁 End Point',
            icon=folium.Icon(color='red', icon='stop', prefix='fa')
        ).add_to(m)
        
        # Add some famous Kolkata landmarks
        for name, coords in self.landmarks.items():
            folium.CircleMarker(
                coords,
                radius=5,
                popup=f"🏛️ {name}",
                color='blue',
                fill=True,
                fillColor='lightblue',
                fillOpacity=0.7
            ).add_to(m)
        
        # Add info box
        info_html = f"""
        <div style="position: fixed; 
                    top: 10px; right: 10px; width: 300px; height: 120px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        <h4>🏙️ Kolkata Pathfinder</h4>
        <p><b>Distance:</b> {path_result['distance_meters']/1000:.2f} km</p>
        <p><b>Path Segments:</b> {len(path_result['path_nodes'])}</p>
        <p><b>Computation Time:</b> {path_result['compute_time']:.3f}s</p>
        </div>
        """
        m.get_root().html.add_child(folium.Element(info_html))
        
        # Save map
        m.save(filename)
        print(f"✅ Interactive Kolkata map saved as {filename}")
    
    def export_kolkata_path_csv(self, path_result: Dict[str, Any], filename: str = "kolkata_path.csv") -> None:
        """
        Export Kolkata path coordinates to CSV file
        
        Args:
            path_result: Result from compute_shortest_path()
            filename: Output CSV filename
        """
        df = pd.DataFrame(path_result['path_coordinates'], columns=['latitude', 'longitude'])
        df['step'] = range(len(df))
        df['city'] = 'Kolkata'
        df['distance_km'] = path_result['distance_meters'] / 1000
        
        df.to_csv(filename, index=False)
        print(f"✅ Kolkata path exported to {filename} ({len(df)} coordinate points)")
    
    def get_kolkata_stats(self) -> Dict[str, Any]:
        """Get statistics about the loaded Kolkata network"""
        if self.graph is None:
            return {}
        
        # Calculate total road length
        total_length = sum(
            data.get('length', 0) for u, v, data in self.graph.edges(data=True)
        ) / 1000  # Convert to km
        
        return {
            'city_name': self.city_name,
            'nodes': len(self.graph.nodes),
            'edges': len(self.graph.edges),
            'total_length_km': total_length,
            'is_strongly_connected': nx.is_strongly_connected(self.graph),
            'average_degree': sum(dict(self.graph.degree()).values()) / len(self.graph.nodes),
            'landmarks_available': len(self.landmarks)
        }


def kolkata_demo():
    """Main Kolkata pathfinder demo"""
    print("🏙️  Kolkata City Pathfinder Demo")
    print("Using Dijkstra's Algorithm with OpenStreetMap Data")
    print("=" * 60)
    
    # Initialize Kolkata pathfinder
    pathfinder = KolkataPathfinder()
    
    try:
        # Load Kolkata street data
        pathfinder.load_kolkata_data()
        
        # Show city statistics
        stats = pathfinder.get_kolkata_stats()
        print(f"\n📊 Kolkata Street Network Statistics:")
        print(f"   🏙️  City: {stats['city_name']}")
        print(f"   📍 Intersections: {stats['nodes']:,}")
        print(f"   🛣️  Road segments: {stats['edges']:,}")
        print(f"   📏 Total road length: {stats['total_length_km']:.1f} km")
        print(f"   🔗 Strongly connected: {stats['is_strongly_connected']}")
        print(f"   🏛️  Landmarks available: {stats['landmarks_available']}")
        
        # Show available landmarks
        pathfinder.show_landmarks()
        
        # Get start and end points from user
        print("📍 Enter start and end locations in Kolkata:")
        print("   • Use landmark names (e.g., 'Victoria Memorial', 'Howrah Bridge')")
        print("   • Use addresses (e.g., 'Park Street', 'Salt Lake')")
        print("   • Use coordinates (e.g., '22.5448,88.3426')")
        print()
        
        start_input = input("🚩 Start location: ").strip()
        end_input = input("🏁 End location: ").strip()
        
        # Parse locations
        def parse_kolkata_location(location_str):
            # Check if it's coordinates
            if ',' in location_str and all(
                part.replace('.', '').replace('-', '').strip().isdigit() 
                for part in location_str.split(',')
            ):
                parts = location_str.split(',')
                return (float(parts[0].strip()), float(parts[1].strip()))
            else:
                # Use geocoding for addresses/landmarks
                return pathfinder.geocode_kolkata_address(location_str)
        
        start_coords = parse_kolkata_location(start_input)
        end_coords = parse_kolkata_location(end_input)
        
        print(f"\n📍 Route Details:")
        print(f"   Start: {start_coords}")
        print(f"   End: {end_coords}")
        
        # Compute shortest path using Dijkstra's algorithm
        path_result = pathfinder.compute_shortest_path(start_coords, end_coords)
        
        # Create visualizations
        print(f"\n🎨 Creating visualizations...")
        pathfinder.visualize_kolkata_path(
            path_result, 
            save_html="kolkata_shortest_path.html", 
            show_plot=False  # Set to True if you want matplotlib plot
        )
        
        # Export path data
        pathfinder.export_kolkata_path_csv(path_result, "kolkata_shortest_path.csv")
        
        print(f"\n🎉 Kolkata pathfinding demo completed successfully!")
        print(f"📁 Files created:")
        print(f"   • kolkata_shortest_path.html (interactive map)")
        print(f"   • kolkata_shortest_path.csv (path coordinates)")
        
        # Summary
        print(f"\n📋 Route Summary:")
        print(f"   🏙️  City: Kolkata, West Bengal, India")
        print(f"   📏 Distance: {path_result['distance_meters']/1000:.2f} km")
        print(f"   🚗 Path segments: {len(path_result['path_nodes'])}")
        print(f"   ⚡ Computation time: {path_result['compute_time']:.3f} seconds")
        print(f"   🧮 Algorithm: Dijkstra's shortest path")
        
        return path_result
        
    except Exception as e:
        print(f"❌ Error in Kolkata demo: {e}")
        return None


def quick_kolkata_demo():
    """Quick demo with predefined Kolkata landmarks"""
    print("🚀 Quick Kolkata Demo: Victoria Memorial to Howrah Bridge")
    print("=" * 60)
    
    pathfinder = KolkataPathfinder()
    pathfinder.load_kolkata_data()
    
    # Predefined route: Victoria Memorial to Howrah Bridge
    start_coords = pathfinder.landmarks["Victoria Memorial"]
    end_coords = pathfinder.landmarks["Howrah Bridge"]
    
    print(f"📍 Route: Victoria Memorial → Howrah Bridge")
    
    # Compute path
    path_result = pathfinder.compute_shortest_path(start_coords, end_coords)
    
    # Create outputs
    pathfinder.visualize_kolkata_path(
        path_result, 
        save_html="kolkata_quick_demo.html", 
        show_plot=False
    )
    pathfinder.export_kolkata_path_csv(path_result, "kolkata_quick_demo.csv")
    
    print(f"\n✅ Quick demo completed!")
    print(f"📁 Created: kolkata_quick_demo.html, kolkata_quick_demo.csv")
    
    return path_result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_kolkata_demo()
    else:
        kolkata_demo()
