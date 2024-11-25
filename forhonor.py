import keyboard
import time
import ctypes
import PIL.ImageGrab
import winsound
import numpy as np
import pygetwindow as gw
import os
import win32gui
import win32con
import win32api
import mss
import asyncio
from ctypes import wintypes

# Definições de teclas
AUTOBLOCK_KEY = "F1"
AUTODODGE_KEY = "F2"
AUTOPARRY_KEY = 0x43


# Definições de cores e tolerâncias
script_dir = os.path.dirname(os.path.abspath(__file__))
S_HEIGHT, S_WIDTH = (PIL.ImageGrab.grab().size)
PARRY_R, PARRY_G, PARRY_B = (139, 146, 253)
PARRY2_R, PARRY2_G, PARRY2_B = (34, 41, 255)
BLOCK_R, BLOCK_G, BLOCK_B = (37, 46, 245)
DODGE_R, DODGE_G, DODGE_B = (246, 98, 8)
BOX_R, BOX_G, BOX_B = (5,107, 255)
BOX2_R, BOX2_G, BOX2_B = (65,131, 5)
GB_R, GB_G, GB_B = (250,31, 26)
TOLERANCE_PARRY = 2
TOLERANCE_BLOCK = 10
TOLERANCE_BOX = 1
TOLERANCE_BOX2 = 5
TOLERANCE_DODGE = 1
TOLERANCE_GB = 2
CGB_coord_x = 0
CGB_coord_y = 0
search_width = 0
search_height = 0
block_coord_x = 0
target_color3 = np.array([BOX_R, BOX_G, BOX_B])
block_coord_y = 0
total_width2, total_height2 = 1920, 1080
region_width2, region_height2 = 400, 400
center_x2, center_y2 = total_width2 // 2, total_height2 // 2
left2 = center_x2 - region_width2 // 2 -400
top2 = center_y2 - region_height2 // 2 -220
right2 = left2 + region_width2
bottom2 = top2 + region_height2
total_width, total_height = 1920, 1080
region_width, region_height = 150, 200
center_x, center_y = total_width // 2, total_height // 2
left = center_x - region_width // 2 +30
top = center_y - region_height // 2 -250
right = left + region_width
bottom = top + region_height
key_pressed = False
center_block_x = 0
center_block_y = 0
target_color1 = np.array([PARRY2_R, PARRY2_G, PARRY2_B])
target_color2 = np.array([PARRY_R, PARRY_G, PARRY_B])
lower_bound2 = target_color2 - TOLERANCE_PARRY
upper_bound2 = target_color2 + TOLERANCE_PARRY
target_color4 = np.array([BOX2_R, BOX2_G, BOX2_B])
box1=False
search_area_size = 200  # Tamanho da nova área de busca
new_pmap = 1
box_pmap = 1
new_left, new_top = 0,0
window = gw.getWindowsWithTitle('For Honor®')[0]
target_color = np.array([BLOCK_R, BLOCK_G, BLOCK_B])
lower_bound = target_color - TOLERANCE_BLOCK
upper_bound = target_color + TOLERANCE_BLOCK
# Definições de entrada do teclado
user32 = ctypes.WinDLL('user32', use_last_error=True)
INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
MAPVK_VK_TO_VSC = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2
wintypes.ULONG_PTR = wintypes.WPARAM
AUTOBLOCK_KEY = "F1"
AUTODODGE_KEY = "F2"
AUTOPARRY_KEY = 0x43

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
    
    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk, MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD),
                ("_input", _INPUT))
LPINPUT = ctypes.POINTER(INPUT)

def move_mouse(x, y, absolute=False):
    flags = MOUSEEVENTF_MOVE
    if absolute:
        flags |= MOUSEEVENTF_ABSOLUTE
        # Normalize x and y to be in the range 0 - 65535
        screen_width = 1920
        screen_height = 1080
        x = int(x * 65535 / screen_width)
        y = int(y * 65535 / screen_height)
    
    mi = MOUSEINPUT(dx=x, dy=y, dwFlags=flags)
    input = INPUT(type=INPUT_MOUSE, mi=mi)
    user32.SendInput(1, ctypes.byref(input), ctypes.sizeof(input))

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=hexKeyCode, dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

