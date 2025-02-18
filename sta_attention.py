from manim import *
import numpy as np

COLOR_DEPTH = 0.8
STOKE_WIDTH = 0.2
BOLD_STOKE_WIDTH = 0.5
SIDE_LENGTH = 100
SLIDING_WINDOW_SIZE = 3
HALF_SIDE_LENGTH = SIDE_LENGTH / 2
CANVAS_SIZE = 10
TILE_SIDE = 2

def get_tile_center(pos, canvas_size=6, kernel_size=3):
    """Calculate the window center for a given position with edge clamping"""
    kernel_half = kernel_size // 2
    row = pos // canvas_size
    col = pos % canvas_size
    
    # Clamp the center coordinates
    center_row = min(max(row, kernel_half), canvas_size - kernel_half - 1)
    center_col = min(max(col, kernel_half), canvas_size - kernel_half - 1)
    
    return center_row, center_col

def get_tile_window_indices(query_tile, canvas_size=12, window_size=3):
    """Get indices of tiles within the window for a given query tile"""
    tiles_per_row = canvas_size // 2
    
    # Get the center tile for attention
    center_row, center_col = get_tile_center(query_tile, tiles_per_row)
    
    half_window = window_size // 2
    
    # Calculate tile range with clamping
    start_row = center_row - half_window
    end_row = center_row + half_window + 1
    start_col = center_col - half_window
    end_col = center_col + half_window + 1
    
    tile_indices = []
    for row in range(start_row, end_row):
        for col in range(start_col, end_col):
            tile_idx = row * tiles_per_row + col
            # Convert tile index to all positions within the tile
            for i in range(4):  # 4 positions per tile
                pos = tile_idx * 4 + i
                tile_indices.append(pos)
    assert len(tile_indices) == 36, f"Expected 9 positions, got {len(tile_indices)}"
    
    return tile_indices

class PlainAttentionScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi=0 * DEGREES, 
            theta=270 * DEGREES,
            zoom=0.025
        )
        
        grid = self.create_numbered_grid(rows=SIDE_LENGTH, cols=SIDE_LENGTH, z_pos=0)
        
        grid_animations = []
        for line in grid:
            grid_animations.append(Create(line))
            
        self.play(AnimationGroup(*grid_animations, lag_ratio=0), run_time=1)
        
        # Process each query position
        for query_pos in range(CANVAS_SIZE * CANVAS_SIZE):
            query_tile = query_pos // (TILE_SIDE * TILE_SIDE)
            
            window_indices = get_tile_window_indices(query_tile, CANVAS_SIZE, SLIDING_WINDOW_SIZE)
            
            # Convert window indices to scene coordinates
            scene_positions = []
            for idx in window_indices:
                row = query_pos
                col = idx
                # Convert to scene coordinates
                x = col - HALF_SIDE_LENGTH
                y = HALF_SIDE_LENGTH - row  # Adjust for scene coordinate system
                scene_positions.append((x, y))
            
            # Create colored regions for this query's attention pattern
            colored_regions = VGroup()
            for pos in scene_positions:
                rect = Rectangle(
                    width=1,
                    height=1,
                    fill_color=YELLOW_E,
                    fill_opacity=COLOR_DEPTH,
                    stroke_width=0
                )
                rect.move_to(np.array([pos[0], pos[1], 0]))
                colored_regions.add(rect)
            
            # Animate the attention pattern
            self.play(FadeIn(colored_regions), run_time=0.5)
    
    def create_numbered_grid(self, rows, cols, z_pos):
        grid = VGroup()
        
        # Create horizontal and vertical lines
        for i in range(rows + 1):      
            grid.add(Line(
                start=np.array([-cols/2, -rows/2 + i, z_pos]),
                end=np.array([cols/2, -rows/2 + i, z_pos]),
                stroke_width=BOLD_STOKE_WIDTH
            ))
        for j in range(cols + 1):
            grid.add(Line(
                start=np.array([-cols/2 + j, -rows/2, z_pos]),
                end=np.array([-cols/2 + j, rows/2, z_pos]),
                stroke_width=BOLD_STOKE_WIDTH
            ))
            
        return grid