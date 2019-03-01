#Qrcode View

import qrcode
import time
import psutil
from ..modules.carry import global_scope

def generate_qrcode(password, version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=15, border=1):
    """
    Generate a qrcode of the password using qrcode module
    """
    
    qr = qrcode.Qrcode(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )

    qr.add_data(password)
    qr.make(fit=True)

    return qr.make_image(fill_color="black", back_color="white")


def display_qrcode(img, duration=None):
    """
    display a qrcode(pillow image)
    duration in secondes if specified, 
        the image will be close after the duration and all temporary image will be destroyed
    """

    img.show()

    if duration != None and duration > 0:
        try:
            time.sleep(duration)
        except KeyboardInterrupt:
            # Will catch `^-c` and immediately close qrcode
            pass
        
        for proc in psutil.process_iter():
            if proc.name == "display":
                try:
                    proc.terminate()
                except:
                    pass
                time.sleep(1)
                try:
                    proc.kill()
                except:
                    pass

def show(item):
    
    print("* The qrcode will be hidden after %s seconds." %
              (global_scope['conf'].hideQrcodeTTL))
    
    qrcode = generate_qrcode(item.password)

    display_qrcode(img, (global_scope['conf'].hideQrcodeTTL))

    return

