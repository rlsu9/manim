from manim import *

COLOR_DEPTH=0.8
STOKE_WIDTH=0.5
BOLD_STOKE_WIDTH=0.5

class PlainAttentionScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
                phi=0 * DEGREES, 
                theta=270 * DEGREES,
                zoom=0.07  # Increase this value to move camera further away
            )
        
        grid = self.create_numbered_grid(rows=36, cols=36, z_pos=0)
        
        grid_animations = []
        for line in grid:
            grid_animations.append(Create(line))
            
        self.play(AnimationGroup(*grid_animations, lag_ratio=0), run_time=1)
        
        hori_start = 0
        vert_start = 18
        
        hardcode_hori = [0,0,6,12,18,18]
        
        for i in range(36):
            if i % 6 == 0:
                hori_start = hardcode_hori[int(i/6)] -15
            
            colored_region = self.create_colored_hori_region(grid, (hori_start, vert_start), RED, COLOR_DEPTH)
            
            self.play(FadeIn(colored_region))
            vert_start -= 1
            
            if not (i % 6 == 0 or i % 6 == 4):
                hori_start += 1
        
    def create_colored_hori_region(self, grid, tl_pos, color, opacity):
        i, j = tl_pos
        
        WIDTH = 3
        HEIGHT = 1
        INTERVAL = 3  # Horizontal interval between the two rectangles
        
        # Get the z-position from the grid's first element
        grid_z_pos = grid[0].get_start()[2]
        
        # Create the first rectangle
        rect1 = Rectangle(
            width=WIDTH,
            height=HEIGHT,
            fill_color=color,
            fill_opacity=opacity,
            stroke_width=0
        )
        rect1.move_to(np.array([
            i - (WIDTH / 2),
            j - (HEIGHT / 2),
            grid_z_pos  # Use the grid's z-position
        ]))
        
        # Create the second rectangle, offset horizontally by WIDTH + INTERVAL
        rect2 = Rectangle(
            width=WIDTH,
            height=HEIGHT,
            fill_color=color,
            fill_opacity=opacity,
            stroke_width=0
        )
        rect2.move_to(np.array([
            i - (WIDTH / 2) + WIDTH + INTERVAL,  # Offset by WIDTH + INTERVAL
            j - (HEIGHT / 2),
            grid_z_pos  # Use the grid's z-position
        ]))
        
        rect3 = Rectangle(
            width=WIDTH,
            height=HEIGHT,
            fill_color=color,
            fill_opacity=opacity,
            stroke_width=0
        )
        rect3.move_to(np.array([
            i - (WIDTH / 2) + 2 * (WIDTH + INTERVAL),  # Offset by WIDTH + INTERVAL
            j - (HEIGHT / 2),
            grid_z_pos  # Use the grid's z-position
        ]))
        
        # Group the two rectangles
        return VGroup(rect1, rect2, rect3)
    
    def create_numbered_grid(self, rows, cols, z_pos):
        grid = VGroup()
        
        # Create horizontal and vertical lines
        for i in range(rows + 1):
            if i % 2 == 0:
                grid.add(Line(
                start=np.array([-cols/2, -rows/2 + i, z_pos]),
                end=np.array([cols/2, -rows/2 + i, z_pos]),
                stroke_width=BOLD_STOKE_WIDTH
            ))
            else:       
                grid.add(Line(
                    start=np.array([-cols/2, -rows/2 + i, z_pos]),
                    end=np.array([cols/2, -rows/2 + i, z_pos]),
                    stroke_width=STOKE_WIDTH
                ))
        for j in range(cols + 1):
            if j % 2 == 0:
                grid.add(Line(
                start=np.array([-cols/2 + j, -rows/2, z_pos]),
                end=np.array([-cols/2 + j, rows/2, z_pos]),
                stroke_width=BOLD_STOKE_WIDTH
            ))
            else:
                grid.add(Line(
                    start=np.array([-cols/2 + j, -rows/2, z_pos]),
                    end=np.array([-cols/2 + j, rows/2, z_pos]),
                    stroke_width=STOKE_WIDTH
                ))
                
        return grid
        
        