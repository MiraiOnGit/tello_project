import pygame
from djitellopy import Tello
import time

# Initialize Pygame
pygame.init()

# Set up display
WINDOW_WIDTH, WINDOW_HEIGHT = 960, 720
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Initialize Tello drone
tello = Tello()
tello.connect()
tello.streamon()
print(f"Battery: {tello.get_battery()}%")

# Set default speed
tello.set_speed(10)

# Initialize control variables
running = True
recording = False
takeoff = False
lr, fb, ud, yaw = 0, 0, 0, 0

def update_drone():
    tello.send_rc_control(lr, fb, ud, yaw)

def display_altitude_and_battery():
    altitude = tello.get_height()
    battery = tello.get_battery()
    font = pygame.font.SysFont("Arial", 24)
    altitude_text = font.render(f"Altitude: {altitude} cm", True, (255, 255, 255))
    battery_text = font.render(f"Battery: {battery}%", True, (255, 255, 255))
    win.blit(altitude_text, (10, 10))
    win.blit(battery_text, (10, 40))

# Main control loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            tello.land()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not takeoff:
                tello.takeoff()
                takeoff = True
            elif event.key == pygame.K_RETURN and takeoff:
                tello.land()
                takeoff = False
            elif event.key == pygame.K_p:
                recording = not recording
            elif event.key == pygame.K_q:  # E-stop functionality
                tello.land()
                running = False

    keys = pygame.key.get_pressed()
    lr = 0
    fb = 0
    ud = 0
    yaw = 0

    # Movement keys
    if keys[pygame.K_w]:
        fb = 20
    elif keys[pygame.K_s]:
        fb = -20

    if keys[pygame.K_a]:
        lr = -20
    elif keys[pygame.K_d]:
        lr = 20

    if keys[pygame.K_UP]:
        ud = 20
    elif keys[pygame.K_DOWN]:
        ud = -20

    # Turning keys
    if keys[pygame.K_LEFT]:
        yaw = -30
    elif keys[pygame.K_RIGHT]:
        yaw = 30

    # Mouse control for yaw
    mouse_rel = pygame.mouse.get_rel()
    if takeoff:  # Only adjust yaw when drone is in the air
        yaw += int(mouse_rel[0] / 2)  # Increase sensitivity as needed

    update_drone()

    # Display the video feed
    frame = tello.get_frame_read().frame
    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    win.blit(frame, (0, 0))

    # Draw crosshair
    pygame.draw.line(win, (255, 0, 0), (WINDOW_WIDTH // 2 - 10, WINDOW_HEIGHT // 2), (WINDOW_WIDTH // 2 + 10, WINDOW_HEIGHT // 2), 2)
    pygame.draw.line(win, (255, 0, 0), (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 10), (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10), 2)

    # Display altitude and battery
    display_altitude_and_battery()

    pygame.display.update()

# Clean up
pygame.quit()
