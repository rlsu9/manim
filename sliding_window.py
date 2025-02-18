from manim import *

STOKE_WIDTH=0.3
COLOR_DEPTH=0.8
SMALL_SIDE_LENGTH = 1
LARGE_SIDE_LENGTH = 5
CANVAS_SIZE = 10
FAST_TIME=1
ROTATION_TIME=1
NUMBER_DISPLAY_TIME=1
class GridProjectionScene(ThreeDScene):
    def construct(self):
        # Configure the scene
        self.set_camera_orientation(
            phi=0 * DEGREES, 
            theta=270 * DEGREES,
            zoom=0.15  # Increase this value to move camera further away
        )
        
        # Create the base grids
        top_grid = self.create_numbered_grid(rows=CANVAS_SIZE, cols=CANVAS_SIZE, z_pos=5)
        bottom_grid = self.create_numbered_grid(rows=CANVAS_SIZE, cols=CANVAS_SIZE, z_pos=0)
        
        # Create connecting lines for the projection
        projections, top_tl, bottom_tl = self.create_projections(top_grid, bottom_grid)
        
        # Create colored regions
        red_region = self.create_coloyellow_region(top_grid, SMALL_SIDE_LENGTH, top_tl, RED_E, COLOR_DEPTH)
        
        
        yellow_region = self.create_coloyellow_region(bottom_grid, LARGE_SIDE_LENGTH, bottom_tl, YELLOW_E, COLOR_DEPTH)
        
        # Animation sequence
        top_numbers = self.create_grid_numbers(CANVAS_SIZE, z_pos=5)
        top_grid_animations = []
        
        for line in top_grid:
            top_grid_animations.append(Create(line))
        for number in top_numbers:
            top_grid_animations.append(Create(number))
        
        self.play(AnimationGroup(*top_grid_animations, lag_ratio=0), run_time=FAST_TIME)
        
        
        self.wait(NUMBER_DISPLAY_TIME)
        
        highlight_grid = self.create_coloyellow_region(top_grid, 2, top_tl, RED_E, 0.4)
        
        self.play(FadeIn(highlight_grid))
        
        self.wait(NUMBER_DISPLAY_TIME)
        
        self.play(FadeOut(highlight_grid))
        
        
        # rotate the camera phi for 62 degrees
        self.move_camera(
            phi=62 * DEGREES,  # Target angle
            run_time=ROTATION_TIME,
            rate_func=smooth,  # Makes the rotation smooth
            zoom=0.2
        )
        
        bottom_numbers = self.create_grid_numbers(CANVAS_SIZE, z_pos=0)
        bottom_grid_animations = []
        for line in bottom_grid:
            bottom_grid_animations.append(Create(line))
        for number in bottom_numbers:
            bottom_grid_animations.append(Create(number))
        for num in top_numbers:
            bottom_grid_animations.append(FadeOut(num))
        
        self.play(AnimationGroup(*bottom_grid_animations, lag_ratio=0), run_time=FAST_TIME)
        
        
        
        projection_animations = []
        for line in projections:
            projection_animations.append(Create(line))
            
        self.play(AnimationGroup(*projection_animations, lag_ratio=0))
        self.play(
            FadeIn(red_region),
            FadeIn(yellow_region),
        )
        
        color_and_Projecton_group = VGroup(projections, red_region, yellow_region)
        
        initial_position = color_and_Projecton_group.get_center()
        
        # Number of horizontal and vertical movements
        horizontal_steps = 9
        vertical_steps = 10  # You can adjust this number for more/fewer vertical movements
        
        # Define step sizes
        horizontal_step = RIGHT
        vertical_step = DOWN
        
        stride = 1
        
        # Create zigzag pattern
        for v in range(vertical_steps):
            for h in range(horizontal_steps):
                # Update projection lines positions before animation
                new_starts = [red_region.get_corner(pos) for pos in [UL, UR, DL, DR]]
                new_ends = [yellow_region.get_corner(pos) for pos in [UL, UR, DL, DR]]
                
                # Create the animation for regions
                region_anim = []
                region_anim.append(red_region.animate.shift(horizontal_step * stride))
                
                if h > 1 and h < 7:
                    region_anim.append(yellow_region.animate.shift(horizontal_step * stride))
                    
                
                
                # Create animations for projection lines
                projection_anims = []
                for i, line in enumerate(projections):
                    # Calculate target positions after shift
                    if h > 1 and h < 7:
                        target_start = new_starts[i] + horizontal_step * stride
                        target_end = new_ends[i] + horizontal_step * stride
                    else:
                    
                        target_start = new_starts[i] + horizontal_step * stride
                        target_end = new_ends[i]
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
            vert_region_anim = []
            vert_region_anim.append(red_region.animate.shift(vertical_step * stride - horizontal_steps * horizontal_step * stride))
            
            
            
            if v > 1 and v < 7:
                vert_region_anim.append(yellow_region.animate.shift(vertical_step * stride - 5 * horizontal_step * stride))
            else:
                vert_region_anim.append(yellow_region.animate.shift(- 5 * horizontal_step * stride))
            
            vertical_offset = vertical_step * (v + 1) * stride
            target_position = initial_position + vertical_offset
            
            # Update projection lines for vertical movement
            new_starts = [red_region.get_corner(pos) for pos in [UL, UR, DL, DR]]
            new_ends = [yellow_region.get_corner(pos) for pos in [UL, UR, DL, DR]]
            
            projection_reset_anims = []
            for i, line in enumerate(projections):
                if h == horizontal_steps - 1:
                    target_start = new_starts[i] + vertical_step * stride - horizontal_steps *horizontal_step * stride
                    if v > 1 and v < 7: 
                        target_end = new_ends[i] - 5 * horizontal_step * stride + vertical_step * stride
                    else:
                        target_end = new_ends[i] - 5 * horizontal_step * stride
                else:
                    target_start = new_starts[i] + vertical_offset
                    target_end = new_ends[i]
                line_anim = line.animate.put_start_and_end_on(target_start, target_end)
                projection_reset_anims.append(line_anim)
            
            # Play reset animation with all elements
            self.play(
                vert_region_anim,
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
            if i % 2 == 0:
                grid.add(Line(
                start=np.array([-cols/2, -rows/2 + i, z_pos]),
                end=np.array([cols/2, -rows/2 + i, z_pos]),
                stroke_width=STOKE_WIDTH
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
                stroke_width=STOKE_WIDTH
            ))
            else:
                grid.add(Line(
                    start=np.array([-cols/2 + j, -rows/2, z_pos]),
                    end=np.array([-cols/2 + j, rows/2, z_pos]),
                    stroke_width=STOKE_WIDTH
                ))
                
        return grid

    def create_grid_numbers(self, size, z_pos):
        numbers = VGroup()
        half_size = size // 2
        
        for i in range(-half_size, half_size):
            for j in range(-half_size, half_size):
                number = Text(
                    str((i + half_size) * size + (j + half_size) + 1),
                    font_size=20,
                    color=WHITE
                )
                number.move_to(np.array([j + 0.5, -i - 0.5, z_pos]))
                numbers.add(number)
        
        return numbers
    
    def create_projections(self, top_grid, bottom_grid):
        projections = VGroup()
        
        # Create connecting lines at the corners
        half_side = int(CANVAS_SIZE / 2)
        
        top_tl = (-half_side, half_side)
        top_tr = top_tl + np.array([SMALL_SIDE_LENGTH, 0])
        top_bl = top_tl + np.array([0, -SMALL_SIDE_LENGTH])
        top_br = top_tl + np.array([SMALL_SIDE_LENGTH, -SMALL_SIDE_LENGTH])
        
        bottom_tl = (-half_side, half_side)
        bottom_tr = bottom_tl + np.array([LARGE_SIDE_LENGTH, 0])
        bottom_bl = bottom_tl + np.array([-0, -LARGE_SIDE_LENGTH])
        bottom_br = bottom_tl + np.array([LARGE_SIDE_LENGTH, -LARGE_SIDE_LENGTH])
                
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
                stroke_width=1.0
            ))
            
        return projections, top_tl, bottom_tl

    def create_coloyellow_region(self, grid, side_length, tl_pos, color, opacity):
        
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