async def BlockUp():
     PressKey(0x26)
     time.sleep(0.01)
     ReleaseKey(0x26)

async def BlockLeft():
      PressKey(0x25)
      time.sleep(0.01)
      ReleaseKey(0x25)

async def BlockRight():
      PressKey(0x27)
      time.sleep(0.01)
      ReleaseKey(0x27)

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def RightClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)


class triggerBot():
    def __init__(self):
        self.last_move_time = 0  # Armazena o tempo da última ação de movimento
        self.move_interval = 1.0  # Intervalo de 1 segundo entre os movimentos
        self.last_move_time_parry = 0  # Armazena o tempo da última ação de movimento
        self.move_interval_parry = 0.0  # Intervalo de 1 segundo entre os movimentos
        self.toggledAutoblock = False
        self.toggledDodge = False

    def draw_rectangle(self, left, top, width, height):
        window_title = "Título da Janela"
        hwnd = win32gui.FindWindow(None, window_title)
        hwnd = win32gui.GetDesktopWindow()
        hdc = win32gui.GetWindowDC(hwnd)
        
        
        # Criar um pincel vermelho de 2 pixels de largura
        pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(255, 0, 0))
        old_pen = win32gui.SelectObject(hdc, pen)
        
        # Desenhar o retângulo com bordas
        win32gui.Rectangle(hdc, left, top, left + width, top + height)
        
        # Restaurar o pincel antigo e liberar a DC
        win32gui.SelectObject(hdc, old_pen)
        win32gui.DeleteObject(pen)
        win32gui.ReleaseDC(hwnd, hdc)


    def toggleAutoblock(self):
        self.toggledAutoblock = not self.toggledAutoblock
        if bot.toggledAutoblock:
            print("Autoblock Activated")
            winsound.Beep(440, 75)
            winsound.Beep(700, 100)
        else:
            print("Autoblock Deactivated")
            winsound.Beep(440, 75)
            winsound.Beep(200, 100)

    def toggleDodge(self):
        self.toggledDodge = not self.toggledDodge
        if bot.toggledDodge:
            print("auto dodge Activated")
            winsound.Beep(440, 75)
            winsound.Beep(700, 100)
        else:
            print("autodoge Deactivated")
            winsound.Beep(440, 75)
            winsound.Beep(200, 100)
    def resetMouse(self):
        global center_block_x
        global center_block_y
        move_mouse(1680//2,1050//2)
        
    def scale_coordinates(self,x, y, orig_width, orig_height, new_width, new_height):
        new_x = int(x * new_width / orig_width)
        new_y = int(y * new_height / orig_height)
        return new_x, new_y
    
    async def Box(self):
        global block_coord_y, block_coord_x
        global new_left, new_top
        global new_pmap
        global box_pmap
        global box1
        global top
        global search_width
        global search_height
        
        with mss.mss() as sct:
            monitor = {"top": 310, "left": 580, "width": 755 - 580, "height": 460 - 310}
            new_pmap = sct.grab(monitor)

        img_np = np.array(new_pmap)
        # Aplica a máscara de uma vez usando broadcasting
        new_mask = np.all((img_np[..., :3] == target_color4), axis=-1)
        #self.draw_rectangle(580, 310, 755-580, 460-310)
        # image_path = "temp4.png"
        # pmap.save(image_path)

        if np.any(new_mask):
            box1 = True
        else:
            box1 = False    

        with mss.mss() as sct:
            monitor = {"top": top-50, "left": left, "width": right - left, "height": bottom - (top-50)}
            new_pmap = sct.grab(monitor)

        img_np = np.array(new_pmap)
        #self.draw_rectangle(left, top-50, right - left, bottom - (top-50))
        new_mask = np.all((img_np[..., :3] == target_color3), axis=-1)
        rows, cols = np.nonzero(new_mask)
        if rows.size > 0: 
 
            block_coord_x = cols[0]
            block_coord_y = rows[0]
            if(box1):
                search_width = 200
                search_height = 300
                vertical_offset = 180
                horizontal_offset = 40
            else:
                search_width = 300
                search_height = 500
                vertical_offset = 320 
                horizontal_offset = 40      
            # Definir nova área de busca ao redor do pixel encontrado
            # Exibir a imagem usando matplotlib
            # Definir nova área de busca ao redor do pixel encontrado
            new_left =left + block_coord_x - search_width//2 - horizontal_offset
            new_top = top+ block_coord_y - search_height //2 +vertical_offset

            #self.draw_rectangle(new_left, new_top, search_width,search_height)
            # Atualizar a área de captura com base nas novas coordenadas
            with mss.mss() as sct:
                monitor = {"top": new_top, "left": new_left, "width": search_width, "height": search_height}
                box_pmap = sct.grab(monitor)
            
        

    async def Parry(self):
            if win32api.GetAsyncKeyState(AUTOPARRY_KEY):
                # self.draw_rectangle(new_left , new_top, width, height)
                new_img_np = np.array(box_pmap)

                # Aplica a máscara de uma vez usando broadcasting
                new_mask = np.all((new_img_np[..., :3] == target_color1), axis=-1)
                if not np.any(new_mask):

                    # Aplica a máscara de uma vez usando broadcasting
                    new_mask = np.all((new_img_np[..., :3] >= lower_bound2) & (new_img_np[..., :3] <= upper_bound2), axis=-1)
                    if np.any(new_mask):
                            # current_time = time.time()
                            # if current_time - self.last_move_time_parry >= self.move_interval_parry:
                            #     self.last_move_time_parry = current_time
                            
                            #     RightClick()
                            #     # PressKey(0x48)
                            #     # ReleaseKey(0x48)
                            #     # await asyncio.sleep(1)
                        RightClick()
 


    async def Dodge(self):
        if self.toggledDodge:
            y, x = block_coord_y,block_coord_x
            global box_pmap
            # Exibir a imagem usando matplotlib
            # self.draw_rectangle(left + x- search_area_size, top + y- search_area_size, 400, 700)
            # Definir nova área de busca ao redor do pixel encontrado     
            new_img_np = np.array(box_pmap)
            # Realizar nova busca na nova área
            new_r, new_g, new_b = new_img_np[:, :, 0], new_img_np[:, :, 1], new_img_np[:, :, 2]
            dodge_mask = ((DODGE_R - TOLERANCE_DODGE < new_r) & (new_r < DODGE_R + TOLERANCE_DODGE) &
                (DODGE_G - TOLERANCE_DODGE < new_g) & (new_g < DODGE_G + TOLERANCE_DODGE) &
                (DODGE_B - TOLERANCE_DODGE < new_b) & (new_b < DODGE_B + TOLERANCE_DODGE))
            dodge_coords = np.argwhere(dodge_mask)
            if(dodge_coords.size  > 0):
                    if keyboard.is_pressed('w'):
                        time.sleep(0.01)
                        PressKey(0x53)
                        time.sleep(0.01)
                        ReleaseKey(0x53) 
                        time.sleep(0.01) 
                        PressKey(0x35)
                        time.sleep(0.01)
                        ReleaseKey(0x35)
                
                    else:
                        await asyncio.sleep(0.05)
                        PressKey(0x35)
                        time.sleep(0.01)
                        ReleaseKey(0x35)
            
    async def AutoBlock(self):
        global box_pmap
        global center_block_x
        global center_block_y
    
        if(box_pmap != 1):
            new_img_np = np.array(box_pmap)
            # Aplica a máscara de uma vez usando broadcasting
            new_mask = np.all((new_img_np[..., :3] >= lower_bound) & (new_img_np[..., :3] <= upper_bound), axis=-1)
            rows, cols = np.nonzero(new_mask)
            
            if rows.size > 0:        
                
                distance_to_top = rows[0]
                distance_to_left = cols[0]
                distance_to_right = search_width - cols[0]
                
                distances = {
                    "top": distance_to_top,
                    "left": distance_to_left,
                    "right": distance_to_right
                }

                closest_side = min(distances, key=distances.get)
                # current_time = time.time()
                # if current_time - self.last_move_time >= self.move_interval:
                #     # Atualizar o tempo da última ação
                #     self.last_move_time = current_time
                    
                #     move_funcs = {"top": BlockUp, "left": BlockLeft, "right": BlockRight}
                #     await move_funcs[closest_side]()
                
                move_funcs = {"top": BlockUp, "left": BlockLeft, "right": BlockRight}
                await move_funcs[closest_side]()


            


    async def monitor(self):
        while True:
            if self.toggledAutoblock:
                if window.isActive:   
                    await self.call_tests()

    async def call_tests(self):
        tasks = [
            asyncio.create_task(self.Box()),
            asyncio.create_task(self.Dodge()),
            asyncio.create_task(self.AutoBlock()),
            asyncio.create_task(self.Parry()),
        ]
        await asyncio.gather(*tasks)

    async def CGB(self):
            
            vertical_offset = 450
            # start_time = time.time()
            y, x = CGB_coord_y,CGB_coord_x
            if(y < 200 and x < 200):
                vertical_offset = 450
            else:
                vertical_offset = 220    
            # Definir nova área de busca ao redor do pixel encontrado
         
            new_left =left2 + x - search_area_size //2 + 150
            new_top = top2+ y - search_area_size //2 +vertical_offset
            new_right = new_left  + search_area_size
            new_bottom = new_top + search_area_size
            width = new_right - new_left
            height = new_bottom - new_top
            # self.draw_rectangle(new_left , new_top, width, height)
            # Atualizar a área de captura com base nas novas coordenadas
            new_pmap = PIL.ImageGrab.grab(bbox=(new_left, new_top, new_right, new_bottom))
            new_img_np = np.array(new_pmap)

            # Realizar nova busca na nova área
            new_r, new_g, new_b = new_img_np[:, :, 0], new_img_np[:, :, 1], new_img_np[:, :, 2]
            gb_mask = (new_r == GB_R) & (new_g == GB_G) & (new_b == GB_B)
            GB_coords = np.argwhere(gb_mask)
            if(GB_coords.size  > 0):
                # new_y, new_x = GB_coords[0]
     
                # cv2.rectangle(new_img_np, (new_x - 10, new_y - 10), (new_x + 10, new_y + 10), (255, 0, 0), 2)
                # plt.imshow(cv2.cvtColor(new_img_np, cv2.COLOR_BGR2RGB))
                # plt.title("New Detected Area")
                # plt.show()
                # print("gby found in:", x, y)   
                PressKey(0x37)
                # print("\rStun's reaction time : {} ms".format(int((time.time() - start_time)*1000))) 
                time.sleep(0.01)
                ReleaseKey(0x37)
                await asyncio.sleep(0.7)

    async def Box2(self):
        global CGB_coord_y, CGB_coord_x
        pmap = PIL.ImageGrab.grab(bbox=(left2, top2, right2, bottom2))
        img_np = np.array(pmap)
        r, g, b = img_np[:, :, 0], img_np[:, :, 1], img_np[:, :, 2]
        mask = (r == BOX_R) & (g == BOX_G) & (b == BOX_B)
        # self.draw_rectangle(left, top, region_width, region_height)
        # image_path = "temp4.png"
        # pmap.save(image_path)
        coords = np.argwhere(mask)

        if coords.size > 0:
            CGB_coord_y, CGB_coord_x = coords[0]

               

if __name__ == "__main__":
    print("For Honor Autoblock/parry v2")
    print("Features :\n", AUTOBLOCK_KEY, " : Activate Autoblock\n", AUTODODGE_KEY ," : Activate Autododge")
    bot = triggerBot()
    keyboard.add_hotkey(AUTOBLOCK_KEY, bot.toggleAutoblock)
    keyboard.add_hotkey(AUTODODGE_KEY, bot.toggleDodge)
    async def main():
        await bot.monitor()


    asyncio.run(main())
          
