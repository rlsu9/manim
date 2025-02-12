from manim import *

STOKE_WIDTH=0.7
COLOR_DEPTH=0.7
FAST_TIME=1
class GridProjectionScene(ThreeDScene):
    def construct(self):
        # Configure the scene
        self.set_camera_orientation(
            phi=65 * DEGREES, 
            theta=270 * DEGREES,
            zoom=0.2  # Increase this value to move camera further away
        )
        
        # Create the base grids
        top_grid = self.create_numbered_grid(rows=12, cols=12, z_pos=5)
        bottom_grid = self.create_numbered_grid(rows=12, cols=12, z_pos=0)
        
        # Create connecting lines for the projection
        projections, top_tl, bottom_tl = self.create_projections(top_grid, bottom_grid)
        
        # Create colored regions
        blue_region = self.create_colored_region(top_grid, 2, top_tl, BLUE_E, COLOR_DEPTH)
        
        
        red_region = self.create_colored_region(bottom_grid, 6, bottom_tl, RED_E, COLOR_DEPTH)
        
        # Animation sequence
        top_bottom_grid_animations = []
        
        for line in top_grid:
            top_bottom_grid_animations.append(Create(line))
        for line in bottom_grid:
            top_bottom_grid_animations.append(Create(line))
        
        self.play(AnimationGroup(*top_bottom_grid_animations, lag_ratio=0), run_time=FAST_TIME)
        
        
        projection_animations = []
        for line in projections:
            projection_animations.append(Create(line))
            
        self.play(AnimationGroup(*projection_animations, lag_ratio=0))
        self.play(
            FadeIn(blue_region),
            FadeIn(red_region),
        )
        
        color_and_Projecton_group = VGroup(projections, blue_region, red_region)
        
        initial_position = color_and_Projecton_group.get_center()
        
        # Number of horizontal and vertical movements
        horizontal_steps = 3
        vertical_steps = 4  # You can adjust this number for more/fewer vertical movements
        
        # Define step sizes
        horizontal_step = RIGHT
        vertical_step = DOWN
        
        stride = 2
        
        regions_group = VGroup(blue_region, red_region)
        
        # Create zigzag pattern
        for v in range(vertical_steps):
            # Move right
            for h in range(horizontal_steps):
                # Update projection lines positions before animation
                new_starts = [blue_region.get_corner(pos) for pos in [UL, UR, DL, DR]]
                new_ends = [red_region.get_corner(pos) for pos in [UL, UR, DL, DR]]
                
                # Create the animation for regions
                region_anim = regions_group.animate.shift(horizontal_step * stride)
                
                # Create animations for projection lines
                projection_anims = []
                for i, line in enumerate(projections):
                    # Calculate target positions after shift
                    target_start = new_starts[i] + horizontal_step * stride
                    target_end = new_ends[i] + horizontal_step * stride
                    
                    # Create line animation
                    line_anim = line.animate.put_start_and_end_on(target_start, target_end)
                    projection_anims.append(line_anim)
                
                # Play all animations together
                self.play(
                    region_anim,
                    *projection_anims,
                    run_time=FAST_TIME
                )
            
            if v == vertical_steps - 1:
                break
            
            # Calculate new positions for vertical movement
            vertical_offset = vertical_step * (v + 1) * stride
            target_position = initial_position + vertical_offset
            
            # Update projection lines for vertical movement
            new_starts = [blue_region.get_corner(pos) for pos in [UL, UR, DL, DR]]
            new_ends = [red_region.get_corner(pos) for pos in [UL, UR, DL, DR]]
            
            projection_reset_anims = []
            for i, line in enumerate(projections):
                if h == horizontal_steps - 1:
                    target_start = new_starts[i] + vertical_step * stride - horizontal_steps *horizontal_step * stride
                    target_end = new_ends[i] + vertical_step * stride - horizontal_steps * horizontal_step * stride
                else:
                    target_start = new_starts[i] + vertical_offset
                    target_end = new_ends[i] + vertical_offset
                line_anim = line.animate.put_start_and_end_on(target_start, target_end)
                projection_reset_anims.append(line_anim)
            
            # Play reset animation with all elements
            self.play(
                regions_group.animate.move_to(target_position),
                *projection_reset_anims,
                run_time=FAST_TIME
            )
            
        
        
        # Rotate the camera for better view
        # self.begin_ambient_camera_rotation(rate=0.2, about="phi")
        # self.wait(2)
        # self.stop_ambient_camera_rotation()

    def create_numbered_grid(self, rows, cols, z_pos):
        grid = VGroup()
        
        # Create horizontal and vertical lines
        for i in range(rows + 1):
            grid.add(Line(
                start=np.array([-cols/2, -rows/2 + i, z_pos]),
                end=np.array([cols/2, -rows/2 + i, z_pos]),
                stroke_width=STOKE_WIDTH
            ))
        for j in range(cols + 1):
            grid.add(Line(
                start=np.array([-cols/2 + j, -rows/2, z_pos]),
                end=np.array([-cols/2 + j, rows/2, z_pos]),
                stroke_width=STOKE_WIDTH
            ))
                
        return grid

    def create_projections(self, top_grid, bottom_grid):
        projections = VGroup()
        
        # Create connecting lines at the corners
        
        top_tl = (-4, 4)
        top_tr = top_tl + np.array([2, 0])
        top_bl = top_tl + np.array([0, -2])
        top_br = top_tl + np.array([2, -2])
        
        bottom_tl = top_tl + np.array([-2, 2])
        bottom_tr = top_tr + np.array([2, 2])
        bottom_bl = top_bl + np.array([-2, -2])
        bottom_br = top_br + np.array([2, -2])
                
        corners = [
            (top_tl[0], top_tl[1], bottom_tl[0], bottom_tl[1]),
            (top_tr[0], top_tr[1], bottom_tr[0], bottom_tr[1]),
            (top_bl[0], top_bl[1], bottom_bl[0], bottom_bl[1]),
            (top_br[0], top_br[1], bottom_br[0], bottom_br[1]),
        ]
        
        for x, y, z, k in corners:
            projections.add(Line(
                start=np.array([x, y, 5]),
                end=np.array([z, k, 0]),
                stroke_opacity=0.5,
                stroke_width=STOKE_WIDTH
            ))
            
        return projections, top_tl, bottom_tl

    def create_colored_region(self, grid, side_length, tl_pos, color, opacity):
        
        i, j = tl_pos
        
        # Get the z-position from the grid's first element
        grid_z_pos = grid[0].get_start()[2]
        
        # Create a colored rectangle for each cell
        rect = Rectangle(
            width=side_length,
            height=side_length,
            fill_color=color,
            fill_opacity=opacity,
            stroke_width=0
        )
        rect.move_to(np.array([
            i + (side_length / 2),
            j - (side_length / 2),
            grid_z_pos  # Use the grid's z-position
        ]))
            
        return rect