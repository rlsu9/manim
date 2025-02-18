from manim import *
import numpy as np

COLOR_DEPTH = 0.8
STOKE_WIDTH = 0.2
BOLD_STOKE_WIDTH = 0.5
SIDE_LENGTH = 100
SLIDING_WINDOW_SIZE = 5
HALF_SIDE_LENGTH = SIDE_LENGTH / 2
CANVAS_SIZE = 10

def get_window_center(pos, canvas_size=CANVAS_SIZE, kernel_size=SLIDING_WINDOW_SIZE):
    """Calculate the window center for a given position with edge clamping"""
    kernel_half = kernel_size // 2
    row = pos // canvas_size
    col = pos % canvas_size
    
    center_row = min(max(row, kernel_half), canvas_size - kernel_half - 1)
    center_col = min(max(col, kernel_half), canvas_size - kernel_half - 1)
    
    return center_row, center_col

def get_window_indices(center_row, center_col, canvas_size=CANVAS_SIZE, kernel_size=SLIDING_WINDOW_SIZE):
    """Get indices within the window given the center position"""
    kernel_half = kernel_size // 2
    rows = np.arange(center_row - kernel_half, center_row + kernel_half + 1)
    cols = np.arange(center_col - kernel_half, center_col + kernel_half + 1)
    
    row_indices, col_indices = np.meshgrid(rows, cols)
    positions = row_indices.flatten() * canvas_size + col_indices.flatten()
    
    return positions

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
            # Calculate window center and indices for this query
            center_row, center_col = get_window_center(query_pos)
            window_indices = get_window_indices(center_row, center_col)
            
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